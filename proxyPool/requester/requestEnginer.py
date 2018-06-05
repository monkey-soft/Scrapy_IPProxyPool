# -*- coding: utf-8 -*-

import logging
import requests
from requests.adapters import HTTPAdapter


"""
    请求处理工具
@Author monkey
@Date 2017-12-14
"""


def do_get(url, headers):
    """
    使用 Session 能够跨请求保持某些参数。
    它也会在同一个 Session 实例发出的所有请求之间保持 cookie
    """
    timeout = 3

    proxies = {
        # 如果你使用的网络需要代理
    }

    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=3))
    session.mount('https://', HTTPAdapter(max_retries=3))

    if headers is None:
        response = session.get(url, proxies=proxies, timeout=timeout)
        return response
    else:
        response = session.get(url, headers=headers, proxies=proxies, timeout=timeout)
        return response


def filter_unavailable_proxy(proxy_list):
    """
    验证代理地址,目的是过滤掉无用的代理
    """
    # validated_url = 'http://httpbin.org/ip'
    # 填写你需要爬取网站的地址
    validated_url = 'https://www.baidu.com/'

    timeout = 3

    proxies = {}

    available_proxy_list = []
    for model in proxy_list:
        http_type = model.get_http_type()
        ip = model.get_ip()
        port = model.get_port()

        proxies[http_type] = http_type.lower() + "://" + ip + ":" + str(port)
        # print(proxies[type])
        try:
            response = requests.get(validated_url, proxies=proxies, timeout=timeout)
            if response.status_code == 200:
                available_proxy_list.append(model)
            else:
                pass
        except Exception as e:
            logging.debug(e)

    logging.debug("=====  经过过滤后剩下 " + str(len(available_proxy_list)) + " 个代理  =====")
    return available_proxy_list
