# -*- coding: utf-8 -*-

import logging
import requests
import threadpool
from requests.adapters import HTTPAdapter
from config.config import Validated_url
from config.config import THREADPOOL_NUM
"""
    请求处理工具
@Author monkey
@Date 2017-12-14
"""
# 全局变量
session = requests.Session()
# 经过过滤之后的代理地址
available_proxy_list = []


def do_get(url, headers, *proxies):
    """
    使用 Session 能够跨请求保持某些参数。
    它也会在同一个 Session 实例发出的所有请求之间保持 cookie
    """
    timeout = 3

    session.mount('http://', HTTPAdapter(max_retries=3))
    session.mount('https://', HTTPAdapter(max_retries=3))

    """
    请求代理网站需要设置 Headers, 不需要代理
    验证代理不需要设置 Headers(session 复用 headers), 需要设置代理
    """
    if headers is None:
        if proxies is None:
            response = session.get(url, timeout=timeout)
            return response
        else:
            response = session.get(url, proxies=proxies, timeout=timeout)
            return response
    else:
        if proxies is None:
            response = session.get(url, headers=headers, timeout=timeout)
            return response
        else:
            response = session.get(url, headers=headers, proxies=proxies, timeout=timeout)
            return response


def filter_unavailable_proxy(proxy_list):
    """
    验证代理地址,目的是过滤掉无用的代理
    """

    # 清空列表的数据
    available_proxy_list.clear()

    # 默认 10 个线程数
    pool = threadpool.ThreadPool(THREADPOOL_NUM)
    pool_requests = threadpool.makeRequests(filter_proxy, proxy_list, save_filter_proxy)
    for req in pool_requests:
        pool.putRequest(req)
    pool.wait()

    logging.debug("=====  经过过滤后剩下 " + str(len(available_proxy_list)) + " 个代理  =====")
    return available_proxy_list


def filter_proxy(model):
    """
    线程池中线程验证代理地址
    """

    url = Validated_url

    http_type = model.get_http_type()
    ip = model.get_ip()
    port = model.get_port()

    proxies = {
        'http_type': http_type.lower() + "://" + ip + ":" + str(port)
    }
    # print(proxies['http_type'])
    try:
        # response = requests.get(validated_url, proxies=proxies)
        response = do_get(url, proxies)

        if response.status_code == 200:
            return model
        else:
            return None
    except Exception as e:
        logging.debug(e)


def save_filter_proxy(request, filer_model):
    """
    threadpool 的回调方法
    :param request: 可以访问request.requestID
    :param filer_model:  request执行完的结果
    """
    # print(request.requestID, filer_model)
    if filer_model is not None:
        available_proxy_list.append(filer_model)
