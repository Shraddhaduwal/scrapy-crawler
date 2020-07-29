import scrapy
import re


class ArchiveSpider(scrapy.Spider):
    name = "archives_new"
    allowed_domain = "archive.nepalitimes.com/"
    start_urls = ["https://archive.nepalitimes.com/issue_archive/list/2013/"]

    def parse(self, response):
        main_links1 = response.xpath('//div[@class="section latest_issue issue_left"]/div[@class="news_image"]/a/@href')
        main_links2 = response.xpath('//div[@style="width:135px;height:192;border:1px solid #CCCCCC;"]/a/@href')
        main_links3 = response.xpath('//div[@style="width:135px;height:190;border:1px solid #CCCCCC;"]/a/@href')
        if main_links1:
            main_links = response.xpath('//div[@class="section latest_issue issue_left"]/div[@class="news_image"]/a/@href').extract()
        elif main_links2:
            main_links_2 = response.xpath('//div[@style="width:135px;height:192;border:1px solid #CCCCCC;"]/a/@href').extract()
            extra = response.xpath('//div[@style="width:135px;height:190;border:1px solid #CCCCCC;"]/a/@href').extract()
            main_links = main_links_2 + extra
        elif main_links3:
            main_links = response.xpath('//div[@style="width:135px;height:190;border:1px solid #CCCCCC;"]/a/@href').extract()
        else:
            main_links = response.xpath('//div[@style="width:120px;height:192;border:1px solid #CCCCCC;"]/a/@href').extract()

        for main_link in main_links:
            main_link = response.urljoin(main_link)
            yield scrapy.Request(main_link, callback=self.parse_link)

    def parse_link(self, response):
        front_links = response.xpath('.//div[@class="section"]/div[@class="news"]/h2/a/@href').extract()
        e_special_links = response.xpath('.//div[@class="brief_full"]/div[@class="grey"]/div[@class="section"]/h2[@class="brief"]/a/@href').extract()
        editorial_links = response.xpath('.//div[@class="section brief_full"]/h2/a/@href').extract()
        column_links = response.xpath('.//div[@class="brief_full"]/div[@class="section"]/div[@class="news"]/div[@class="news_container"]/div[@class="column_content"]/a[@class="categoryheading"]/@href').extract()
        about_town_links = response.xpath('.//div[@class="seperator"]/a/@href').extract()
        more_about_town_links = response.xpath('.//div[@class="section tabs border_bottom"]/a/@href').extract()
        from_nepalipress_links = response.xpath('.//div[@class="section"]/div[@class="news"]/a/@href').extract()

        issue_date = response.xpath('.//div[@class="main_headline section-heading"]/h2/a/text()').get()
        issue_tag = response.xpath('.//div[@class="main_headline section-heading"]/h2/text()').get()

        links = front_links + e_special_links + editorial_links + column_links + about_town_links + more_about_town_links + from_nepalipress_links

        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_article, meta={'issue_date': issue_date, 'issue_tag': issue_tag})

    @staticmethod
    def remove_html_tags(text):
        """Remove html tags from a string"""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def parse_article(self, response):
        issue_date1 = response.xpath('.//div[@class="asidedetails"]/h4/a/text()')
        issue_date2 = response.xpath('.//span[@class="date1"]/text()')
        issue_date3 = response.xpath('.//span[@class="date1"]/text()')
        if issue_date1:
            issue_date = response.xpath('.//div[@class="asidedetails"]/h4/a/text()')[0].extract()
        elif issue_date2:
            issue_date = response.xpath('.//span[@class="date1"]/text()')[0].extract()
        elif issue_date3:
            issue_date = response.xpath('.//div[@class="postdatetime"]/text()')[0].extract()
        else:
            issue_date = response.meta['issue_date']

        issue_tag1 = response.xpath('.//div[@class="asidedetails"]/h4/text()')
        if issue_tag1:
            issue_tag = response.xpath('.//div[@class="asidedetails"]/h4/text()').get()
        else:
            issue_tag = response.meta['issue_tag']

        category1 = response.xpath('.//div[@class="category"]/a/text()')
        category2 = response.xpath('.//h2[@class="red_heading"]/text()')
        if category1:
            category = response.xpath('.//div[@class="category"]/a/text()').get()
        elif category2:
            category = response.xpath('.//h2[@class="red_heading"]/text()').get()
        else:
            category = response.xpath('.//span[@class="category"]/text()').get()

        headline1 = response.xpath('.//div[@class="asidedetails"]/h2/text()')
        headline2 = response.xpath('.//div[@class="blog_title"]/h2[@class="red_title"]/text()')
        headline3 = response.xpath('.//h2[@class="sub-heading"]/text()')
        if headline1:
            headline = response.xpath('.//div[@class="asidedetails"]/h2/text()').get()
        elif headline2:
            headline = response.xpath('.//div[@class="blog_title"]/h2[@class="red_title"]/text()').get()
        elif headline3:
            headline = response.xpath('.//h2[@class="sub-heading"]/text()').get()
        else:
            headline = response.xpath('.//span[@class="heading"]/text()').get()

        author1 = response.xpath('.//div[@class="author_name"]/span[@itemprop="name"]/text()')
        author2 = response.xpath('.//div[@class="author_name"]/text()')
        author3 = response.xpath('.//div[@class="excerpt"]/text()')
        if author1:
            author = response.xpath('.//div[@class="author_name"]/span[@itemprop="name"]/text()').get()
        elif author2:
            author = response.xpath('.//div[@class="author_name"]/text()').get()
        elif author3:
            author = response.xpath('.//div[@class="excerpt"]/text()').get()
        else:
            author = response.xpath('.//span[@class="writer"]/text()').get()

        article1 = response.css('.article_content, p')
        article2 = response.css('.entry, text')
        article3 = response.css('.articletext, p')
        if article1:
            article = ''.join(response.css('.article_content, p').extract())
        elif article2:
            article = ''.join(response.css('.entry, p').extract())
        elif article3:
            article = ''.join(response.css('.articletext, p').extract())
        else:
            article = ''.join(response.css('.articletext, text').extract())

        article = ArchiveSpider.remove_html_tags(article)
        if article:
            yield {'issue_date': issue_date, 'issue_tag': issue_tag, 'title': headline, 'author': author, 'body': article, 'category': category}
