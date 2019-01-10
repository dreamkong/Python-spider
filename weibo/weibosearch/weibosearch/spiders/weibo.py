# -*- coding: utf-8 -*-
import re

from scrapy import Spider, FormRequest, Request


class WeiboSpider(Spider):
    name = 'weibo'
    allowed_domains = ['weibo.cn']
    search_url = 'http://weibo.cn/search/mblog'
    max_page = 100

    def start_requests(self):
        keyword = '000001'
        url = '{url}?keyword={keyword}'.format(url=self.search_url, keyword=keyword)
        # for page in range(self.max_page + 1):
        for page in range(1):
            data = {
                'mp': str(self.max_page),
                'page': str(page)
            }
            yield FormRequest(url=url, callback=self.parse_index, formdata=data, dont_filter=True)

    def parse_index(self, response):
        weibos = response.css('div[id*="M_"]')
        for weibo in weibos:
            is_forward = bool(weibo.css('.cmt').extract_first())
            detail_url = weibo.css('.cc::attr(href)').extract_first()
            print(detail_url)
            yield Request(detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        id = re.search('comment\/(.*?)\?', response.url).group(1)
        url = response.url
        text = ''.join(response.css('.ctt::text').extract())
        # print(id, url, text)
        forward_count = response.css('div["转发"]')
        print(forward_count)
