# -*- coding: utf-8 -*-

import logging
from lxml import etree

from config.config import getLogConfig
from proxyPool.model.ProxyModel import ProxyModel
from proxyPool.spiders.baseSpider import baseSpider
'''
    西刺爬虫
@Author monkey
@Date 2017-12-18
'''
class xiciSpider(baseSpider):

    # url = 'http://www.xicidaili.com/wt/1'    # 国内 HTTP 代理
    url = 'http://www.xicidaili.com/wn/'   # 国内 HTTPS 代理

    agent = "xici"

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        # 'Referer': 'http://www.xicidaili.com/wt/1',
        'Referer': 'http://www.xicidaili.com/wn',
        'Content-Type': 'text/html;charset=UTF-8',
        'Cache-Control': 'no-cache',
        'Host': 'www.xicidaili.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }


    @classmethod
    def getProxies(self):
        # 加载 Log 配置
        getLogConfig()

        proxy_model_list = []

        response = super(xiciSpider, self).getProxies()
        selector = etree.HTML(response.text)

        infos = selector.xpath('//tr[@class="odd"]')

        for i, info in enumerate(infos):
            try:
                ip = info.xpath('./td[2]/text()')[0]            # ip
                port = info.xpath('./td[3]/text()')[0]          # 端口
                anonymity = info.xpath('./td[5]/text()')[0]     # 匿名度
                type = info.xpath('./td[6]/text()')[0]          # 类型
                area = info.xpath('./td[4]/a/text()')[0]        # 地区
                speed = info.xpath('./td[7]/div/@title')[0]     # 速度
                survivalTime = info.xpath('./td[9]/text()')[0]  # 存活时间

                print(ip + " | " + port + " | " + anonymity + " | " + type + " | " + area + " | " + speed + " | " + survivalTime)

                proxy = ProxyModel()
                proxy.set_ip(ip)
                proxy.set_port(port)
                proxy.set_type(type)
                proxy.set_anonymity(anonymity)
                # 处理空地区
                if area is None:
                    proxy.set_area('')
                else:
                    proxy.set_area(area)
                proxy.set_speed(speed)
                proxy.set_agent(self.agent)
                proxy.set_survivalTime(survivalTime)
                proxy_model_list.append(proxy)

            except Exception as e:
                logging.debug(e)

        logging.debug("抓取 " + self.agent + " 网站共计 " + str(len(proxy_model_list)) + " 个代理")

        return proxy_model_list