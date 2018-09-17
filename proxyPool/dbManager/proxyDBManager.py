#!/usr/bin/env python
# coding=utf-8

import pymysql
import logging

from config import config
from config.config import get_log_config
"""
    IP 代理池处理类
@Author monkey
@Date 2017-12-10
"""


class ProxyDBManager(object):

    def __init__(self):

        # 加载 Log 配置
        get_log_config()

        self.__proxy_table = 'proxy'

        self.conn = pymysql.connect(
            host=config.MYSQL_HOST,
            db=config.MYSQL_DBNAME,
            user=config.MYSQL_USER,
            passwd=config.MYSQL_PASSWORD,
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            use_unicode=False)

        with self.conn:
            self.cursor = self.conn.cursor()

    """
    关闭数据库连接
    """
    def close_connection(self):
        # 关闭游标连接
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()

    def create_proxy_table(self, ):
        """  创建数据库表 proxy 来保存抓取的代理  """
        create_table_sql = (
          # "DROP TABLE IF EXISTS {};"
          # "CREATE TABLE {} ("
          "CREATE TABLE IF NOT EXISTS {} ("
          "`id` INT(9) NOT NULL AUTO_INCREMENT,"
          "`ip` BIGINT(10) NOT NULL,"
          "`port` INT(5) NOT NULL,"
          "`http_type` VARCHAR(6) NOT NULL,"
          "`area` VARCHAR(200),"
          "`anonymity` VARCHAR(25),"
          "`speed` VARCHAR(25) DEFAULT '-1',"
          "`failed_count` INT(2) DEFAULT 0,"
          "`agent` VARCHAR(25),"
          "`survival_time` VARCHAR(25),"
          "PRIMARY KEY(id)"
          ") ENGINE=InnoDB DEFAULT CHARSET=utf8".format(self.__proxy_table, self.__proxy_table)
        )

        try:
            self.cursor.execute(create_table_sql)
            self.conn.commit()
            logging.debug('===== 成功创建数据库 proxy 表 =====')

        except Exception as e:
            logging.exception('===== 创建数据库 proxy 表出现异常 =====\n %s', e)

    def drop_proxy_table(self):
        """  删除数据库表 proxy  """
        delete_sql = "DROP TABLE IF EXISTS {}".format(self.__proxy_table)
        try:
            self.cursor.execute(delete_sql)
            self.conn.commit()
            logging.debug("===== 成功删除 " + self.__proxy_table + " 表  =====")

        except Exception as e:
            logging.exception('===== mysql delete data exception =====\n %s', e)

    def insert_proxy_table(self, proxy):
        """
        往插入数据库表 proxy 中插入数据
        :param proxy: proxyModel 对象
        """
        insert_sql = (
            "insert into "
            "{} (ip, port, http_type, area, anonymity, speed, agent, survival_time) "
            "values(INET_ATON(%s), %s, %s, %s, %s, %s, %s, %s)".format(self.__proxy_table))

        try:
            data = (proxy.get_ip(),
                    proxy.get_port(),
                    proxy.get_http_type(),
                    proxy.get_area(),
                    proxy.get_anonymity(),
                    proxy.get_speed(),
                    proxy.get_agent(),
                    proxy.get_survival_time()
                    )

            self.cursor.execute(insert_sql, data)
            self.conn.commit()
            logging.debug("===== 成功插入 " + proxy.get_agent() + " 数据  =====")

        except Exception as e:
            logging.exception('===== mysql insert_proxy exception =====\n %s', e)

    def select_ip_num(self):
        """ 查询数据库表 proxy 中剩余的 IP 总数 """
        select_sql = "select COUNT(1) from {}".format(self.__proxy_table)

        try:
            self.cursor.execute(select_sql)
            self.conn.commit()

            datas = self.cursor.fetchone()
            logging.debug("===== 数据库中还剩下 " + datas[0] + " IP 地址  =====")

        except Exception as e:
            logging.exception('===== mysql insert_proxy exception =====\n %s', e)

    def select_random_proxy(self):
        """ 从数据库中随机查询一个 IP 代理地址 """
        select_sql = (
            "SELECT INET_NTOA(ip), http_type, port "
            "FROM {} AS t1 JOIN (SELECT ROUND(RAND() * (SELECT MAX(id) FROM {})) AS id) AS t2 "
            "WHERE t1.id >= t2.id "
            "ORDER BY t1.id ASC LIMIT 1;".format(self.__proxy_table, self.__proxy_table))

        try:
            self.cursor.execute(select_sql)
            self.conn.commit()

            data = self.cursor.fetchone()
            # str(data[1], encoding="utf-8") + "://" + str(data[0], encoding="utf-8") + ":" + str(data[2])
            proxy = str(data[1], encoding="utf-8").lower() + "://" + str(data[0], encoding="utf-8") + ":" + str(data[2])
            return proxy

        except Exception as e:
            logging.exception('===== select random_proxy exception =====\n %s', e)

    def plus_proxy_faild_time(self, ip):

        """ 对于代理地址连接超时或者失败, 在数据库的失败次数 +1 """
        update_sql = (
            "update {} "
            "set failed_count = failed_count + 1 "
            "where ip = INET_ATON(%s)".format(self.__proxy_table))

        """ 查询当前代理的失败次数 """
        select_time_sql = (
            "select failed_count "
            "from {} "
            "where ip = INET_ATON(%s)".format(self.__proxy_table))

        """ 如果失败次数超过 3 次, 删除代理地址 """
        delete_sql = (
            "delete from {} "
            "where ip = INET_ATON(%s)".format(self.__proxy_table))

        if ip is not None:
            try:
                self.cursor.execute(select_time_sql, ip)
                self.conn.commit()

                datas = self.cursor.fetchone()

                if datas[0] >= 3 | datas[0] + 1 >= 3:
                    # print('deleteSql  ===== ', deleteSql)
                    self.cursor.execute(delete_sql, ip)
                    self.conn.commit()
                    logging.debug('===  success to delete %s proxy  ===', ip)
                else:
                    # print('updateSql  ===== ', updateSql)
                    self.cursor.execute(update_sql, ip)
                    self.conn.commit()
                    logging.debug('===  success to update %s proxy  ===', ip)

            except Exception as e:
                logging.exception('=== mysql operation exception ====\n %s', e)
        else:
            logging.error('===  ip is None  ===')
