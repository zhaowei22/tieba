# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from baidu.items import BaiduItem

class TiebaSpider(Spider):
    name = 'tieba'
    # allowed_domains = ['tieba.baidu.com']
    start_urls = ['http://tieba.baidu.com/']

    def start_requests(self):
        # url = 'http://tieba.baidu.com/f/index/forumclass'
        # url = 'http://tieba.baidu.com/f/index/forumpark?cn=B%E8%82%A1&ci=0&pcn=%E9%87%91%E8%9E%8D&pci=0&ct=1'
        url = 'http://tieba.baidu.com/f/index/forumpark?cn=DIY&ci=72&pcn=%E7%94%9F%E6%B4%BB%E5%AE%B6&pci=214&ct=0&rn=20&pn=1'
        yield Request(url, callback=self.get_tieba)

    def get_tag(self, response):
        '''
        获取百度贴吧类型，并从类型开始分类抓取
        '''
        print('--------------------------')

        titles = response.xpath('//*[@id="right-sec"]/div/div')
        for title in titles: #循环获大标题
            for j in title.xpath('ul/li'): #循环获取小标签
                # print(title.xpath('a/text()').extract())
                # print(j.xpath('a/text()').extract())
                # print(j.xpath('a/@href').extract()[0])
                url = 'http://tieba.baidu.com/' + j.xpath('a/@href').extract()[0]
                yield Request(url, callback=self.get_tieba)
        # print('xxxxxxxxxxxxxxxxxxxxxxxx')
        # print(response.xpath('//*[@id="right-sec"]/div[2]/div[1]/ul/li[1]/a/text()'))

    def get_tieba(self, response):
        '''
        根据分类爬取此类型所有的贴吧
        '''
        tiebas = response.xpath('//*[@id="ba_list"]/div')
        for tieba in tiebas:

            print(tieba.xpath('a/div/p[@class="ba_name"]/text()').extract())
            print(tieba.xpath('a/div/p[@class="ba_num clearfix"]/span[@class="ba_m_num"]/text()').extract())
            print(tieba.xpath('a/div/p[@class="ba_num clearfix"]/span[@class="ba_p_num"]/text()').extract())
        # url = response.xpath('/html/body/div[3]/div/div/div[2]/div[1]/div[2]/div[4]/div/a[3]/@href').extract()[0]
        next_url = response.xpath('//*[@class="next"]/@href').extract()
        if next_url:
            # 按段是否存在下一页，存在则翻页抓取
            url = 'http://tieba.baidu.com/' + next_url[0]
            # print(url)
            yield Request(url, callback=self.get_tieba)