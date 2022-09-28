# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, Compose, TakeFirst


def clean_price(value):
    try:
        value = value[0].replace(" ", "").replace('/n', '')
        value = list(value)
    except KeyError:
        return value
    return value


class CastoramaItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(inpit_processor=Compose(clean_price), output_processor=TakeFirst())
    photos = scrapy.Field()
    _id = scrapy.Field()
