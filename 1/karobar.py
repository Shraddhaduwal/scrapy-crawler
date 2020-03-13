import scrapy


class KarobarSpider(scrapy.Spider):
    name = "karobar"
    allowed_domain = "karobardaily.com"
    start_urls = ["https://www.karobardaily.com/"]

    def parse(self, response):
        main_links = response.xpath('//ul[@class="nav navbar-nav"]/li/a/@href').extract()
        for main_link in main_links:
            main_link = response.urljoin(main_link)
            yield scrapy.Request(main_link, callback=self.parse_link)

    def parse_link(self, response):
        links = response.xpath('//div[@class="mn-header"]/h4/a/@href').extract()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_article)

        next_page = response.xpath('.//a[@rel="next"]/@href')[0].extract()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, dont_filter=True, callback=self.parse_link)

    def parse_article(self, response):
        headline = response.xpath('.//div[@class="col-lg-12"]/h4/text()')[0].extract()
        author = response.xpath('.//div[@class="author-name"]/span/text()')[0].extract()
        date = response.xpath('.//div[@class="date-time"]/span/text()')[0].extract()
        article1 = ''.join(response.xpath('.//div[@class="mn-text"]/p/text()').extract())
        article2 = ''.join(response.xpath('.//div[@class="mn-text"]/text()').extract())
        article = article1 + article2
        category = response.xpath('.//div[@class="col-lg-12"]/a/h2/text()')[0].extract()

        if article1:
            yield {'title': headline, 'author': author, 'date': date, 'body': article, 'category': category}