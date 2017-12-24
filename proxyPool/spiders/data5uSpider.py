# -*- coding: utf-8 -*-

import logging
from lxml import etree

from lagou.config import getLogConfig
from proxyPool.model.proxyModel import proxyModel
from proxyPool.spiders.baseSpider import baseSpider

'''
    无忧代理(data5u) 爬虫
@Author monkey
@Date 2017-12-18
'''
class data5uSpider(baseSpider):

    url = 'http://www.data5u.com/free/gngn/index.shtml'

    agent = "data5u"

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'http://www.data5u.com/free/gngn/index.shtml',
        'Content-Type': 'text/html;charset=UTF-8',
        'Cache-Control': 'no-cache',
        'Host': 'www.data5u.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }


    @classmethod
    def getProxies(self):
        # 加载 Log 配置
        getLogConfig()

        proxy_model_list = []

        response = super(data5uSpider, self).getProxies()
        selector = etree.HTML(response.text)

        infos = selector.xpath('//ul[@class="l2"]')

        for i, info in enumerate(infos):
            try:
                ip = info.xpath('//ul[@class="l2"]/span[1]/li/text()')[i]               # ip
                port = info.xpath('//ul[@class="l2"]/span[2]/li/text()')[i]             # 端口
                anonymity = info.xpath('//ul[@class="l2"]/span[3]/li/a/text()')[i]      # 匿名度
                type = info.xpath('//ul[@class="l2"]/span[4]/li/a/text()')[i]           # 类型
                area = info.xpath('//ul[@class="l2"]/span[6]/li/a[1]/text()')[i]        # 地区, 省
                area = area + info.xpath('//ul[@class="l2"]/span[6]/li/a[2]/text()')[i] # 地区, 市
                speed = info.xpath('//ul[@class="l2"]/span[8]/li/text()')[i]            # 速度

                if type == 'http' or type == 'https':
                    # print(type + "://" + ip + ":" + port)
                    proxy = proxyModel()
                    proxy.set_ip(ip)
                    proxy.set_port(port)
                    proxy.set_type(type)
                    proxy.set_anonymity(anonymity)
                    proxy.set_area(area)
                    proxy.set_speed(speed)
                    proxy.set_agent(self.agent)
                    proxy.set_survivalTime("")
                    proxy_model_list.append(proxy)
                else:
                    pass
            except Exception as e:
                logging.debug(e)

        logging.debug("抓取 " + self.agent + " 网站共计 " + str(len(proxy_model_list)) + " 个代理")

        return proxy_model_list