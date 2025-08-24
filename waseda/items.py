# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WasedaItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

class WasedaCourseItem(scrapy.Item):

    pKey_id = scrapy.Field()
    url = scrapy.Field()
    year = scrapy.Field()
    school = scrapy.Field()
    course_title = scrapy.Field()
    instructor = scrapy.Field()
    term_day_period = scrapy.Field()
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
