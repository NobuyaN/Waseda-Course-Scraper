import scrapy
import json
from waseda.items import WasedaCourseItem
import uuid


class WasedascrapySpider(scrapy.Spider):
    name = "wasedaScrapy"
    allowed_domains = ["www.wsl.waseda.jp"]
    start_urls = ["https://www.wsl.waseda.jp/syllabus/JAA104.php?pKey=1100001010012025110000101011&pLng=en"]

    def parse(self, response):
        with open("data/clean_pKeys.json", "r", encoding="utf-8") as f:
            pKeys = json.load(f)
        for pKey in pKeys:
            course_url = f"https://www.wsl.waseda.jp/syllabus/JAA104.php?pKey={pKey}&pLng=en"
            yield response.follow(course_url, 
                                  self.parse_course_details,
                                  cb_kwargs={"pKey_id": pKey},
                                  )


    def parse_course_details(self, response, pKey_id):
        """
            using response.css would be very brittle due to different table sizes for different course
            therefore, xpath is recommended for detail extractions
        """

        def xPath_boilerplate(text):
            is_td_header = text in ["Exam:", "Papers:", "Class Participation:", "Others:"]
            search_tag = "td" if is_td_header else "th"

            xpath = f"normalize-space(translate(string(//{search_tag}[contains(normalize-space(.), '{text}')]/following-sibling::td[1]), '\xa0\u3000％', ' '))"
            if text == "Course Title":
                xpath = f"normalize-space(translate(string(//{search_tag}[contains(normalize-space(.), '{text}')]/following-sibling::td[1]//div), '\xa0\u3000％', ' '))"
            
            return response.xpath(xpath).get() or None

        item = WasedaCourseItem()
        """
            - Must yield strings
            - XPath is 1-based index
            - Since XPath is case-sensitive, translate(normalize-space(.), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz") is helpful
        """
     
        item["pKey_id"] = str(pKey_id)
        item["url"] = response.url
        item["year"] = xPath_boilerplate("Year") 
        item["school"] = xPath_boilerplate("School")
        item["course_title"] = xPath_boilerplate("Course Title")
        item["instructor_list"] = xPath_boilerplate("Instructor")
        item["term_day_period_str"] = xPath_boilerplate("Term/Day/Period")
        item["category"] = xPath_boilerplate("Category")
        item["eligible_year"] = xPath_boilerplate("Eligible Year")
        item["credits"] = xPath_boilerplate("Credits")
        item["classroom"] = xPath_boilerplate("Classroom")
        item["campus"] = xPath_boilerplate("Campus")
        item["main_language"] = xPath_boilerplate("Main Language")
        item["class_modality_categories"] = xPath_boilerplate("Class Modality Categories")
        item["level"] = xPath_boilerplate("Level")
        item["types_of_lesson"] = xPath_boilerplate("Types of lesson")
        item["exam_contrib_prcnt"] = xPath_boilerplate("Exam:")
        item["papers_contrib_prcnt"] = xPath_boilerplate("Papers:")
        item["class_participation_contrib_prcnt"] = xPath_boilerplate("Class Participation:")
        item["others_contrib_prcnt"] = xPath_boilerplate("Others:")
        
        yield item