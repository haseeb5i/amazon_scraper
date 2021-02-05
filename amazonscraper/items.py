# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonscraperItem(scrapy.Item):
    title = scrapy.Field()
    vendor = scrapy.Field()
    rating = scrapy.Field()
    tags = scrapy.Field()
    compare_price = scrapy.Field()
    variant_price = scrapy.Field()
    option1_value = scrapy.Field()
    instock = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    description = scrapy.Field()
    p_link = scrapy.Field()
