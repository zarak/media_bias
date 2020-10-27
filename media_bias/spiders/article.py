# -*- coding: utf-8 -*-
import scrapy
import w3lib
import datetime
from newspaper import Article


class ArticleSpider(scrapy.Spider):
    name = 'article'
    start_urls = []

    def parse_article(self, response):
        article = Article(response.url)
        article.download()
        article.parse()
        yield{
            'link': response.url,
            'headline': article.title,
            'publish_date': article.publish_date.strftime('%m-%d-%y'),
            'text': article.text,
            'image': article.top_image}
