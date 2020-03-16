import scrapy


class MedianpSpider(scrapy.Spider):
    name = "medianp"
    allowed_domain = "medianp.com"
    start_urls = ["https://medianp.com"]

    def parse(self, response):
        main_links = response.xpath('//nav[@id="site-navigation"]/div/ul/li/a/@href').extract()
        for main_link in main_links:
            main_link = response.urljoin(main_link)
            yield scrapy.Request(main_link, callback=self.parse_link)

    def parse_link(self, response):
        category = response.xpath('.//h1[@class="page-title"]/text()')[0].extract()
        links = response.xpath('//h2[@class="entry-title"]/a/@href').extract()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_article, meta={'category': category})

        next_page = response.xpath('.//a[@class="next page-numbers"]/@href')[0].extract()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, dont_filter=True, callback=self.parse_link)

    def parse_article(self, response):
        headline = response.xpath('.//h1[@class="entry-title"]/text()')[0].extract()
        author = response.xpath('.//span[@class="author vcard"]/a/text()')[0].extract()
        date = response.xpath('.//span[@class="posted-on"]/text()')[0].extract()
        article = ''.join(response.xpath('.//p[@style="text-align: justify;"]/text()').extract())
        category = response.meta['category']

        if article:
            yield {'title': headline, 'author': author, 'date': date, 'body': article, 'category': category}
