# -*- coding: utf-8 -*-

import logging
from lxml import etree

from lagou.config import getLogConfig
from proxyPool.model.proxyModel import proxyModel
from proxyPool.spiders.baseSpider import baseSpider

'''
    ip181 爬虫
@Author monkey
@Date 2017-12-18
'''
class ip181Spider(baseSpider):

    url = 'http://www.ip181.com/'

    agent = "ip181"

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'http://www.ip181.com/',
        'Content-Type': 'text/html;charset=UTF-8',
        'Cache-Control': 'no-cache',
        'Host': 'www.ip181.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }

    @classmethod
    def getProxies(self):

        # 加载 Log 配置
        getLogConfig()

        proxy_model_list = []

        response = super(ip181Spider, self).getProxies()
        # 这个网站的编码是 gb2312
        response.encoding = 'gb2312'
        selector = etree.HTML(response.text)

        infos = selector.xpath('//div[@class="col-md-12"]/table/tbody/tr')
        for i, info in enumerate(infos):
            try:
                ip = info.xpath('./td[1]/text()')[0]         # ip
                port = info.xpath('./td[2]/text()')[0]       # 端口
                anonymity = info.xpath('./td[3]/text()')[0]  # 匿名度
                type = info.xpath('./td[4]/text()')[0]       # 类型
                speed = info.xpath('./td[5]/text()')[0]      # 速度
                area = info.xpath('./td[6]/text()')[0]       # 地区
                # print(ip + " | " + port + " | " + anonymity + " | " + type + " | " + speed + " | " + area)

                if i == 1:
                    # 把标题过滤掉
                    pass
                else:
                    proxy = proxyModel()
                    proxy.set_ip(ip)
                    proxy.set_port(port)
                    if type == 'HTTP,HTTPS':
                        proxy.set_type('http')
                    else:
                        proxy.set_type(type.lower())
                    proxy.set_anonymity(anonymity)
                    proxy.set_area(area)
                    proxy.set_speed(speed)
                    proxy.set_agent(self.agent)
                    proxy.set_survivalTime("")
                    proxy_model_list.append(proxy)
            except Exception as e:
                logging.debug(e)
        logging.debug("抓取 " + self.agent + " 网站共计 " + str(len(proxy_model_list)) + " 个代理")

        return proxy_model_list