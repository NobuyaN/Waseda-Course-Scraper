# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WasedaCourseItem(scrapy.Item):
    """
        An item representing a course at Waseda University.
    """

    pKey_id = scrapy.Field()
    url = scrapy.Field()
    year = scrapy.Field()
    school = scrapy.Field()
    course_title = scrapy.Field()
    instructor = scrapy.Field()
    term_day_period = scrapy.Field()
    slots = scrapy.Field()
    category = scrapy.Field()
    eligible_year = scrapy.Field()
    credits = scrapy.Field()
    classroom = scrapy.Field()
    campus = scrapy.Field()
    main_language = scrapy.Field()
    class_modality_categories = scrapy.Field()
    level = scrapy.Field()
    types_of_lesson = scrapy.Field()
    exam_contrib_prcnt = scrapy.Field()
    papers_contrib_prcnt = scrapy.Field()
    class_participation_contrib_prcnt = scrapy.Field()
    others_contrib_prcnt = scrapy.Field()
