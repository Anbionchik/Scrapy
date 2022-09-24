import scrapy
from scrapy.http import HtmlResponse
from parser_job.items import ParserJobItem


class LabirintRuSpider(scrapy.Spider):
    name = 'labirint_ru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/books/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//div[@class='product-cover']/a[@class='product-title-link']/@href").get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

        urls_books = response.xpath("//div[@class='product-cover']//a[@class='product-title-link']/@href").getall()
        for url_book in urls_books:
            yield response.follow(url_book, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        book_ref = response.url
        book_title = self.exctract_data(response.xpath("//h1/text()"))
        book_author = self.exctract_data(response.xpath("//div[@class='authors']/a/text()"))
        book_main_price = self.exctract_data(response.xpath('//div[@class="buying-priceold-val"]/span/text()'))
        book_discount_price = self.exctract_data(response.xpath('//div[@class="buying-pricenew-val"]/span[@class="buying-pricenew-val-number"]/text()'))
        book_rating = self.exctract_data(response.xpath('//div[@id="rate"]/text()'))

        yield ParserJobItem(
            ref=book_ref,
            title=book_title,
            author=book_author,
            main_price=book_main_price,
            discount_price=book_discount_price,
            rating=book_rating
        )

    def exctract_data(self, selector):
        if len(selector) == 0:
            variable = None
        elif len(selector) == 1:
            variable = selector[0].root
        elif len(selector) > 1:
            variable = ', '.join([x.root for x in selector])

        return variable