# coding=UTF-8
from time import sleep

import io
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import ConfigParser
import random

cf = ConfigParser.ConfigParser()
cf.read("config.ini")
phantomjsPath=cf.get('path','phantomjsPath')
UA = eval(cf.get('UA','UA'))
UserAgent = UA[random.randint(0,3)]
LoginUrl = 'http://weibo.com/login'
USERID = cf.get('weibo','USERID')
USERPASSWD = cf.get('weibo','USERPASSWD')
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (UserAgent)

driver = webdriver.PhantomJS(executable_path=phantomjsPath,desired_capabilities=dcap)
driver.set_window_size(1440, 900)
driver.get(LoginUrl)
sleep(2)
userId = driver.find_element_by_xpath("//*[@id='loginname']")
userId.send_keys(USERID)
password = driver.find_element_by_xpath("//*[@id='pl_login_form']/div/div[3]/div[2]/div/input")
password.send_keys(USERPASSWD)
sleep(1)
driver.find_element_by_xpath("//*[@id='pl_login_form']/div/div[3]/div[6]/a/span").click()
sleep(2)

# f = io.open('source','w',encoding='utf-8')
# f.write(driver.page_source)
# sleep(2)
driver.get_screenshot_as_file('01.png')

driver.quit()


