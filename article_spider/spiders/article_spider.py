import scrapy

# REFERENCE THIS: https://docs.scrapy.org/en/latest/intro/tutorial.html#using-spider-arguments
   
class ArticleSpider(scrapy.Spider):
    name = 'article'

    start_urls = ['https://theintercept.com/politics/',
                  'https://theintercept.com/justice/',
                  'https://theintercept.com/national-security/',
                  'https://theintercept.com/world/',
                  'https://theintercept.com/technology/',
                  'https://theintercept.com/environment/',
                  #'https://www.breitbart.com/politics/',
                 ]

    def parse(self, response):
        if 'theintercept' in response.url:
            article_links = response.css('a.data-SpecialPromoData-container').xpath('@href').getall()
        elif 'breitbart' in response.url:
            article_links = response.css('article a::attr(href)').getall()    
            next_page = response.css('nav.pagination a::attr(href)').get()
        
        print(article_links)
        print(next_page)
        yield from response.follow_all(article_links, self.parse_article)
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
    
    def parse_article(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).get(default='').strip()
        def extract_with_xpath_body(query):
            return response.xpath(query).getall()
                
        yield {
            'headline' : extract_with_xpath('//title/text()'),
            'body' : extract_with_xpath_body('//p/text()'),
            'url' : response.url,
            #'author' : 
        }

        # domain = response.url.split('/')[2]
        # switch (domain) {
        #     case 'theintercept.com':
        #         article_links = response.css('a.data-SpecialPromoData-container').xpath('@href').getall()
        #         break 
        #     case 'breitbart.com':           
        # }

# class AuthorSpider(scrapy.Spider):
#     name = 'author'

#     start_urls = ['http://quotes.toscrape.com/']

#     def parse(self, response):
#         author_page_links = response.css('.author + a')
#         yield from response.follow_all(author_page_links, self.parse_author)

#         pagination_links = response.css('li.next a')
#         yield from response.follow_all(pagination_links, self.parse)
    
#     def parse_author(self, response):
#         def extract_with_css(query):
#             return response.css(query).get(default='').strip()

#         yield {
#             'name' : extract_with_css('h3.author-title::text'),
#             'birthdate' : extract_with_css('.author-born-date::text'),
#             'bio' : extract_with_css('.author-description::text'),
#         }


# class QuotesSpider(scrapy.Spider):
#     name = "quotes"

#     start_urls = [
#         'http://quotes.toscrape.com/page/1/',
#     ]

#     def parse(self, response):
#         for quote in response.css('div.quote'):
#             yield {
#                 'text' : quote.css('span.text::text').get(),
#                 'author' : quote.css('small.author::text').get(),
#                 'tags' : quote.css('div.tags a.tag::text').getall(),
#             }

# # Many options re how to handle the link following part
#         yield from response.follow_all(css='ul.pager a', callback=self.parse)

        # Option no. 0.5 [for following multiple links]
        # anchors = response.css('ul.pager a')
        # yield from response.follow_all(anchors, callback=self.parse)
        
        # Option no. 1
        # Note: For <a> elements there is a shortcut: response.follow uses their href attribute automatically. 
        # for a in response.css('ul.pager a'):
        #     yield response.follow(a, callback=self.parse)

        # Option no. 2
        # next_page = response.css('li.next a::attr(href)').get()        
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)

        # Option no. 3
        # next_page = response.css('li.next a::attr(href)').get()        
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

# Orig tutorial code
    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    # def parse(self, response):
    #     page = response.url.split("/")[-2]
    #     filename = f'quotes-{page}.html'
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log(f'Saved file {filename}')

