#!/usr/bin/env python
# coding=utf-8

import pymysql
import logging

from config import config
from config.config import getLogConfig
'''
    IP 代理池处理类
@Author monkey
@Date 2017-12-10
'''
class proxyDBManager(object):

    def __init__(self):

        # 加载 Log 配置
        getLogConfig()

        self.__proxyTable = 'proxy'

        self.conn = pymysql.connect(
            host        = config.MYSQL_HOST,
            db          = config.MYSQL_DBNAME,
            user        = config.MYSQL_USER,
            passwd      = config.MYSQL_PASSWORD,
            charset     = 'utf8',  # 编码要加上，否则可能出现中文乱码问题
            use_unicode = False)

        with self.conn:
            self.cursor = self.conn.cursor()


    '''
    关闭数据库连接
    '''
    def closeConnection(self):
        # 关闭游标连接
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()


    def create_proxy_table(self, ):
        '''
        创建数据库表 proxy 来保存抓取的代理
        '''
        createTableSql = '''
          DROP TABLE IF EXISTS proxy;
          CREATE TABLE {} (
              id INT(9) NOT NULL AUTO_INCREMENT PRIMARY KEY,
              ip VARCHAR(25) NOT NULL,
              port INT(5) NOT NULL,
              type VARCHAR(6) NOT NULL,
              area VARCHAR(200),
              anonymity VARCHAR(25),
              speed VARCHAR(25) DEFAULT '-1',
              failed_count INT(2) DEFAULT 0, 
              agent VARCHAR(25),
              survivalTime VARCHAR(25)
          ) DEFAULT CHARSET=utf8;
        '''.format(self.__proxyTable)

        try:
            self.cursor.execute(createTableSql)
            self.conn.commit()
            logging.debug('===== 成功创建数据库 proxy 表 =====')

        except Exception as e:
            logging.exception('===== 创建数据库 proxy 表出现异常 =====\n %s', e)


    def insert_proxy_table(self, proxymodel):
        '''
        往插入数据库表 proxy 中插入数据
        :param proxymodel: proxyModel 对象
        '''
        insertSql = '''
            insert into
            {} (ip, port, type, area, anonymity, speed, agent, survivalTime)
            values(%s, %s, %s, %s, %s, %s, %s, %s)
        '''.format(self.__proxyTable)


        try:
            data = (proxymodel.get_ip(),
                    proxymodel.get_port(),
                    proxymodel.get_type(),
                    proxymodel.get_area(),
                    proxymodel.get_anonymity(),
                    proxymodel.get_speed(),
                    proxymodel.get_agent(),
                    proxymodel.get_survivalTime()
                    )

            self.cursor.execute(insertSql, data)
            self.conn.commit()
            logging.debug("===== 成功插入 " + proxymodel.get_agent() + " 数据  =====")

        except Exception as e:
            logging.exception('===== mysql insert_proxy exception =====\n %s', e)



    def select_ip_num(self):
        '''
        查询数据库表 proxy 中剩余的 IP 总数
        '''
        selectSql = '''
            select COUNT(1) from {}
        '''.format(self.__proxyTable)

        try:
            self.cursor.execute(selectSql)
            self.conn.commit()

            datas = self.cursor.fetchone()
            logging.debug("===== 数据库中还剩下 " + datas[0] + " IP 地址  =====")

        except Exception as e:
            logging.exception('===== mysql insert_proxy exception =====\n %s', e)


    def select_random_proxy(self):
        '''
        从数据库中随机查询一个 IP 代理地址
        '''
        selectSql = '''
            SELECT * 
            FROM {} AS t1 JOIN (SELECT ROUND(RAND() * (SELECT MAX(id) FROM {})) AS id) AS t2 
            WHERE t1.id >= t2.id 
            ORDER BY t1.id ASC LIMIT 1;
        '''.format(self.__proxyTable, self.__proxyTable)

        try:
            self.cursor.execute(selectSql)
            self.conn.commit()

            data = self.cursor.fetchone()
            # str(data[3], encoding="utf-8") + "://" + str(data[1], encoding="utf-8") + ":" + str(data[2])
            proxy = str(data[3], encoding="utf-8").lower() + "://" + str(data[1], encoding="utf-8") + ":" + str(data[2])
            return proxy

        except Exception as e:
            logging.exception('===== select random_proxy exception =====\n %s', e)


    def plus_proxy_faild_time(self, ip):

        # 对于代理地址连接超时或者失败, 在数据库的失败次数 +1
        updateSql = '''
            update {}
            set failed_count = failed_count + 1
            where ip = {}
        '''.format(self.__proxyTable, ip)

        # 查询当前代理的失败次数
        selectTimeSql = '''
            select failed_count
            from {}
            where ip = {}
        '''.format(self.__proxyTable, ip)

        # 如果失败次数超过 3 次, 删除代理地址
        deleteSql = '''
            delete from {}
            where ip = {}
        '''.format(self.__proxyTable, ip)


        if ip is not None:
            try:
                self.cursor.execute(selectTimeSql)
                self.conn.commit()

                datas = self.cursor.fetchone()
                if datas[0] >= 3 | datas[0] + 1 >= 3:
                    self.cursor.execute(deleteSql)
                    self.conn.commit()
                    logging.debug('===  success to delete {} proxy  ===', ip)
                else:
                    self.cursor.execute(updateSql)
                    self.conn.commit()
                    logging.debug('===  success to update {} proxy  ===', ip)

            except Exception as e:
                logging.exception('=== mysql operation exception ====\n %s', e)
        else:
            logging.error('===  ip is None  ===')