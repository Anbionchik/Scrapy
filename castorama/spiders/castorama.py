import scrapy
from scrapy.http import HtmlResponse
from castorama.items import CastoramaItem
from scrapy.loader import ItemLoader


class CastoramaSpider(scrapy.Spider):
    name = 'castorama'
    allowed_domains = ['castorama.ru']

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = ['https://www.castorama.ru/catalogsearch/result/?q=фотообои']
        # self.start_urls = [f'https://www.castorama.ru/catalogsearch/result/?q={kwargs.get("query")}']

    def parse(self, response: HtmlResponse):
        pages_links = response.xpath("//a[contains(@class, 'product-card__name')]")
        for link in pages_links:
            yield response.follow(link, callback=self.parse_goods)


    def parse_goods(self, response: HtmlResponse):
        loader = ItemLoader(item=CastoramaItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('price', "//span[@class='price']/span/span/text()")
        loader.add_xpath('photos', "//li[contains(@class, 'thumb-slide')]/img/@data-src")
        loader.add_xpath('features', "//dl[@class='specs-table js-specs-table']/dt/span/text()")
        loader.add_xpath('features', "//dl[@class='specs-table js-specs-table']/dd/text()")
        yield loader.load_item()
