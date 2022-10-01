# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from itemloaders.processors import MapCompose, Compose, TakeFirst


def clean_price(value):
    for i, element in enumerate(value):
        try:
            value[i] = int(re.sub('[-|.|,|"|/|\xa0|\u202f| |/n|/D]', '', element))
        except ValueError:
            value[i] = element
        except KeyError:
            value[i] = element
    return value


def clean_string(values_list):
    for i in range(len(values_list)):
        string = values_list[i]
        string = re.sub('[/|\xa0|\u202f|\n]', '', string)
        string = string.rstrip().lstrip()
        values_list[i] = string
    return values_list


def create_features_dict(values_list):
    result_dict = {}
    half_length = int(len(values_list) / 2)
    for i in range(half_length):
        result_dict[values_list[i]] = values_list[i + half_length]
    return result_dict


# def get_features(element):
#     try:
#         specs = element.xpath("/dt/span/text()")
#         vals = element.xpath("dd/text()")
#         return {clean_string(spec): clean_string(val) for spec, val in zip(specs, vals)}
#     except KeyError as e:
#         print(e)


class CastoramaItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(clean_price), output_processor=TakeFirst())
    photos = scrapy.Field()
    features = scrapy.Field(input_processor=clean_string, output_processor=create_features_dict)
    _id = scrapy.Field()
