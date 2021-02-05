# -*- coding: utf-8 -*-
import scrapy

from ..items import AmazonscraperItem


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    # allowed_domains = ['https://www.amazon.com']

    def __init__(self, pages=1, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)
        self.no_of_pages = int(pages)

    def get_urls(self, filepath):
        urls_list = []
        with open(filepath, "r") as f:
            for url in f.readlines():
                if len(url.strip()) != 0:
                    urls_list.append(url.strip())
        return urls_list

    def start_requests(self):
        # starting urls for scraping
        urls = self.get_urls("urls_list.txt")

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        """
        Get links of all items on the page, generate a request corresponding to each item.
        Get link of next page and genrate request for that.
        """
        self.no_of_pages -= 1
        # gets links of all items from the result page
        search_items = response.xpath(
            "//a[@class='a-link-normal a-text-normal']").xpath("@href").getall()

        print("Items got: ", len(search_items))

        for item_url in search_items:
            yield response.follow(url=item_url, callback=self.parse_item)

        if(self.no_of_pages > 0):
            next_page_url = response.xpath(
                "//ul[@class='a-pagination']/li[@class='a-last']/a").xpath("@href").get()
            yield response.follow(url=next_page_url, callback=self.parse_page)

    def parse_item(self, response):
        """
        Parse the response of individual items for certain results."
        """
        properties = AmazonscraperItem()

        # amazon_availibility = response.css(
        #     "div div#availability span span::text").getall()[2].strip()
        available = not response.css(
            "div div#availability span span a").get()

        # only get available products
        if available:
            tags = response.css("div#wayfinding-breadcrumbs_feature_div ul li")
            tag_items = []
            for tag in tags:
                try:
                    tmp = tag.css("a::text").get().strip()
                    tag_items.append(tmp)
                except:
                    pass
            properties["tags"] = tag_items

            properties["title"] = response.css(
                "h1[id=title] span::text").get().strip()

            p_overview = response.css("div#productOverview_feature_div tr")
            for feature in p_overview:
                if feature.css("td.a-span3 span::text").get() == "Brand":
                    properties["vendor"] = feature.css(
                        "td.a-span9 span::text").get()

            properties["rating"] = response.xpath("//div[@id='averageCustomerReviews_feature_div']").xpath(
                "//span[@class='a-icon-alt']//text()").get()

            properties["compare_price"] = response.css(
                "div#unifiedPrice_feature_div span.priceBlockStrikePriceString::text").get() or "not available"

            properties["variant_price"] = response.css(
                "div#unifiedPrice_feature_div span#priceblock_ourprice::text").get()

            try:
                # response.css("div#twister_feature_div li.swatchSelect") # current selected variant
                variant_prop_name = response.css(
                    "div#twister_feature_div div.a-row label::text").get().strip()
                variant_prop_value = response.css(
                    "div#twister_feature_div div.a-row span::text").get().strip()
                properties["option1_value"] = variant_prop_name + \
                    ' ' + variant_prop_value
            except:
                properties["option1_value"] = "default"

            stock_status = response.css(
                "div div#availability span::text").get() or ""
            if stock_status.strip() == "In Stock.":
                properties["instock"] = stock_status.strip()
            else:
                properties["instock"] = "Out of Stock."

            properties["image_urls"] = response.css("img#landingImage::attr(data-old-hires)").get(
            ) or response.xpath("//img[@id='imgBlkFront']/@src").get()
            properties["image_urls"] = [properties["image_urls"]]

            description_raw = response.css("div[id=feature-bullets] ul li")
            description = []
            for point in description_raw:
                description.append(point.css("::text").get().strip())
            properties["description"] = [d for d in description if len(d) != 0]

            properties["p_link"] = response.url

            yield properties
