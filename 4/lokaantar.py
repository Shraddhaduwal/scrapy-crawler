import scrapy


class LokaantarSpider(scrapy.Spider):
    name = 'lokaantar'
    allowed_domain = "lokaantar.com"
    start_urls = ["https://lokaantar.com/"]

    def parse(self, response):
        main_links = response.xpath('//ul[@class="nav-menu"]/li/a/@href').extract()
        # extra = response.xpath('//ul[@class="nav-menu"]/li[@class="has-dropdown"]/div[@class="dropdown"]/div[@class="dropdown-body"]/ul/li/a/@href').extract()
        # main_links = main_ + extra
        for main_link in main_links:
            main_link = response.urljoin(main_link)
            yield scrapy.Request(main_link, callback=self.parse_link)

    def parse_link(self, response):
        links = response.xpath('//h3[@class="post-title title-sm"]/a/@href').extract()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_article)

        next_page = response.xpath('.//ul[@class="pagination"]/li/a/@href')[-2].extract()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, dont_filter=True, callback=self.parse_link)

    def parse_article(self, response):
        headline = response.xpath('.//div[@class="mt-3 mb-3 detail-title-font"]/h1/text()')[0].extract()
        author = response.xpath('.//div[@class="comment-content author-font comment-author-style"]/a/h5/text()')[0].extract()
        date = response.xpath('.//ul[@class="post-meta mb-4"]/li/text()')[1].extract()
        article = ''.join(response.xpath('.//p[@style="text-align: justify;"]/text()').extract())
        category = response.xpath('.//div[@class="post-category hot-post-category-tag"]/a/text()')[0].extract()

        if article:
            yield {'title': headline, 'author': author, 'date': date, 'body': article, 'category': category}
