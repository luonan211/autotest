# -*- coding: utf-8 -*- 
# TIME     : 2020/11/30 21:27
# AUTHOR   : luo nan
# FILE     : test01case.py
# SOFTWARE : PyCharm
# FUNCTION :
import unittest
from selenium import webdriver


class TestBaiduCase(unittest.TestCase):
    def test_001_case(self):
        driver = webdriver.Chrome()
        url = "http://www.baidu.com"
        driver.get(url)
        driver.find_element_by_id('kw').send_keys("python+selenium")
        driver.find_element_by_id('su').click()
        driver.quit()


if __name__ == '__main__':
    unittest.main()
