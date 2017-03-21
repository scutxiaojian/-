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

driver = webdriver.Firefox(executable_path='/usr/bin/firefox')
driver.get(LoginUrl)

# userId = driver.find_element_by_xpath("//*[@id='pl_login_form']/div/div[1]/div/a[1]")
# userId.send_keys(USERID)
# password = driver.find_element_by_xpath("//*[@id='pl_login_form']/div/div[3]/div[2]/div/input")
# password.send_keys(USERPASSWD)
sleep(2)
# f = io.open('source','w',encoding='utf-8')
# f.write(driver.page_source)
# sleep(2)
driver.get_screenshot_as_file('01.png')



driver.quit()


