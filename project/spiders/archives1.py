import scrapy
import re


class ArchiveSpider(scrapy.Spider):
    name = "archives_old"
    allowed_domain = "archive.nepalitimes.com/"
    start_urls = ["http://archive.nepalitimes.com/issue/archive/2005/"]

    def parse(self, response):
        # main_links1 = response.xpath('//div[@class="section latest_issue issue_left"]/div[@class="news_image"]/a/@href')
        main_links1 = response.xpath('//div[@style="width:135px;height:192;border:1px solid #CCCCCC;"]/a/@href')
        main_links2 = response.xpath('//div[@style="width:135px;height:190;border:1px solid #CCCCCC;"]/a/@href')
        # if main_links1:
        #     main_links = response.xpath('//div[@class="section latest_issue issue_left"]/div[@class="news_image"]/a/@href').extract()
        if main_links1:
            main_links_1 = response.xpath('//div[@style="width:135px;height:192;border:1px solid #CCCCCC;"]/a/@href').extract()
            extra = response.xpath('//div[@style="width:135px;height:190;border:1px solid #CCCCCC;"]/a/@href').extract()
            main_links = main_links_1 + extra
        elif main_links2:
            main_links = response.xpath('//div[@style="width:135px;height:190;border:1px solid #CCCCCC;"]/a/@href').extract()
        else:
            main_links = response.xpath('//div[@style="width:120px;height:192;border:1px solid #CCCCCC;"]/a/@href').extract()

        for main_link in main_links:
            main_link = response.urljoin(main_link)
            yield scrapy.Request(main_link, callback=self.parse_link)
        next_page = response.xpath('.//a[@class="updatesmallheading"]/@href').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_link(self, response):
        # front_links = response.xpath('.//h2[@class="front-heading"]/a/@href').extract()
        # e_special_links = response.xpath('.//div[@class="brief_full"]/div[@class="grey"]/div[@class="section"]/h2[@class="brief"]/a/@href').extract()
        # editorial_links = response.xpath('.//div[@class="section brief_full"]/h2/a/@href').extract()
        # guest_editorial_links = response.xpath('.//div[@class="brief_full"]/div[@class="section"]/div[@class="news"]/div[@class="news_container"]/div[@class="column_content"]/a[@class="categoryheading"]/@href').extract()
        # biz_brief_links = response.xpath('.//aside[@class="asideleft middlecolumn"]/div[@class="section"]/div[@class="news"]/h2/a/@href').extract()
        # about_town_links = response.xpath('.//div[@class="seperator"]/a/@href').extract()
        # from_nepalipress_links = response.xpath('.//div[@class="section"]/div[@class="news"]/a/@href').extract()

        issue_tag = response.xpath('.//font[@class="articlecategorysubheading"]/text()').get()

        # links1 = response.xpath('.//a[@class="categoryheading"]/@href')
        # if links1:
        links = response.xpath('//a[@class="categoryheading"]/@href').extract()
        # else:
        #     links = front_links + e_special_links + editorial_links + guest_editorial_links + biz_brief_links + about_town_links + from_nepalipress_links

        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_article, meta={'issue_tag': issue_tag})

    @staticmethod
    def remove_html_tags(text):
        """Remove html tags from a string"""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def parse_article(self, response):
        # issue_date1 = response.xpath('.//div[@class="asidedetails"]/h4/a/text()')
        # issue_date2 = response.xpath('.//span[@class="date1"]/text()')
        # if issue_date1:
        #     issue_date = response.xpath('.//div[@class="asidedetails"]/h4/a/text()')[0].extract()
        # elif issue_date2:
        #     issue_date = response.xpath('.//span[@class="date1"]/text()')[0].extract()
        # else:
        issue_date = response.xpath('.//div[@class="postdatetime"]/text()')[0].extract()

        # issue_tag1 = response.xpath('.//div[@class="asidedetails"]/h4/text()')
        # if issue_tag1:
        #     issue_tag = response.xpath('.//div[@class="asidedetails"]/h4/text()').get()
        # else:
        issue_tag = response.meta['issue_tag']

        # category1 = response.xpath('.//div[@class="category"]/a/text()')
        # category2 = response.xpath('.//h2[@class="red_heading"]/text()')
        # if category1:
        #     category = response.xpath('.//div[@class="category"]/a/text()')[0].extract()
        # elif category2:
        #     category = response.xpath('.//h2[@class="red_heading"]/text()')[0].extract()
        # else:
        category = response.xpath('.//span[@class="category"]/text()')[0].extract()

        # headline1 = response.xpath('.//div[@class="asidedetails"]/h2/text()')
        # headline2 = response.xpath('.//div[@class="blog_title"]/h2[@class="red_title"]/text()')
        # headline3 = response.xpath('.//h2[@class="sub-heading"]/text()')
        # if headline1:
        #     headline = response.xpath('.//div[@class="asidedetails"]/h2/text()').get()
        # elif headline2:
        #     headline = response.xpath('.//div[@class="blog_title"]/h2[@class="red_title"]/text()').get()
        # elif headline3:
        #     headline = response.xpath('.//h2[@class="sub-heading"]/text()').get()
        # else:
        headline = response.xpath('.//span[@class="heading"]/text()').get()

        # author1 = response.xpath('.//div[@class="author_name"]/span[@itemprop="name"]/text()')
        # author2 = response.xpath('.//div[@class="author_name"]/text()')
        # author3 = response.xpath('.//div[@class="excerpt"]/text()')
        # if author1:
        #     author = response.xpath('.//div[@class="author_name"]/span[@itemprop="name"]/text()').get()
        # elif author2:
        #     author = response.xpath('.//div[@class="author_name"]/text()').get()
        # elif author3:
        #     author = response.xpath('.//div[@class="excerpt"]/text()').get()
        # else:
        author = response.xpath('.//span[@class="writer"]/text()').get()

        article1 = response.css('.articletext, p')
        if article1:
            article = ''.join(response.css('.articletext, p').extract())
        else:
            article = ''.join(response.css('.articletext, text').extract())

        article = ArchiveSpider.remove_html_tags(article)
        if article:
            yield {'issue_date': issue_date, 'issue_tag': issue_tag, 'title': headline, 'author': author, 'body': article, 'category': category}
