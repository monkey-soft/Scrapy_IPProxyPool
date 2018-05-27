#!/usr/bin/env python
# coding=utf-8


'''
    IP 代理对象类
@Author monkey
@Date 2017-12-10
'''
class ProxyModel(object):

    __failed_count = 0
    __speed = -1

    def __init__(self):
        pass

    def set_ip(self, ip):
        self.__ip = ip

    def get_ip(self):
        return self.__ip

    def set_port(self, port):
        self.__port = port

    def get_port(self):
        return self.__port

    def set_type(self, type):
        self.__type = type

    def get_type(self):
        return self.__type

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

    def set_survivalTime(self, survivalTime):
        self.__survivalTime = survivalTime

    def get_survivalTime(self):
        return self.__survivalTime
