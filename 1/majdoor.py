import scrapy


class MajdoorSpider(scrapy.Spider):
    name = "majdoor"
    allowed_domain = "onlinemajdoor.com"
    start_urls = ["https://onlinemajdoor.com"]

    def parse(self, response):
        main_links = response.xpath('//ul[@id="menu-primary-menu"]/li/a/@href')[:12].extract()
        for main_link in main_links:
            main_link = response.urljoin(main_link)
            yield scrapy.Request(main_link, callback=self.parse_link)

    def parse_link(self, response):
        category = response.xpath('.//div[@class="main-bar clearfix"]/h3/text()')[0].extract()
        links = response.xpath('//h3[@class="entry-title"]/a/@href').extract()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_article, meta={'category': category})

        next_page = response.xpath('.//a[@class="next page-numbers"]/@href')[0].extract()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, dont_filter=True, callback=self.parse_link)

    def parse_article(self, response):
        headline = response.xpath('.//div[@class="main-title"]/h3/text()')[0].extract()
        date = response.xpath('.//span[@class="post-time"]/text()')[0].extract()
        article = ''.join(response.xpath('.//div[@id="fontresizer"]/p/span/text()').extract())
        category = response.meta['category']

        if article:
            yield {'title': headline, 'date': date, 'body': article, 'category': category}
