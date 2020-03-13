import scrapy


class AbhiyanSpider(scrapy.Spider):
    name = "abhiyan"
    allowed_domain = "www.abhiyandaily.com"
    start_urls = ["https://www.abhiyandaily.com"]

    def parse(self, response):
        main_ = response.xpath('//ul[@class="navbar-nav ml-auto"]/li/a/@href').extract()
        extra = response.xpath('//div[@class="dropdown-content"]/a/@href').extract()
        main_links = main_ + extra
        for main_link in main_links:
            main_link = response.urljoin(main_link)
            yield scrapy.Request(main_link, callback=self.parse_link)

    def parse_link(self, response):
        links = response.xpath('//div[@class="col-lg-8"]/a/@href').extract()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_article)

        next_page = response.xpath('.//a[@rel="next"]/@href')[0].extract()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, dont_filter=True, callback=self.parse_link)

    def parse_article(self, response):
        headline = response.xpath('.//div[@class="mb-4 bg-cont mr-m"]/h1/text()')[0].extract()
        author = response.xpath('.//div[@class="mb-4 bg-cont mr-m"]/figure/a/text()')[1].extract()
        date = response.xpath('.//div[@class="col-lg-4 mb-4 al-r"]/text()')[0].extract()
        article = ''.join(response.xpath('.//p[@style="text-align:justify"]/text()').extract())
        category = response.xpath('.//span[@class="span-bg abhiyaninner"]/text()')[0].extract()

        if article:
            yield {'title': headline, 'author': author, 'date': date, 'body': article, 'category': category}
