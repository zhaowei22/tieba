# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from baidu.items import BaiduItem

class TiebaSpider(Spider):
    name = 'tieba'
    # allowed_domains = ['tieba.baidu.com']
    start_urls = ['http://tieba.baidu.com/']

    def start_requests(self):
        url = 'http://tieba.baidu.com/f/index/forumclass'
        # url = 'http://tieba.baidu.com/f/index/forumpark?cn=B%E8%82%A1&ci=0&pcn=%E9%87%91%E8%9E%8D&pci=0&ct=1'
        # url = 'http://tieba.baidu.com/f/index/forumpark?cn=DIY&ci=72&pcn=%E7%94%9F%E6%B4%BB%E5%AE%B6&pci=214&ct=0&rn=20&pn=1'
        yield Request(url, callback=self.get_tag)

    def get_tag(self, response):
        '''
        获取百度贴吧类型，并从类型开始分类抓取
        '''
        print('--------------------------')

        titles = response.xpath('//*[@id="right-sec"]/div/div')
        for title in titles: #循环获大标题
            for tags in title.xpath('ul/li'): #循环获取小标签
                Tb_title = title.xpath('a/text()').extract()[0]
                Tb_tag = tags.xpath('a/text()').extract()[0]
                url = 'http://tieba.baidu.com/' + tags.xpath('a/@href').extract()[0]
                yield Request(url, callback=self.get_tieba, meta={'title':Tb_title,'tag':Tb_tag})

    def get_tieba(self, response):
        '''
        根据分类爬取此类型所有的贴吧信息
        '''
        tiebas = response.xpath('//*[@id="ba_list"]/div')
        for tieba in tiebas:
            item = BaiduItem()
            # 初始化item并进行赋值保存
            try:
                try:
                    item['title'] = response.meta['title']
                except KeyError:
                    item['title'] = 'title invalid!'
                try:
                    item['tag'] = response.meta['tag']
                except:
                    item['tag'] = 'tag invalid!'
                item['name'] = tieba.xpath('a/div/p[@class="ba_name"]/text()').extract()[0]
                item['img'] = tieba.xpath('a/img/@src').extract()[0]
                item['user_num'] = tieba.xpath('a/div/p[@class="ba_num clearfix"]/span[@class="ba_m_num"]/text()').extract()[0]
                item['topic_num'] = tieba.xpath('a/div/p[@class="ba_num clearfix"]/span[@class="ba_p_num"]/text()').extract()[0]
                try:
                    item['description'] = tieba.xpath('a/div/p[@class="ba_desc"]/text()').extract()[0]
                except KeyError:
                    item['description'] = 'not find description!'
                except IndexError:
                    item['description'] = 'not find description!'
                item['url'] = 'http://tieba.baidu.com' + tieba.xpath('a/@href').extract()[0]
            except Exception as e:
                print('------------------------')
                print(e)
            yield item
        next_url = response.xpath('//*[@class="next"]/@href').extract()
        if next_url:
            # 按段是否存在下一页，存在则翻页抓取
            url = 'http://tieba.baidu.com/' + next_url[0]
            # print(url)
            yield Request(url, callback=self.get_tieba, meta={'title':response.meta['title'],'tag':response.meta['tag']})