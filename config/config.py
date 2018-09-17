# coding=utf-8

import logging
import datetime

"""
    项目配置文件
@Author monkey
@Date 2017-12-18
"""


def get_log_config():
    # 将 requests的日志级别设成 WARNING
    LOG_LEVEL = logging.WARNING
    logging.getLogger("requests").setLevel(LOG_LEVEL)

    # Log 文件名
    LOG_STORE_NAME = 'proxy_{}.txt'.format(
        datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d]/%(levelname)s/  %(message)s',
        datefmt='%Y-%b-%d %H:%M:%S',
        filename='./' + LOG_STORE_NAME,
        filemode='w')


# Mysql 配置信息
# Mysql 数据库建议使用 5.5 或者 5.5 以上的版本
# 根据你的环境修改
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'proxy'        # 数据库名
MYSQL_USER = 'root'         # 数据库用户
MYSQL_PASSWORD = '123456'       # 数据库密码


# 验证代理地址的线程池的总数, 默认是 10
THREADPOOL_NUM = 10

# 验证代理地址的网站, 最好填写你要爬取的网站
Validated_url = 'https://www.baidu.com/'


# 配置代理
IF_USE_PROXY = True
