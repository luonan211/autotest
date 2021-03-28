# -*- coding: utf-8 -*- 
# TIME     : 2020/11/30 21:45
# AUTHOR   : luo nan
# FILE     : runall.py
# SOFTWARE : PyCharm
# FUNCTION :

import os
import yaml
import logging
from logging.config import dictConfig
from data.op_mysql import execute_query
import controler.HTMLTestRunner as HTMLTestRunner
import basepath
import unittest
# import readConfig
from controler.getenvconfig import get_email_config
from controler.sendemail import SendEmail
# from apscheduler.schedulers.blocking import BlockingScheduler
# import pythoncom

BASE_PATH = basepath.get_base_path()
print(BASE_PATH)
LOGGING_CONFIG = os.path.join(BASE_PATH, "config", "logging.yaml")
print(LOGGING_CONFIG)


def setup_logging(default_path=LOGGING_CONFIG, default_level=logging.INFO, env_key="LOG_CFG"):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "r", encoding='utf-8') as f:
            config = yaml.safe_load(f)
            print(config)
            dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


setup_logging()
logger = logging.getLogger(__name__)

# send_mail = send_email()
send_mail = SendEmail()
path = basepath.get_base_path()
report_path = os.path.join(path, 'report')
on_off = get_email_config().get('on_off')
logger.info(report_path)


class AllTest:

    global resultPath
    # result/report.html
    resultPath = os.path.join(report_path, "report.html")

    def __init__(self):
        # 初始化一些参数和数据
        # 配置执行哪些测试文件的配置文件路径
        self.caseListFile = os.path.join(path, "caselist.txt")
        # 真正的测试断言文件路径
        self.caseFile = os.path.join(path, "testCase")
        self.caseList = []
        logger.info('resultPath '+resultPath)
        logger.info('caseListFile '+self.caseListFile)
        logger.info('caseList '+str(self.caseList))
        logger.info('caseFile ' + str(self.caseFile))

    def set_case_list(self):
        """
        读取caselist.txt文件中的用例名称，并添加到caselist元素组
        :return:
        """
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            # 如果data非空且不以#开头
            if data != '' and not data.startswith("#"):
                # 读取每行数据会将换行转换为\n，去掉每行数据中的\n
                self.caseList.append(data.replace("\n", ""))
        fb.close()

    def set_case_suite(self):
        """

        :return:
        """
        # 通过set_case_list()拿到caselist元素组
        self.set_case_list()
        test_suite = unittest.TestSuite()
        suite_module = []
        # 从caselist元素组中循环取出case
        for case in self.caseList:
            # 通过split函数来将aaa/bbb分割字符串，-1取后面，0取前面
            case_name = case.split("/")[-1]
            logger.info(case_name+".py")
            # 批量加载用例，第一个参数为用例存放路径，第一个参数为路径文件名
            discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case_name + '.py', top_level_dir=None)
            # 将discover存入suite_module元素组
            suite_module.append(discover)
            logger.info('suite_module:'+str(suite_module))
            # 判断suite_module元素组是否存在元素
        if len(suite_module) > 0:
            # 如果存在，循环取出元素组内容，命名为suite
            for suite in suite_module:
                # 从discover中取出test_name，使用addTest添加到测试集
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            print('else:')
            return None
        # 返回测试集
        return test_suite

    def run(self):
        """
        run test
        :return:
        """
        try:
            # 调用set_case_suite获取test_suite
            suit = self.set_case_suite()
            print(f"当前测试suit{suit}")
            # 判断test_suite是否为空
            if suit is not None:
                print(resultPath)
                # fp = open(resultPath, 'wb')  # a bytes-like object is required, not 'str' 去掉B
                # fp = open(resultPath, 'w', encoding='utf-8')
                # 调用HTMLTestRunner
                with open(resultPath, 'w') as fp:
                    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                                           title='测试报告',
                                                           description='Test Description')
                    runner.run(suit)
            else:
                logger.info("Have no case to test.")
        except Exception as ex:
            logger.info(str(ex))

        finally:
            logger.info("*********TEST END*********")
            # fp.close()

        # 判断邮件发送的开关
        if on_off == 'open':
            send_mail.qq_email()
        else:
            logger.info("邮件发送开关配置关闭，请打开开关后可正常自动发送测试报告")


# pythoncom.CoInitialize()
# scheduler = BlockingScheduler()
# scheduler.add_job(AllTest().run, 'cron', day_of_week='1-5', hour=14, minute=59)
# scheduler.start()


if __name__ == '__main__':
    AllTest().run()
