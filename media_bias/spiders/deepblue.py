# -*- coding: utf-8 -*-
import scrapy
import w3lib
import datetime
import pandas as pd
from newspaper import Article


class DeepBlueSpider(scrapy.Spider):
    name = 'deepblue'

    df = pd.read_csv('../newsArticlesWithLabels.tsv', sep='\t')
    
    start_urls = df.url

    # start_urls = [ "http://www.foxnews.com/politics/2013/04/03/obamacare-in-trouble-exchange-provision-delayed-as-lawmakers-push-to-repeal/"	
                 # , "http://www.breitbart.com/Big-Government/2013/10/09/Exclusive-Immigration-agents-rip-Bob-Goodlatte-other-Republicans-Democrats-pushing-for-amnesty-in-House"	
                 # , "http://www.cnn.com/2013/06/28/politics/obama-contraceptives/index.html"	
                 # , "http://www.foxnews.com/politics/2013/10/14/amid-cuts-to-federal-courts-judge-suggests-congress-go-to-hell/"	
                 # , "http://www.bbc.co.uk/news/technology-22213379"	
                 # , "http://www.nbcnews.com/technology/microsoft-let-nsa-bypass-encryption-mail-chats-cloud-storage-says-6C10607490"	
                 # , "http://radio.foxnews.com/toddstarnes/top-stories/military-blocks-access-to-southern-baptist-website.html"	
                 # , "http://www.bbc.co.uk/vietnamese/world/2013/08/130812_snowden_father_visit.shtml"	
                 # , "http://www.usatoday.com/story/nation/2013/08/07/jill-kelley-general-david-petraeus-general-john-allen/2625981"
                 # , "http://www.dailykos.com/story/2013/12/02/1259558/-Young-white-dancer-with-her-two-black-instructors-handcuffed-by-Houston-Police-Racism"	
                 # , "http://online.wsj.com/article/SB10001424127887323482504578227152762437278.html"
                 # , "http://www.chicagotribune.com/news/opinion/editorials/ct-illinois-pension-reform-edit-1118-20131118,0,5239008.story" 
                 # ]

    def parse(self, response):
        article = Article(response.url)
        article.download()
        article.parse()
        yield{
            'link': response.url,
            'headline': article.title,
            'publish_date': article.publish_date.strftime('%m-%d-%y'),
            'text': article.text,
            'image': article.top_image}
