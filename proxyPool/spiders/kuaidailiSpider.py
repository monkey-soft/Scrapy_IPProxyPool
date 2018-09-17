# -*- coding: utf-8 -*-

import logging
import re

from config.config import get_log_config
from proxyPool.model.proxy import Proxy
from proxyPool.spiders.baseSpider import BaseSpider

'''
    快代理爬虫
@Author monkey
@Date 2017-12-18
'''


class KuaidailiSpider(BaseSpider):

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
    def get_proxies(self):

        # 加载 Log 配置
        get_log_config()

        proxy_model_list = []

        print('正在爬取快代理……')

        response = super(KuaidailiSpider, self).get_proxies()

        pattern = re.compile(
            '<tr>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>('
            '.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?</tr>',
            re.S)

        infos = re.findall(pattern, response.text)

        for item in infos:
            try:
                ip = item[0]  # ip
                port = item[1]  # 端口
                anonymity = item[2]  # 匿名度
                http_type = item[3]  # 类型
                area = item[4]  # 地区
                speed = item[5]  # 速度

                print(ip + " | " + port + " | " + anonymity + " | " + http_type + " | " + area + " | " + speed)

                if http_type == 'HTTP' or http_type == 'HTTPS':
                    # print(type.lower() + "://" + ip + ":" + port)
                    proxy = Proxy()
                    proxy.set_ip(ip)
                    proxy.set_port(port)
                    proxy.set_http_type(http_type.lower())
                    proxy.set_anonymity(anonymity)
                    proxy.set_area(area)
                    proxy.set_speed(speed)
                    proxy.set_agent(self.agent)
                    proxy.set_survival_time("")
                    proxy_model_list.append(proxy)
            except Exception as e:
                logging.debug(e)

        logging.debug("抓取 " + self.agent + " 网站共计 " + str(len(proxy_model_list)) + " 个代理")

        return proxy_model_list
