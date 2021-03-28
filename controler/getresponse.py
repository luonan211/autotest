# -*- coding: utf-8 -*- 
# TIME     : 2020/12/6 16:34
# AUTHOR   : luo nan
# FILE     : getresponse.py
# SOFTWARE : PyCharm
# FUNCTION :

import requests
import json
import logging
from toolkit.time_measure import time_measure

logger = logging.getLogger(__name__)


class Request:
    def __init__(self, method, url, data, headers=None):
        self.method = method
        self.url = url
        self.data = data
        self.headers = headers

    def request_get(self):
        res = requests.get(url=self.url, data=self.data)
        logger.info("请求的response:{}".format(res.json()))
        # print("请求的response:{}".format(res.json()))
        return res.json()

    def request_post(self):
        res = requests.post(url=self.url, data=self.data)
        logger.info("请求的response:{}".format(res.json()))
        # print("请求的response:{}".format(res.json()))
        return res.json()

    @time_measure
    def request_all(self):
        """
        根据实例传入的方法来进行不同的请求，并拿到请求响应的结果
        :return:
        """
        res = ''
        if self.method and self.url:
            if self.method.upper() == 'POST':
                res = self.request_post()
            elif self.method.upper() == 'GET':
                res = self.request_get()
            else:
                logger.info("Excel中的请求方法错误")
        else:
            return 'method或url 不可为空'
        return res


if __name__ == '__main__':
    # urls = 'http://www.baidu.com'
    url = "http://192.168.56.1:50050/user-app/api/v2/get_user_info"
    params = {'city': 'shanghai', 'passwd': 'mima123', 'username': 'luonan'}
    re = Request(url=url, method='get', data=params)
    print(re.request_all())
    print(type(re.request_all()))
