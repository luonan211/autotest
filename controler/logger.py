# -*-coding:utf-8 -*-
# 解决配置的logger 在单独的文件中无法调试
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from basepath import get_base_path

# log_path是存放日志的路径
log_path = os.path.join(get_base_path(), 'logs')
# 如果不存在这个logs文件夹，就自动创建一个
if not os.path.exists(log_path):
    os.mkdir(log_path)


class MyLog:
    def __init__(self):
        # 文件的命名
        self.log_name = os.path.join(log_path, 'log')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        # 最多存放日志的数量
        self.backup_count = 30
        # 日志输出格式
        # self.formatter = logging.Formatter('[%(asctime)s]-%(filename)s-%(processName)s]-%(levelname)s: %(message)s')
        self.formatter = logging.Formatter('%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s')

    def __console(self, level, message):
        # 创建一个FileHandler，用于写到本地
        # fh = logging.FileHandler(self.log_name, 'a')  # 追加模式  这个是python2的
        # fh = logging.FileHandler(self.log_name, 'a', encoding='utf-8')  # 这个是python3的
        # 每天重新创建一个日志文件，最多保留backup_count份
        fh = TimedRotatingFileHandler(filename=self.log_name, when='D', interval=1,
                                      backupCount=self.backup_count, delay=True, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)

        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)


if __name__ == "__main__":
    log = MyLog()
    log.info("---测试开始----")
    log.info("操作步骤1,2,3")
    log.warning("----测试结束----")