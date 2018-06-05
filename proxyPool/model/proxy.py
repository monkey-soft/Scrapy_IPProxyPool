#!/usr/bin/env python
# coding=utf-8


"""
    IP 代理对象类
@Author monkey
@Date 2017-12-10
"""


class Proxy(object):

    def __init__(self):
        self.__ip = ''
        self.__port = ''
        self.__http_type = ''
        self.__area = ''
        self.__anonymity = ''
        self.__speed = ''
        self.__failed_count = 0
        self.__agent = ''
        self.__survival_time = ''

    def set_ip(self, ip):
        self.__ip = ip

    def get_ip(self):
        return self.__ip

    def set_port(self, port):
        self.__port = port

    def get_port(self):
        return self.__port

    def set_http_type(self, http_type):
        self.__http_type = http_type

    def get_http_type(self):
        return self.__http_type

    def set_area(self, area):
        self.__area = area

    def get_area(self):
        return self.__area

    def set_anonymity(self, anonymity):
        self.__anonymity = anonymity

    def get_anonymity(self):
        return self.__anonymity

    def set_speed(self, speed):
        self.__speed = speed

    def get_speed(self):
        return self.__speed

    def set_failed_count(self, failed_count):
        self.__failed_count = failed_count

    def get_failed_count(self):
        return self.__failed_count

    def set_agent(self, agent):
        self.__agent = agent

    def get_agent(self):
        return self.__agent

    def set_survival_time(self, survival_time):
        self.__survival_time = survival_time

    def get_survival_time(self):
        return self.__survival_time
