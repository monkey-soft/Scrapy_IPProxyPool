# -*- coding: utf-8 -*-

import logging
import re

from config.config import getLogConfig
from proxyPool.model.ProxyModel import ProxyModel
from proxyPool.spiders.baseSpider import baseSpider

'''
    快代理爬虫
@Author monkey
@Date 2017-12-18
'''
class kuaidailiSpider(baseSpider):

    url = 'http://www.kuaidaili.com/free'

    agent = "快代理"

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'http://www.kuaidaili.com/free',
        'Content-Type': 'text/html;charset=UTF-8',
        'Cache-Control': 'no-cache',
        'Host': 'www.kuaidaili.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }

    @classmethod
    def getProxies(self):

        # 加载 Log 配置
        getLogConfig()

        proxy_model_list = []

        response = super(kuaidailiSpider, self).getProxies()

        pattern = re.compile(
            '<tr>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>('
            '.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?</tr>',
            re.S)

        infos = re.findall(pattern, response.text)

        for item in infos:
            try:
                ip        = item[0]  # ip
                port      = item[1]  # 端口
                anonymity = item[2]  # 匿名度
                type      = item[3]  # 类型
                area      = item[4]  # 地区
                speed     = item[5]  # 速度

                if type == 'HTTP' or type == 'HTTPS':
                    # print(type.lower() + "://" + ip + ":" + port)
                    proxy = ProxyModel()
                    proxy.set_ip(ip)
                    proxy.set_port(port)
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