# -*- coding: utf-8 -*-
import scrapy


class IkyuRestaurantSpider(scrapy.Spider):
    name = 'ikyu_restaurant'
    allowed_domains = ['https://restaurant.ikyu.com/']

    start_urls = ['https://restaurant.ikyu.com/104864/?pups=2&pndt=1/']     # '/' must me included :(
    base_url = 'https://restaurant.ikyu.com/104864/?pups=2&pndt=1/'         # '/' must be included  :(
    
    def parse(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        all_items = response.xpath('//li[@class="_1QMibK-"]')

        for item in all_items:

            meal_type               = extract_with_css('div.pYabCMk.span.font.font::text')
            # title                   = extract_with_css()
            # regular_fee             = extract_with_css()
            # course_only             = extract_with_css()
            # course_dessert          = extract_with_css()
            # course_dessert_drink    = extract_with_css()

            yield {
                'meal_type' :               meal_type, 
                # 'title' :                   title, 
                # 'regular_fee' :             regular_fee , 
                # 'course_only' :             course_only, 
                # 'course_dessert' :          course_dessert, 
                # 'course_dessert_drink' :    course_dessert_drink, 
            }
        
