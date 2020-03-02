import scrapy

"""
Replace the link in `start_urls` into:
1. https://setopati.com/politics
2. https://setopati.com/social
3. https://setopati.com/art
4. https://setopati.com/opinion
5. https://setopati.com/nepali-brand
6. https://setopati.com/kinmel
7. https://setopati.com/sports
8. https://setopati.com/ghumphir
9. https://setopati.com/blog
10. https://setopati.com/literature
11. https://setopati.com/global

And save the output in different csv files:
eg scrapy crawl setopati -o setopati_art.csv 
"""


class SetopatiSpider(scrapy.Spider):
    name = "setopati"

    start_urls = ["https://setopati.com/global"]

    def parse(self, response):
        links = response.xpath('.//a/@href').extract()
        next_ = response.xpath('.//div[@class="pagination"]/a[@rel="next"]')

        if next_:
            for link in links:
                link = response.urljoin(link)

                yield scrapy.Request(link, callback=self.parse_article)

            next_page = response.xpath(".//div[@class='pagination']/a[@rel='next']/@href")[0].extract()
            next_page = response.urljoin(next_page)

            yield scrapy.Request(next_page, dont_filter=True)
        else:
            print("EOW")

    def parse_article(self, response):
        authors = response.xpath('.//div[@class="row authors-box"]')

        if authors:
            headline = response.xpath('.//span[@class="news-big-title"]/text()')[0].extract()
            author = response.xpath('.//span[@class="main-title"]/a/text()')[0].extract()
            date = response.xpath('.//span[@class="pub-date"]/text()')[0].extract().split(",")[1:]
            article = ''.join(response.xpath('.//div[@class="editor-box"]//text()').extract())

            if article:
                yield {"title": headline, "author": author, "date": date, "body": article}
