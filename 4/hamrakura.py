import scrapy


class HamrakuraSpider(scrapy.Spider):
    name = "hamrakura"
    allowed_domain = "hamrakura.com"

    start_urls = ["https://hamrakura.com"]

    def parse(self, response):
        main_links = response.xpath('//ul[@class="nav navbar-nav"]/li/a/@href').extract()
        for main_link in main_links:
            main_link = response.urljoin(main_link)
            yield scrapy.Request(main_link, callback=self.parse_link)

    def parse_link(self, response):
        category = response.xpath('.//h1[@class="page-title"]/text()')[0].extract()
        links = response.xpath('//div[@class="itemCat"]/h4/a/@href').extract()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_article, meta={'category': category})

        # next_page = response.xpath('.//li[@class="pagination-items"]/a[@rel="nofollow"]/@href')[0].extract()

        next_page = response.xpath('.//li[@class="pagination-items"]/a/@href')[-1].extract()

        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, dont_filter=True, callback=self.parse_link)

    def parse_article(self, response):
        headline = response.xpath('.//h1[@class="page-title"]/text()')[0].extract()
        author = response.xpath('.//span[@class="writer"]/text()')[0].extract()
        date = response.xpath('.//span[@class="pubed"]/text()')[0].extract().split(":")[1]
        article = ''.join(response.xpath('.//div[@class="content-single"]/p/text()').extract())
        category = response.meta['category']

        if article:
            yield {'title': headline, 'author': author, 'date': date, 'body': article, 'category': category}
