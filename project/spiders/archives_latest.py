import scrapy
import re


class ArchiveLatest(scrapy.Spider):
    name = "archives_latest"
    allowed_domain = "www.nepalitimes.com/nt/latest"
    start_urls = ["https://www.nepalitimes.com/nt/latest"]

    def parse(self, response):
        category = response.xpath('.//div[@class="multimedia-head"]/h2/strong/text()')[0].extract()
        links = response.xpath('.//a[@class="nt-header-link"]/@href').extract()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_article, meta={'category': category})
        next_page = response.xpath('.//a[@class="nav-next-link"]/@href')[0].extract()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    @staticmethod
    def remove_html_tags(text):
        """Remove html tags from a string"""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def parse_article(self, response):
        headline = response.xpath('.//div[@class="about-page-detailing"]/h1/text()')[0].extract()
        author = response.xpath('.//span[@class="author fnt-mont"]/text()')[2].extract()
        issue_date = response.xpath('.//span[@class="dates"]/a/text()')[0].extract()
        article = ''.join(response.css('.elementor-text-editor elementor-clearfix, p').extract())
        article = ArchiveLatest.remove_html_tags(article)
        category = response.meta['category']

        if article:
            yield {'issue_date': issue_date, 'title': headline, 'author': author, 'body': article, 'category': category}
