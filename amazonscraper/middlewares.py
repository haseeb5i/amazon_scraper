# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals, exceptions
import time


class AmazonscraperSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class AmazonscraperDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def response_is_captcha(self, response):
        # This string is in the response if a captcha is detected.
        return response.status == 200 and ("api-services-support@amazon.com" in response.text)

    def amazon_is_sorry(self, response):
        if not response.css("h2"):
            return False
        h2 = response.css("h2")
        return any(["we're sorry!" in h.get().lower() for h in h2])

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        CAPTCHA_SLEEP_TIME = 5
        print("WORKING!!!")
        if self.amazon_is_sorry(response):
            # This is raised if a page is not found, specifically a seller.
            # this still returns a response code of 200, so Scrapy doesn't detect it.
            spider.logger.warning(
                'Amazon said "We\'re sorry!" for %s', response.url)
            on_amazon_sorry = getattr(spider, "on_amazon_sorry", None)
            if on_amazon_sorry:
                on_amazon_sorry(self, request, response)
            raise exceptions.IgnoreRequest()
        if self.response_is_captcha(response):
            # Same with captchas. But in this instance we want to ask the throttle
            # to slow down (although, the damage has probably already been done).
            # To tell scrapy to slow down, we throw an error 403.
            spider.logger.warning(
                "Encountered captcha; sleeping for %d seconds, adding '%s' to queue",
                CAPTCHA_SLEEP_TIME,
                request.url,
            )
            time.sleep(CAPTCHA_SLEEP_TIME)
            # I'm sure there's a better way to do this. This is just a quick and
            # dirty method.
            setattr(spider, "__invoke_shaker", True)
            response.status = 403
            spider.start_urls.append(request.url)
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
