import scrapy


class TestSpider(scrapy.Spider):
    name = "setopati"
    allowed_domain = "setopati.com"

    start_urls = ["https://setopati.com"]

    def parse(self, response):
        main_links = response.xpath('//div[@class="navigation_box"]/ul/li/a/@href').extract()
        for main_link in main_links:
            main_link = response.urljoin(main_link)
            yield scrapy.Request(main_link, callback=self.parse_link)

    def parse_link(self, response):
        links = response.xpath('//a/@href').extract()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_article)

        next_page = response.xpath(".//div[@class='pagination']/a[@rel='next']/@href")[0].extract()
        next_page = response.urljoin(next_page)

        yield scrapy.Request(next_page, dont_filter=True, callback=self.parse_link)

    def parse_article(self, response):
        authors = response.xpath('.//div[@class="row authors-box"]')

        if authors:
            headline = response.xpath('.//span[@class="news-big-title"]/text()')[0].extract()
            author = response.xpath('.//span[@class="main-title"]/a/text()')[0].extract()
            date = response.xpath('.//span[@class="pub-date"]/text()')[0].extract().split(",")[1:]
            article = ''.join(response.xpath('.//div[@class="editor-box"]//text()').extract())
            category = response.xpath('.//span[@class="cat-title"]/text()')[0].extract()

            if article:
                yield {'title': headline, 'author': author, 'date': date, 'body': article, 'category': category}
