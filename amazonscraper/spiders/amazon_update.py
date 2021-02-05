# -*- coding: utf-8 -*-
import csv

import scrapy


class AmazonUpdateSpider(scrapy.Spider):
    name = 'amazon-update'
    # allowed_domains = ['https://www.amazon.com']

    def __init__(self, ifile=None, *args, **kwargs):
        super(AmazonUpdateSpider, self).__init__(*args, **kwargs)
        urls = []
        with open(ifile, newline='', encoding='utf-8') as csv_file:
            dict_reader = csv.DictReader(csv_file, delimiter=',')
            for row in dict_reader:
                urls.append(row['p_link'])
        self.start_urls = urls

    def parse(self, response):
        stock_status = response.css(
            "div div#availability span::text").get() or ""
        if stock_status.strip() == "In Stock.":
            instock = stock_status.strip()
        else:
            instock = "Out of Stock."

        variant_price = response.css(
            "div#unifiedPrice_feature_div span#priceblock_ourprice::text").get()

        yield {
            'instock': instock,
            'price': variant_price,
        }
