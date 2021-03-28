# -*- coding: utf-8 -*- 
# TIME     : 2020/12/6 17:36
# AUTHOR   : luo nan
# FILE     : test003case.py
# SOFTWARE : PyCharm
# FUNCTION :

import json
import unittest
from controler.getresponse import Request
import paramunittest
from controler.getenvconfig import get_url
import urllib.parse
from data.op_xls import GetExcelInfo
import logging
from sys import argv
# from controler.logger import MyLog

logger = logging.getLogger(__name__)

# logger = MyLog()

login_xls = GetExcelInfo('userinfo.xls', 'testcase').get_excel_info()
logger.info("测试数据:{}".format(login_xls))


@paramunittest.parametrized(*login_xls)
class TestUserInfo(unittest.TestCase):
    def setParameters(self, case_name, path, query, method):
        """
        set params
        :param case_name:
        :param path
        :param query
        :param method
        :return:
        """
        self.case_name = str(case_name)
        self.path = str(path)
        self.query = str(query)
        self.method = str(method)

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    @classmethod
    def setUpClass(cls):
        logger.info('\n=======测试类{}开始=========='.format(argv[0]))

    @classmethod
    def tearDownClass(cls):
        logger.info('\n======测试类{}结束======'.format(argv[0]))

    def setUp(self):
        logger.info(self.case_name+"测试开始前准备".center(60, '*'))

    def tearDown(self):
        logger.info("*******************测试结束，输出log完结******************\n\n")

    def test01case(self):
        url = get_url()
        urls = url + self.path
        logger.info(f"urls :{urls}")
        logger.info(f"请求方法：{self.method}")
        logger.info(f'请求参数：{self.query}')
        r = Request(method=self.method, url=urls, data=self.query).request_all()
        res = str(r)
        self.assertIn("name", res, msg="结果验证")


if __name__ == '__main__':
    unittest.main(verbosity=2)