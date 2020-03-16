import scrapy


class KoshionlineSpider(scrapy.Spider):
    name = "koshi_online"
    allowed_domain = "www.koshionline.com"
    start_urls = ["https://www.koshionline.com"]

    def parse(self, response):
        main_links = response.xpath('//ul[@id="menu-main-new-menu"]/li/a/@href').extract()
        for main_link in main_links:
            main_link = response.urljoin(main_link)
            yield scrapy.Request(main_link, callback=self.parse_link)

    def parse_link(self, response):
        category = response.xpath('.//div[@class="he-part"]/h1/text()')[0].extract()
        links = response.xpath('//div[@class="ko-grid-post"]/a/@href').extract()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_article, meta={'category': category})

        next_page = response.xpath('.//div[@class="navigation"]/ul/li/a/@href')[-1].extract()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, dont_filter=True, callback=self.parse_link)

    def parse_article(self, response):
        headline = response.xpath('.//div[@class="ko-entry-single-title"]/h1/text()')[0].extract()
        author = response.xpath('.//span[@class="ko-author-name"]/text()')[0].extract()
        date = response.xpath('.//time[@class="ko-post-date"]/text()')[0].extract()
        article = ''.join(response.xpath('.//div[@class="ko-entry-data"]/p/text()').extract())
        category = response.meta['category']

        if article:
            yield {'title': headline, 'author': author, 'date': date, 'body': article, 'category': category}
