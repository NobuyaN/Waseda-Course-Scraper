# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
from waseda.parser import make_schedules, make_terms, make_slots, shorten_mapped_string
import pymongo


class WasedaPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        """
            create a list of all instructors in a given course
            Example: MINOO, Arihiroothers／MORI, Masashi -> [MINOO, Arihiroothers, MORI, Masashi]
        """

        value = adapter.get("instructor")
        if value is not None:
            adapter["instructor"] = value.split("／")

        """
            change eligible_year into an integer number.
            The number represents what year and above students can take the respective course
            Example: 1st year and above -> 1
        """

        value = adapter.get("eligible_year")
        if value is not None:
            adapter["eligible_year"] = int(value[:1])

        """
            Convert from string to int
            Example: "exam_contrib_prcnt": "80" -> "exam_contrib_prcnt": 80
            If none, then return none
        """

        contrib_percnts = ["exam_contrib_prcnt", "papers_contrib_prcnt", "class_participation_contrib_prcnt", "others_contrib_prcnt", "credits", "year"]
        for field_name in contrib_percnts:
            value = adapter.get(field_name)
            if value is not None:
                adapter[field_name] = int(value)


        """
            shorten campus string: Nishi-Waseda（Former: Okubo) -> Nishi-Waseda
            capitalize waseda -> Waseda and other -> Other
            - Waseda
            - Nishi-Waseda
            - Toyama
            - Tokorozawa
            - Kikui-cho
            - Fucyu
            - Other
        """

        campus_mapping = {
            "nishi-waseda(former: okubo)": "Nishi-Waseda",
            "waseda": "Waseda",
            "other": "Other"
        }

        shorten_mapped_string(adapter, "campus", campus_mapping)
        
        """
            shorten level key string
        """

        level_mapping = {
            "beginner, initial or introductory": "Beginner",
            "intermediate, developmental and applicative": "Intermediate",
            "advanced, practical and specialized": "Advanced",
            "final stage advanced-level undergraduate": "Final-stage",
            "level of master": "Master",
            "level of doctor": "Doctor",
            "N/A": None
        }

        shorten_mapped_string(adapter, "level", level_mapping)

        """
            create a dictionary for term_day_period holding different periods 
            for courses of multiple classes
            List of different cases:
                - fall semester Fri.4
                - summer othersothers
                - summer quarter Mon.1-2
                - fall semester othersothers
                - fall term Fri.2
                - summer term othersothers
                - fall semester Wed.others
                - winter quarter 01:Mon.5／02:Thur.3 
                - fall semester 01:othersOn demand／02:othersOn demand
                - an intensive course(fall) othersothers
                - an intensive course(fall) Tues.others
                - an intensive course(spring) othersOn demand
                - fall semester Fri.7(evening)
                - full year Wed.6
                - full year othersothers
                - fall term／winter term 01:Fri.4／02:othersothers
                - summer and fall semester Tues.5-6
                - summer and fall semester othersothers
                - an intensive course(spring and fall) othersothers
                - an intensive course(spring and fall) othersOn demand
                - an intensive course(spring and fall) 01:Wed.5-6／02:Sat.3-4
                - an intensive course(spring) 01:Tues.1／02:Sat.others

                slots = [
                    {"season": __, "session": __, "day": __, "start_p": __, "end_p": __, "flags": {__}}},
                    {"season": __, "session": __, "day": __, "start_p": __, "end_p": __, "flags": {__}}}
                ]
        """

        terms = []
        schedules = []
        value = (adapter.get("term_day_period") or "").strip()

        INTENSIVE_RE = re.compile(
            r"an\s+intensive\s+course"
            r"\((?P<seasons>[A-Za-z]+(?:\s+and\s+[A-Za-z]+)*)\)\s+"
            r"(?P<tail>(?:(?:\d{2}:)?(?:[A-Za-z]+(?=\.)|others)\.?"
            r"(?:\d+(?:-\d+)?|others|On\s+demand)"
            r"(?:\([^)]+\))?(?:[/／])?)+)\s*"
        )

        HEADER_BLOCK = re.compile(
            r"(?P<header>(?:[A-Za-z]+(?:\s+and\s+[A-Za-z]+)*(?:\s+(?:semester|quarter|term|year))?)"
            r"(?:\s*[/／]\s*[A-Za-z]+(?:\s+and\s+[A-Za-z]+)*(?:\s+(?:semester|quarter|term|year))?)*)\s+"
            r"(?P<tail>(?:(?:\d+:)?(?:[A-Za-z]+(?=\.)|others)\.?"
            r"(?:\d+(?:-\d+)?|others|On\s+demand)"
            r"(?:\([^)]+\))?(?:[/／])?)+)\s*",
            re.I
        )

        HEADER_ITEM_RE = re.compile(
            r"^(?P<seasons>[A-Za-z]+(?:\s+and\s+[A-Za-z]+)*)"
            r"(?:\s+(?P<session>semester|quarter|term|year))?$",
            re.I
        )

        SEGMENT_RE = re.compile(
            r"(?:\d+:)?"  
            r"(?:"  
                r"(?P<day_others>others)(?P<period_flag>others|On\s+demand)" 
                r"|(?:(?P<day_word>[A-Za-z]+)\.(?P<period_text>(?P<start_time>\d+)(?:-(?P<end_time>\d+))?|others|On\s+demand))"  
            r")"
            r"(?:\((?P<note>[^)]+)\))?"   
            r"(?:[／/])?",
            re.I
        )

        intensive_m = INTENSIVE_RE.fullmatch(value)
        if intensive_m:
            terms_list = []
            seasons_text = intensive_m.group("seasons")
            seasons = re.split(r"\s+and\s+", seasons_text, flags=re.I)
            terms = make_terms(terms_list, seasons, session=None)
            schedules = make_schedules(intensive_m, SEGMENT_RE, intensive=True)

        if not intensive_m:
            header_block_m = HEADER_BLOCK.fullmatch(value)
            if header_block_m is None:
                spider.logger.warning(f"Could not parse term_day_period: '{value}'")
                adapter["term_day_period"] = {
                    "terms": [{"season": "Unknown", "session": None, "position": 1}],
                    "schedules": [{"seq": 1, "day": "Unknown", "period": "Unknown", "start_time": None, "end_time": None, "note": None, "flags": {"others": True, "time_unknown": True}}],
                    "slots": [{"season": "Unknown", "session": "Unknown", "day": "Unknown", "start_time": None, "end_time": None, "flags": {"time_unknown": True}}],
                }

                return item
            
            terms_list = []
            header_items = re.split(r"\s*[/／]\s*", header_block_m.group("header"))
            
            for item_text in header_items:
                header_item_m = HEADER_ITEM_RE.fullmatch(item_text)
                if header_item_m is None:
                    spider.logger.warning(f"Could not parse header item: '{item_text}'")
                    continue
                seasons_text = header_item_m.group("seasons")
                seasons = re.split(r"\s+and\s+", seasons_text, flags=re.I)
                session = header_item_m.group("session")
                terms = make_terms(terms_list, seasons, session)
            
            schedules = make_schedules(header_block_m, SEGMENT_RE, intensive=False)
        
        slots = make_slots(terms, schedules, value)

        adapter["term_day_period"] = {
            "terms": terms,
            "schedules": schedules,
        }

        adapter["slots"] = slots

        return item

class MongoPipeline:
    collection_name = "courses"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        doc = ItemAdapter(item).asdict()
        _id = str(doc.pop("pKey_id"))
        self.db[self.collection_name].update_one(
            {"_id": _id},
            {"$set": doc},
            upsert=True
        )

        return item