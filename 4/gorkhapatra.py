import scrapy


class GorkhapatraSpider(scrapy.Spider):
    name = "gorkhapatra"

    allowed_domain = "gorkhapatraonline.com"
    start_urls = ["https://gorkhapatraonline.com"]

    def parse(self, response):
        main_links = response.xpath('//ul[@class="navbar-nav"]/li/a/@href').extract()
        for main_link in main_links:
            main_link = response.urljoin(main_link)
            yield scrapy.Request(main_link, callback=self.parse_link)

    def parse_link(self, response):
        links = response.xpath('//div[@class="business"]/a/@href').extract()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_article)

        next_page = response.xpath('.//li[@class="page-item"]/a/@href')[1].extract()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, dont_filter=True, callback=self.parse_link)

    def parse_article(self, response):
        headline = response.xpath('.//h1[@class="post-title"]/text()')[0].extract()
        author = response.xpath('.//span[@class="post-author-name"]/a/text()')[0].extract()
        date = response.xpath('.//li[@class="forlist"]/text()')[4].extract()
        article = ''.join(response.xpath('.//div[@id="content"]/p/text()').extract())
        category = response.xpath('.//div[@class="catagory"]/text()')[0].extract()

        if article:
            yield {'title': headline, 'author': author, 'date': date, 'body': article, 'category': category}
