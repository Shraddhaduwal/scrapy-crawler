import scrapy


class RatopatiSpider(scrapy.Spider):
    name = "ratopati"
    allowed_domain = "ratopati.com"

    start_urls = ["https://ratopati.com/"]

    def parse(self, response):
        main_links = response.xpath('//li[@id="main-menu-items"]/a/@href').extract()
        for main_link in main_links:
            main_link = response.urljoin(main_link)
            yield scrapy.Request(main_link, callback=self.parse_link)

    def parse_link(self, response):
        links = response.xpath('//div[@class="item-content"]/span/a/@href').extract()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_article)

        next_page = response.xpath('.//a[@class="next page-numbers"]/@href')[0].extract()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, dont_filter=True, callback=self.parse_link)

    def parse_article(self, response):
        headline = response.xpath('.//div[@class="article-head"]/h1/text()')[0].extract()
        author = response.xpath('.//span[@itemprop="author"]/text()')[0].extract()
        date = response.xpath('.//span[@class="meta-item"]/text()')[0].extract()
        article = ''.join(response.xpath('.//div[@class="imgAdj"]/p/text()').extract())
        category = response.xpath('.//li[@class="breadcrumb-item active"]/a/text()')[0].extract()
        yield {'title': headline, 'author': author, 'date': date, 'body': article, 'category': category}
