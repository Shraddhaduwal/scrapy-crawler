# scrapy-crawler

This is a data-crawler made in `Scrapy`. The data from local newspapers is crawled for data processing purpose. There are a number of spiders through which we can start the data crawling. The crawled data is stored in `csv` files. The files can also be stored in other formats like .json, .txt etc as per the convenience.

## Start Scrapy Project
`scrapy startproject <project_name>`

## Run Spider
After navigating to the parent folder `<project_name>` :
- `scrapy crawl <spider_name>`

## Save the crawled data to different files
- `scrapy crawl <spider_name> -o <filename>.csv`
- `scrapy crawl <spider_name> -o <filename>.json`