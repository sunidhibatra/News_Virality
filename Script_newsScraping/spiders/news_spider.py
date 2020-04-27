# -*- coding: utf-8 -*-
import scrapy
from ..items import NewsScrapeItem
from scrapy.utils.response import open_in_browser
#import nltk
#from newspaper import Article

class NewsSpiderSpider(scrapy.Spider):
    name = 'news_spider'
    page_number = 2
    start_urls = ['https://www.thehindu.com/news/national/?page=1']

    def parse(self, response):
    	#print(type(response))
    	#open_in_browser(response)
    	open_page = response.css('#section_3 h3 a').css('::attr(href)').extract()
    	for x in open_page:
    		yield scrapy.Request(x,callback = self.find_title)

    def find_title(self,response):
    	items = NewsScrapeItem()
    	title = response.css('h1.title').css('::text').extract()
    	new_title = []
    	for ele in title:
    		new_title.append(ele.strip())
    	text = response.css('.intro+ div p').css('::text').extract()
    	new_text = []
    	for ele in text:
    		new_text.append(ele.strip())
    	place = response.css('.ksl-time-stamp:nth-child(1)').css('::text').extract()
    	place = place[0].strip()
    	date_and_time = response.css('.ksl-time-stamp none').css('::text').extract()
    	date_and_time = date_and_time[0].strip()
    	items['title'] = new_title
    	items['text'] = new_text
    	items['place'] = place
    	items['date_and_time'] = date_and_time
    	yield items

    	next_page = 'https://www.thehindu.com/news/national/?page=' + str(NewsSpiderSpider.page_number)
    	if NewsSpiderSpider.page_number <= 10:
    		NewsSpiderSpider.page_number += 1
    		yield response.follow(next_page,callback = self.parse)

 