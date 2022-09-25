# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.selector.unified import SelectorList


class ParserJobPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.books_labirint_ru

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        item = self.extract_data_form_selectors(item)
        collection.insert_one(item)

        return item

    def extract_data_form_selectors(self, item):
        for field in item.fields:
            try:
                if type(item[field]) == SelectorList:

                    selector = item[field]

                    if len(selector) == 0:
                        variable = None
                    elif len(selector) == 1:
                        variable = selector[0].root
                    elif len(selector) > 1:
                        variable = ', '.join([x.root for x in selector])

                    item[field] = variable
            except KeyError:
                continue
        return item
