# -*- coding: utf-8 -*-

'''
    请求处理工具
@Author monkey
@Date 2017-12-14
'''
import logging
import requests
from requests import Response
from requests.adapters import HTTPAdapter

from proxyPool.model.proxyModel import proxyModel

def do_get(url, headers):
    '''
    使用 Session 能够跨请求保持某些参数。
    它也会在同一个 Session 实例发出的所有请求之间保持 cookie
    '''
    timeout = 3

    proxies = {
        # 如果你使用的网络需要代理
    }

    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=5))
    session.mount('https://', HTTPAdapter(max_retries=5))

    if headers is None:
        response = session.get(url, proxies=proxies, timeout=timeout)
        return response
    else:
        response = session.get(url, headers=headers, proxies=proxies, timeout=timeout)
        return response


def filter_unavailable_proxy(proxymodel_list):
    '''
    验证代理地址,目的是过滤掉无用的代理
    '''
    # validatedUrl = 'http://httpbin.org/ip'
    # 填写你需要爬取网站的地址
    validatedUrl = 'https://www.baidu.com/'

    timeout = 3

    proxies = {}

    available_proxy_list = []
    for model in proxymodel_list:
        type = model.get_type()
        ip = model.get_ip()
        port = model.get_port()

        proxies[type] = type.lower() + "://" + ip + ":" + str(port)
        # print(proxies[type])
        try:
            response = requests.get(validatedUrl, proxies=proxies, timeout=timeout)
            if response.status_code == 200:
                available_proxy_list.append(model)
            else:
                pass
        except Exception as e:
            logging.debug(e)

    logging.debug("=====  经过过滤后剩下 " + str(len(available_proxy_list)) + " 个代理  =====")
    return available_proxy_list