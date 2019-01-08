# -*- coding: utf-8 -*-
import scrapy

from quotetutorual.items import QuotetutorualItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
        }
    }

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuotetutorualItem()
            text = quote.css('.text::text').extract_first()
            author = quote.css('.author::text').extract_first()
            tags = quote.css('.tags .tag::text').extract()
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item

        next = response.css('.next a::attr(href)').extract_first()
        url = response.urljoin(next)

        yield scrapy.Request(url=url, callback=self.parse)
