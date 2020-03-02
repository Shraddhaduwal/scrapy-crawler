import scrapy


class OnlinekhabarSpider(scrapy.Spider):
    name = "onlinekhabar"
    allowed_domain = ["www.onlinekhabar.com"]

    start_urls = ["https://www.onlinekhabar.com"]

    def parse(self, response):
        main_links = response.xpath('//ul[@id="primary-menu"]/li/a/@href').extract()
        for main_link in main_links:
            main_link = response.urljoin(main_link)
            yield scrapy.Request(main_link, callback=self.parse_link)

    def parse_link(self, response):
        links = response.xpath('//div[@class="item__wrap"]/a/@href').extract()
        for link in links:
            link = response.urljoin(link)

            yield scrapy.Request(link, callback=self.parse_article)

        next_page = response.xpath('.//div[@class="paginate-links"]/a[@class="next page-numbers"]/@href')[0].extract()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, dont_filter=True, callback=self.parse_link)

    def parse_article(self, response):
        headline = response.xpath('.//h2[@class="mb-0"]/text()')[0].extract()
        author = response.xpath('.//div[@class="author__wrap"]/label/text()')[0].extract()
        date = response.xpath('.//div[@class="post__time"]/span/text()')[0].extract()
        category = response.xpath('.//div[@class="custom_breadcrumb"]/a/text()')[2].extract().split(" ")[0]
        article = ''.join(response.xpath('//div[@class="col colspan3 main__read--content ok18-single-post-content-wrap"]/p/text()').extract())
        yield {'title': headline, 'author': author, 'date': date, 'body': article, 'category': category}
