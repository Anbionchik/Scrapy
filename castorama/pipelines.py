# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


class CastoramaPipeline:
    def process_item(self, item, spider):
        return item


class CastoramaPhotoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        try:
            for img in item['photos']:
                try:
                    yield Request(img)
                except Exception as e:
                    print(e)
        except KeyError as e:
            print(e)

    def item_completed(self, results, item, info):
        try:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        except KeyError:
            return item
        return item

    def file_path(self, request, response=None, info=None, item=None):
        # path_of_the_file = item['url'].split('/')[-1] + item['photos']['url'].split('/')[-1]
        path_of_the_file = item['url'].split('/')[-1] + '/' + request.url.split('/')[-1]
        return path_of_the_file


