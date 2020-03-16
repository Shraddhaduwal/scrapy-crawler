import scrapy


class NepalkhabarSpider(scrapy.Spider):
    name = "nepalkhabar"
    allowed_domain = "nepalkhabar.com"
    start_urls = ["https://nepalkhabar.com"]

    def parse(self, response):
        main_links = response.xpath('//ul[@class="uk-navbar-nav uk-margin-remove"]/li/a/@href')[:-2].extract()
        for main_link in main_links:
            main_link = response.urljoin(main_link)
            yield scrapy.Request(main_link, callback=self.parse_link)

    def parse_link(self, response):
        links = response.xpath('//a[@class="uk-link-reset"]/@href').extract()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_article)

        next_page = response.xpath('.//a[@uk-tooltips="Next"]/@href')[0].extract()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, dont_filter=True, callback=self.parse_link)

    def parse_article(self, response):
        headline = response.xpath('.//h1[@class="uk-heading-medium uk-margin-remove"]/text()')[0].extract()
        author = response.xpath('.//span[@class="uk-text-meta nk-author"]/text()')[0].extract()
        date = response.xpath('.//div[@class="uk-margin-small-top published uk-text-bold uk-text-muted"]/text()')[1].extract()
        article = ''.join(response.xpath('.//div[@class="uk-article"]/p/text()').extract())
        category = response.xpath('.//div[@class="custom"]/text()')[1].extract()

        if article:
            yield {'title': headline, 'author': author, 'date': date, 'body': article, 'category': category}
