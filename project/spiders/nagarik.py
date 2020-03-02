import scrapy

"""
Replace the link in `start_urls` into:
1. https://nagariknews.nagariknetwork.com/category/21 [politics]
2. https://nagariknews.nagariknetwork.com/category/22 [economy]
3. https://nagariknews.nagariknetwork.com/category/24 [politics]
4. https://nagariknews.nagariknetwork.com/category/25
5. https://nagariknews.nagariknetwork.com/category/26
6. https://nagariknews.nagariknetwork.com/category/27
7. https://nagariknews.nagariknetwork.com/category/31
8. https://nagariknews.nagariknetwork.com/category/125
9. https://nagariknews.nagariknetwork.com/category/81
10. https://nagariknews.nagariknetwork.com/category/82
11. https://nagariknews.nagariknetwork.com/category/85

And save the output in different csv files:
eg scrapy crawl nagarik -o nagarik-politics.csv 
"""


class NagarikSpider(scrapy.Spider):
    name = "nagarik"

    allowed_domain = ["nagariknews.nagariknetwork.com"]
    start_urls = ["https://nagariknews.nagariknetwork.com"]

    def parse(self, response):
        main_links = response.xpath('//ul[@class="nav navbar-nav"]/li/a/@href').extract()
        for main_link in main_links:
            main_link = response.urljoin(main_link)
            yield scrapy.Request(main_link, callback=self.parse_link)

    def parse_link(self, response):
        links = response.xpath('//div[@class="col-sm-9 detail-on"]/h3/a/@href').extract()
        for link in links:
            link = response.urljoin(link)

            yield scrapy.Request(link, callback=self.parse_article)

        next_page = response.xpath('.//ul[@class="pagination"]/li/a[@rel="next"]/@href')[0].extract()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, dont_filter=True, callback=self.parse_link)

    def parse_article(self, response):
        headline = response.xpath('.//div[@class="col-sm-12"]/h1/text()')[0].extract()
        author = response.xpath('.//span[@class="author"]/a/text()').extract()
        date = response.xpath('.//span[@class="publish-date"]/text()').get()
        article = response.xpath('.//div[@class="tag news-content"]/p/text()').extract()
        # category = response.xpath('')
        yield {'title': headline, 'author': author, 'date': date, 'article': article}
