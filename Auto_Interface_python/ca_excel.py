# -*- coding:utf-8 -*-

import time
import xlrd
import json
from xlutils.copy import copy
from Auto_Interface_python.getConfigParam import ConfigParse

class excel_cal:

    def __init__(self):
        excel_path = ConfigParse().get_items("Excel-Config", "excel-path")
        print(excel_path)
        self.workBook = xlrd.open_workbook(excel_path, formatting_info=True)
        self.work_sheet = self.workBook.sheet_by_index(0)

    def get_method(self, index):
        try:
            method = self.work_sheet.cell(index, 2).value
            return method
        except:
            print("获取请求方式出现错误，检查excel文档写法是否规范")
            return None

    def get_url(self, index):
        try:
            url = self.work_sheet.cell(index, 3).value
            return url
        except:
            print("获取接口出现错误，检查excel文档写法是否规范")
            return None

    '''
        return :    list
    '''
    def get_body(self, index):
        data = self.work_sheet.cell(index, 4).value
        data = json.loads(data)
        return data

    def check_result(self, index, rest1):
        rest2 = self.work_sheet.cell(index, 5).value
        rest2 = json.loads(rest2)
        if rest2 == rest1:
            self.write_result(index, "pass")
        else:
            self.write_result(index, "fail")

    '''
    #2  测试结果写入
        # 文件不存在 -- 新建excel -- 写 -- xlwt
        # 文件本身存在 -- 另存写新excel -- xlutils
        from xlutils.copy import copy   
        #1 - 拷贝excel对象
        newWorkBook = copy(workBook)
        #2 - 取拷贝的excel的sheet---sheet 下标
        newSheet = newWorkBook.get_sheet(1)
        #3 - 写入数据 -- info -- newSheet.write(行下标，列下标，内容)
        newSheet.write(1, 9, info)
        #4 - 保存excel对象
        newWorkBook.save(r'../data/res.xls')
    '''
    def write_result(self, index, word):
        newWorkBook = copy(self.workBook)
        newSheet = newWorkBook.get_sheet(0)
        newSheet.write(index, 6, word)
        # newSheet.write()
        time_format = time.strftime('%Y%m%d-%H%M%S', time.localtime())
        newWorkBook.save(rf'./data/results-{time_format}.xls')

# if __name__ == '__main__':
#     e = excel_cal()
#     url = e.get_url(1)
#     print(url)
#     method = e.get_method(1)
#     print(method)