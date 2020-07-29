import scrapy
import re


class OpinionSpider(scrapy.Spider):
    name = "opinion"
    allowed_domain = "www.nepalitimes.com"
    start_urls = ["https://www.nepalitimes.com"]

    def parse(self, response):
        main_links = response.xpath('//ul[@class=" dropdown-menu"]/li/a/@href').extract()
        for main_link in main_links:
            main_link = response.urljoin(main_link)
            yield scrapy.Request(main_link, callback=self.parse_link)

    def parse_link(self, response):
        category = response.xpath('.//div[@class="multimedia-head"]/h2/strong/text()')[0].extract()
        links = response.xpath('.//a[@class="nt-image-link"]/@href').extract()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_article, meta={'category': category})
        next_page = response.xpath('.//div[@class="nav-next alignright"]/a/@href').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_link)

    @staticmethod
    def remove_html_tags(text):
        """Remove html tags from a string"""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def parse_article(self, response):
        headline = response.xpath('.//div[@class="about-page-detailing"]/h1/text()')[0].extract()
        author1 = response.xpath('.//span[@class="author fnt-mont"]/text()')
        if author1:
            author = response.xpath('.//span[@class="author fnt-mont"]/text()')[2].extract()
        else:
            author = response.xpath('.//span[@class="author fnt-mont"]/a/text()')[2].extract()

        issue_date = response.xpath('.//span[@class="dates"]/a/text()')[0].extract()
        article1 = response.css('.elementor-text-editor elementor-clearfix, p')
        if article1:
            article = ''.join(response.css('.elementor-text-editor elementor-clearfix, p').extract())
        else:
            article = ''.join(response.css('.article_content, text').extract())
        article = OpinionSpider.remove_html_tags(article)
        category1 = response.xpath('.//span[@class="cat_sub_name"]/strong/a/text()')
        if category1:
            category = response.xpath('.//span[@class="cat_sub_name"]/strong/a/text()')[0].extract()
        else:
            category = response.meta['category']
        if article:
            yield {'issue_date': issue_date, 'title': headline, 'author': author, 'body': article, 'category': category}
