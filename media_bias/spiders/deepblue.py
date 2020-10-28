# -*- coding: utf-8 -*-
import scrapy
import w3lib
import datetime
import pandas as pd
from newspaper import Article


class DeepBlueSpider(scrapy.Spider):
    name = 'deepblue'

    df = pd.read_csv('newsArticlesWithLabels.tsv', sep='\t')
    print("df", df.head())
    print("cols", df.columns)
    
    start_urls = list(df.url)

    def parse(self, response):
        article = Article(response.url)
        article.download()
        article.parse()
        yield {
            'url': response.url,
            'text': article.text,
        }
