# coding=UTF-8
from time import sleep, time

import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import ConfigParser
import random

time_1 = time()

cf = ConfigParser.ConfigParser()
cf.read("config.ini")
phantomjsPath=cf.get('path','phantomjsPath')
UA = eval(cf.get('UA','UA'))
UserAgent = UA[random.randint(0,3)]
USERID = cf.get('weibo','USERID')
USERPASSWD = cf.get('weibo','USERPASSWD')

LoginUrl = 'http://weibo.com/login'

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (UserAgent)

driver = webdriver.PhantomJS(executable_path=phantomjsPath,desired_capabilities=dcap)
driver.maximize_window()
# driver.set_window_size(1440, 900)
driver.get(LoginUrl)
sleep(1)
userName = driver.find_element_by_xpath("//*[@id='loginname']")
userName.send_keys(USERID)
password = driver.find_element_by_xpath("//*[@id='pl_login_form']/div/div[3]/div[2]/div/input")
password.send_keys(USERPASSWD)
sleep(1)
driver.find_element_by_xpath("//*[@id='pl_login_form']/div/div[3]/div[6]/a/span").click()
sleep(2)
driver.find_element_by_xpath("//*[@id='v6_pl_rightmod_myinfo']/div/div/div[2]/ul/li[1]/a/strong").click()
sleep(2)

for i in range(1,31):
    userUrl = driver.find_element_by_xpath("//*[@id='Pl_Official_RelationMyfollow__93']/div/div/div/div[3]/ul/li["+str(i)+"]/div[1]/div[2]/div[1]/a[1]").get_attribute('href')

    userId = userUrl.split('?')[0][19:]
    if not(re.match(r'[0-9]',userId)):
        userDomain = userUrl.split('?')[0][17:]
        print 'userDomain:'+userDomain
    else:
        print 'userId:'+userId


driver.quit()

time_2 = time()
print time_2-time_1