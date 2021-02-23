# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from urllib.parse import urljoin

LUA_SCRIPT = """
function main(splash)
    splash.private_mode_enabled = false
    splash:go(splash.args.url)
    splash:wait(2)
    html = splash:html()
    splash.private_mode_enabled = true
    return html
end
"""


class IkyuRestaurantSpider(scrapy.Spider):
    name = 'ikyu_restaurant'
    allowed_domains = ['restaurant.ikyu.com']

    start_urls = ['https://restaurant.ikyu.com/104864/?pups=2&pndt=1/']     # '/' must me included :(
    base_url = 'https://restaurant.ikyu.com/104864/?pups=2&pndt=1/'         # '/' must be included  :(

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url=url,
                callback=self.parse,
                endpoint='execute',
                args={
                    'wait': 1,
                    "lua_source":LUA_SCRIPT
                }
            )
    
    def parse(self, response):

        plans = response.xpath('//div[@id="plans"]/section/div[3]/ul//li[@class="_1QMibK-"]')

        for plan in plans:

            meal_type               = plan.xpath('.//div/div/div/div/span/text()').extract_first()
            title                   = plan.xpath('.//div/div/div/h3/text()').extract_first()
            course_type             = plan.xpath('.//div/div/div/span[1]/text()').extract_first()
            regular_fee             = plan.xpath('.//div/div/div/span[2]/text()').extract_first()

            offer_list = []
            scrap_output = { 'meal_type' : str(meal_type) + ' ', 'title' :  str(title) + ' ', 'course_type' : str(course_type) + ' ', 'regular_fee' : str(regular_fee) + ' ', 'offers' : offer_list }

            plan_offers = plan.xpath('./div/ul/li[@class="_3S76qhi"]')

            for plan_offer in plan_offers:
                offer_title               = plan_offer.xpath('.//a/div[1]/div[1]/h4/text()').extract_first()
                try:
                    offer_current_price   = plan_offer.xpath('.//a/div[1]/div[2]/div[@class="_2U8wNG5"]/span[@class="_1CPmbeh"]/span[@class="_2Xel14i"]/text()').extract_first()
                except:
                    offer_current_price   = plan_offer.xpath('.//a/div[1]/div[2]/div[@class="_2U8wNG5"]/span[@class="_1CPmbeh"]/span[@class="_2Xel14i"]/text()').extract_first()
                offer_prev_price          = plan_offer.xpath('.//a/div[1]/div[2]/div[1]/span[@class="_1gV6Q0h"]/text()').extract_first()
                offer_off                 = plan_offer.xpath('.//a/div[1]/div[2]/div[2]/span/span[@class="sAkFuj_"]/text()').extract_first()
                offer = "title : " + str(offer_title) + ' ' + "current_price : " + ' ' +  str(offer_current_price) + ' ' + "previous_price : " + str(offer_prev_price) + ' ' + "off : " + str(offer_off) + ' '
                scrap_output['offers'].append(offer)

            yield scrap_output
