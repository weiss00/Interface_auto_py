# -*- coding:utf-8 -*-

'''
    配置文件工具类
'''

import configparser

class ConfigParse:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('./config/config.ini')

    def get_items(self, type, *param):
        options = self.config.options(type)
        l = []
        for item in options:
            l.append(self.config.get(type, item))
        param = l
        if len(param) ==1:
            return param[0]
        else:
            return param

