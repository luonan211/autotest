# -*- coding: utf-8 -*- 
# TIME     : 2020/12/6 16:51
# AUTHOR   : luo nan
# FILE     : test002case.py
# SOFTWARE : PyCharm
# FUNCTION : 参数化

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

url = get_url()
login_xls = GetExcelInfo('userinfo.xls', 'testcase').get_excel_info()
logger.info("测试数据:{}".format(login_xls))
print("测试数据:{}".format(login_xls))
print(f"url:{url}")


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
        logger.info(self.case_name+"测试开始前准备")
        logger.info('案例名称：{}, 接口路径：{}, 请求参数：{}, 请求方法：{} '.format(
            self.case_name, self.path, self.query, self.method))

    def tearDown(self):
        logger.info(self.case_name + "测试结束，输出log完结\n")

    def test01case(self):
        self.checkResult()

    def checkResult(self):
        # 断言
        """
        check test result
        :return:
        """

        urls = url + self.path
        logger.info('接口URL：{}'.format(urls))
        data_dict = urllib.parse.parse_qs(self.query)
        logger.info('接口请求参数data2：{}'.format(data_dict))
        info = Request(self.method, urls, data_dict)
        ss = info.request_all()
        logger.info("接口返回数据：{}".format(type(ss)))

        if self.case_name == 'user_info_v1':
            # 如果case_name是login，说明合法，返回的code应该为200
            self.assertEqual(ss["res_code"], 0)
            logger.info('测试结果：{}'.format(self.assertEqual(ss['res_code'], 0)))
        if self.case_name == 'user_info_v2':
            # 同上
            self.assertEqual(ss["res_code"], 0)
            logger.info('测试结果：{}'.format(self.assertEqual(ss['res_code'], 0)))
        if self.case_name == 'user_info_v3':
            # 同上
            self.assertEqual(ss["res_code"], 0)
            logger.info('测试结果：{}'.format(self.assertEqual(ss['res_code'], 0)))


if __name__ == '__main__':
    unittest.main(verbosity=2)