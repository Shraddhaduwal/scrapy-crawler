import scrapy


class NepalsamacharpatraSpider(scrapy.Spider):
    name = "nepal_samacharpatra"
    allowed_domain = "www.newsofnepal.com"
    start_urls = ["https://www.newsofnepal.com"]

    def parse(self, response):
        main_ = response.xpath('//ul[@class="navbar-nav mr-auto nav-justified w-100 my-nav"]/li/a/@href').extract()
        extra = response.xpath('//div[@class="dropdown-menu bg-dark dropdown-menu-right"]/a/@href').extract()
        main_links = main_ + extra
        for main_link in main_links:
            main_link = response.urljoin(main_link)
            yield scrapy.Request(main_link, callback=self.parse_link)

    def parse_link(self, response):
        category = response.xpath('.//h1[@class="archive-title p-2"]/text()')[0].extract()
        links = response.xpath('//a[@class="post-list d-flex"]/@href').extract()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_article, meta={'category': category})

        next_page = response.xpath('.//i[@class="page-link"]/a/@href')[-1].extract()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, dont_filter=True, callback=self.parse_link)

    def parse_article(self, response):
        headline = response.xpath('.//h1[@class="text-left pt-5"]/text()')[0].extract()
        author = response.xpath('.//div[@class="col-6 col-sm-3 align-self-center"]/h4/text()')[0].extract()
        date = response.xpath('.//div[@class="col-6 col-sm-3 lead align-self-center"]/h4/text()')[1].extract()
        article = ''.join(response.xpath('.//article[@class="post-entry"]/p/text()').extract())
        category = response.meta['category']

        if article:
            yield {'title': headline, 'author': author, 'date': date, 'body': article, 'category': category}
