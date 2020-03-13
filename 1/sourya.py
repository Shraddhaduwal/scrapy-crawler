import scrapy


class SouryaonlineSpider(scrapy.Spider):
    name = "sourya"
    allowed_domain = "www.souryaonline.com"
    start_urls = ["https://www.souryaonline.com"]

    def parse(self, response):
        main_links = response.xpath('//nav/ul/li/a/@href').extract()
        for main_link in main_links:
            main_link = response.urljoin(main_link)
            yield scrapy.Request(main_link, callback=self.parse_link)

    def parse_link(self, response):
        links = response.xpath('//div[@class="ar_loop"]/h2/a/@href').extract()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_article)

        next_page = response.xpath('.//a[@class="next page-numbers"]/@href')[0].extract()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, dont_filter=True, callback=self.parse_link)

    def parse_article(self, response):
        headline = response.xpath('.//div[@class="story_head"]/h1/text()')[0].extract()
        author = response.xpath('.//span[@class="writer"]/text()')[0].extract()
        date = response.xpath('.//span[@class="pubed"]/text()')[0].extract()
        article = response.xpath('.//div[@class="incon_sec"]/p/text()').extract()
        category = response.xpath('.//span[@class="catt"]/a/text()')[0].extract()

        if article:
            yield {'title': headline, 'author': author, 'date': date, 'body': article, 'category': category}
