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
        # print(plans)

        for plan in plans:

            meal_type               = plan.xpath('.//div/div/div/div/span/text()').extract_first()
            title                   = plan.xpath('.//div/div/div/h3/text()').extract_first()
            course_type             = plan.xpath('.//div/div/div/span[1]/text()').extract_first()
            regular_fee             = plan.xpath('.//div/div/div/span[2]/text()').extract_first()

            offer_list = []
            scrap_output = { 'meal_type' : meal_type + ' ', 'title' :  title + ' ', 'course_type' : course_type + ' ', 'regular_fee' : regular_fee + ' ', 'offers' : [] }

            plan_offers = plan.xpath('./div/ul/li[@class="_3S76qhi"]')

            for plan_offer in plan_offers:
                offer_title           = plan_offer.xpath('.//a/div[1]/div[1]/h4/text()').extract_first()
                offer_current_price   = plan_offer.xpath('.//a/div[1]/div[2]/div[2]/span/span[2]/text()').extract_first()
                offer_prev_price      = plan_offer.xpath('.//a/div[1]/div[2]/div[1]/span/text()').extract_first()
                offer_off             = plan_offer.xpath('.//a/div[1]/div[2]/div[2]/span/span[1]/text()').extract_first()
                offer = "title : " + str(offer_title) + ' ' + "current_price : " + ' ' +  str(offer_current_price) + ' ' + "previous_price : " + str(offer_prev_price) + ' ' + "off : " + str(offer_off) + ' '
                scrap_output['offers'].append(offer)
        
            yield scrap_output
        




# class PaypaySpider(scrapy.Spider):
#     name = 'paypay'
#     allowed_domains = ['paypaymall.yahoo.co.jp']
#     start_urls = ['https://paypaymall.yahoo.co.jp/?sc_e=ytc/']

#     

#     def parse(self, response):

#         top_rankings = []
#         famous_stores = []

#         scrap_output = { 
#             'top_rankings': top_rankings, 
#             'famous_stores': famous_stores 
#         }

#         # --------------------------------------------Top Ranking-------------------------------------------------------------------------------------------------
        
#         top_rankings = response.xpath('//body/div/main/div[@class = "Partition top_ranking Partition-separate"]/div[@class = "RankingCarousel"]/amp-list/div[@class="i-amphtml-fill-content i-amphtml-replaced-content"]/amp-carousel/div[@class="i-amphtml-scrollable-carousel-container"]').extract()

#         ranking_categories = response.xpath('.//div[@class="RankingItem amp-carousel-slide amp-scrollable-carousel-slide"]/div')

#         for category in ranking_categories:
#             category_name = category.xpath('./p/a/text()').extract_first().replace(' ', '').replace('\n', '')
#             items = category.xpath('.//div[@class="TinyShelfItem_info"]')

#             ranking_item_list = []

#             ranking_output = {
#                 'category_name' : category_name,
#                 'items' : ranking_item_list
#             }
        
#             for item in items:
#                 brand = item.xpath('./p[@class="TinyShelfItem_brand"]/text()').extract_first()
#                 name = item.xpath('./p[@class="TinyShelfItem_name"]/text()').extract_first()
#                 price = item.xpath('./p[@class="TinyShelfItem_price"]/text()').extract_first()
#                 # yield {
#                 #     'category_name': category_name,
#                 #     'item_brand' : brand,
#                 #     'item_name' : name,
#                 #     'item_price' : price,
#                 # }

#                 ranking_items_out = {
#                     'item_brand' : brand,
#                     'item_name' : name,
#                     'item_price' : price,
#                 }

#                 ranking_output['items'].append(ranking_items_out)
#             scrap_output['top_rankings'].append(ranking_output) 

#         #------------------------------------------Famous Store ----------------------------------------------------------------------------------------------------------
#         famous_stores = response.xpath('//body/div/main/div[@class = "Partition top_famousStore Partition-separate"]/div[@class = "RecommendStoreCarousel"]/amp-list/div[@class="i-amphtml-fill-content i-amphtml-replaced-content"]/amp-carousel/div[@class="i-amphtml-scrollable-carousel-container"]').extract()

#         stores = response.xpath('.//div[@class="RecommendStoreItem amp-carousel-slide amp-scrollable-carousel-slide"]/div')

#         for store in stores:
#             store_name = store.xpath('./p/a/text()').extract_first().replace(' ', '').replace('\n', '')
#             items = store.xpath('.//div[@class="RecommendStoreItem_unit"]/div/a/div')

#             store_item_list = []

#             store_output = {
#                 'store_name' : store_name,
#                 'items' : store_item_list
#             }
        
#             for item in items:
#                 item_title = item.xpath('./p[@class="TinyItem_title"]/text()').extract_first()
#                 price = item.xpath('./p[@class="TinyItem_price"]/text()').extract_first()

#                 # yield {
#                 #     'store_name': store_name,
#                 #     'item_title' : item_title,
#                 #     'item_price' : price,
#                 # }

#                 store_items_out = {
#                     'item_title' : item_title,
#                     'item_price' : price,
#                 }

#                 store_output['items'].append(store_items_out)
#             scrap_output['famous_stores'].append(store_output)

#         yield scrap_output