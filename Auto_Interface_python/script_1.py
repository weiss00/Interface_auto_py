# -*- coding:utf8 -*-

import requests
import json
from urllib3 import encode_multipart_formdata
from Auto_Interface_python.db_utils import dbUtils
from Auto_Interface_python.getConfigParam import ConfigParse
from Auto_Interface_python.ca_excel import excel_cal

class demo1:

    def __init__(self, url):
        # 定一个调度器
        # self.index = 1
        self.excel_1 = excel_cal()
        self.url = url
        self.username = self.excel_1.get_body(2).get("username")
        self.password = self.excel_1.get_body(2).get("password")

        print(self.username + "==" + self.password)
        self.param = {"username": self.username,"password": self.password}
        self.token = self.get_token(param=self.param)
        print("====>", self.token)
        # print(self.token)
        if self.token == None:
            self.register(self.username, self.password, )
            self.token = self.get_token(param=self.param)
            print("<====", self.token)
        self.header_token = {
            "Authorization": "JWT " + self.token
        }

    # 读取excel文件
    '''
    #1
        1. 首先找到excel文件路径
        2. 打开excel文件 formatting_info=True 保持原样式
        3. 读取excel文件获取请求参数， 拼装好参数发送请求，处理返回结果
        4. 对返回的结果进行处理， 将用例执行情况写入excel表中
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

    #  注册操作
    def get_code(self, data):
        data = {"mobile": data}
        status = self.method_type(self.excel_1.get_url(1), self.excel_1.get_method(1), json=data).json()
        host, user, password, port, database = ConfigParse().get_items("Mysql-Database", "host", "user", "password", "port", "database")
        print(host, user, password, port, database)
        if status != "" and status != None:
            try:
                db_conn = dbUtils(host, user, password, int(port), database)
                sql = "select code from users_verifycode where mobile = '{}';".format(data['mobile'])
                code = db_conn.select_sql_one(sql)
                if code != None:
                    return code
                else:
                    raise RuntimeError("查询数据有误，请检查sql语句")
            except:
                raise RuntimeError("连接数据库出错")

    # 注册并登录
    def register(self, mobile, password):
        code = self.get_code(mobile)
        print(code)
        data = {"username":mobile, "password" : password, "code":code}
        resp = self.method_type(self.excel_1.get_url(2), self.excel_1.get_method(2), "POST", json=data).json()
        print(resp)

    #  登陆操作获取token
    def get_token(self, param):
        try:
            print("===========>", param)
            token = self.method_type(self.excel_1.get_url(3), self.excel_1.get_method(3), json=param).json()
            print(token)
            return token['token']
        except:
            return None

    # 获取用户收藏列表
    def get_orders_list(self):
        orders = self.method_type(self.excel_1.get_url(4), self.excel_1.get_method(4), headers=self.header_token)
        print(self.header_token)
        if isinstance(orders.json(), list):
            print(orders.json())
            return orders.json()
        else:
            raise RuntimeError("返回数据有误，请检查返回类型")

    # 上传文件
    #  /messages/   post  form-data
    def upload_file(self):
        file_path = self.excel_1.get_body(5)["file_path"]
        file_name = self.excel_1.get_body(5)["file_name"]
        #  mode  rb 以二进制方式进行读取文件
        with open(file_path, mode="rb") as f:
            file = {
                "file" : (file_name, f.read()),
                "subject": self.excel_1.get_body(5)["subject"],
                "message": self.excel_1.get_body(5)["message"],
                "message_type": self.excel_1.get_body(5)["message_type"]
            }
            encode_data = encode_multipart_formdata(file)
            print(encode_data)
            file_data = encode_data[0]
            headers_form_data = self.header_token.copy()
            headers_form_data["Content-Type"] = encode_data[1]

            upload_img_status =self.method_type(self.excel_1.get_url(5), self.excel_1.get_method(5), data=file_data, headers=headers_form_data).json()
            print(upload_img_status)
            return {"message":"success"}

    # 查看上传文件
    def get_upload_file(self):
        resp = self.method_type(self.excel_1.get_url(6), self.excel_1.get_method(6), headers=self.header_token)
        resp.encoding="UTF-8"
        return json.dumps(resp.json(), indent=2, sort_keys=True, ensure_ascii=False)

    # 请求类型
    def method_type(self, url_key, type, data=None, json=None, headers=None):
        url = self.url + url_key
        if type == "POST":
            return requests.post(url, data=data, json=json, headers=headers)
        else:
            return requests.get(url, data=data, json=json, headers=headers)

if __name__ == '__main__':

    # pass
    url = "http://admin.5istudy.online"
    run = demo1(url)
    run.get_orders_list()
    results = run.upload_file()
    # results = run.get_upload_file()
    print("=======>>>======", results)
    print(type(results))
    excel_cal().check_result(5, results)
    print(results)
