# -*- coding: utf-8 -*- 
# TIME     : 2021/2/3 22:51
# AUTHOR   : luo nan
# FILE     : test_selenium_api.py
# SOFTWARE : PyCharm
# FUNCTION :
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select

driver = webdriver.Chrome()

driver.maximize_window()

driver.get('http://www.baidu.com')

bg = driver.find_element_by_link_text('设置')
bg.click()

# ActionChains(driver).move_to_element(bg).perform()
# time.sleep(3)
# driver.find_element_by_link_text("搜索设置").click()
time.sleep(3)

se = driver.find_element_by_id("nr")

Select(se).select_by_index(2)

time.sleep(2)

driver.quit()