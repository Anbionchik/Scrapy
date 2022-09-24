# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserJobItem(scrapy.Item):
    _id = scrapy.Field()
    ref = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    main_price = scrapy.Field()
    discount_price = scrapy.Field()
    rating = scrapy.Field()
