# coding=UTF-8
from time import sleep, time
import MySQLdb
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import ConfigParser
import random
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui

cf = ConfigParser.ConfigParser()
cf.read("config.ini")

phantomjsPath=cf.get('path','phantomjsPath')

UA = eval(cf.get('UA','UA'))
UserAgent = UA[random.randint(0,3)]

USERID = cf.get('weibo','USERID')
USERPASSWD = cf.get('weibo','USERPASSWD')

u = cf.get('mysql','u')
p = cf.get('mysql','p')


def start(LoginUrl):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (UserAgent)

    driver = webdriver.PhantomJS(executable_path=phantomjsPath,desired_capabilities=dcap)
    driver.maximize_window()
    # driver.set_window_size(1440, 900)
    driver.get(LoginUrl)
    print 'login'

    locator_1 = cf.get('locator','locator_1')
    locator_2 = cf.get('locator','locator_2')
    locator_3 = cf.get('locator','locator_3')

    if is_visible(driver,locator_1) and is_visible(driver,locator_2) and is_visible(driver,locator_3):
        userName = driver.find_element_by_xpath(locator_1)
        userName.send_keys(USERID)
        password = driver.find_element_by_xpath(locator_2)
        password.send_keys(USERPASSWD)
        driver.find_element_by_xpath(locator_3).click()

    print 'craw start'
    if craw(driver) == 0:
        print 'craw failed'
    else:
        print 'craw end'
        driver.quit()

def out_put(data):
    try:
        datas = [data['username'],data['follow'],data['fans'],data['tweets'],data['url']]
        conn = MySQLdb.connect(db='sina', user=u,passwd=p,charset="utf8")
        cursor = conn.cursor()
        cursor.execute("insert into user (username,follow,fans,tweets,url) values (%s,%s,%s,%s,%s)", datas)
        conn.commit()
        cursor.close()
        conn.close()
    except:
        return 0

def craw(driver):
    data = {}
    locator_1 = '//*[@id=\"Pl_Core_T8CustomTriColumn__3\"]/div/div/div/table/tbody/tr/td[1]/a/strong'
    locator_2 = '//*[@id=\"Pl_Core_T8CustomTriColumn__3\"]/div/div/div/table/tbody/tr/td[2]/a/strong'
    locator_3 = '//*[@id=\"Pl_Core_T8CustomTriColumn__3\"]/div/div/div/table/tbody/tr/td[3]/a/strong'

    main_handle = driver.current_window_handle
    print driver.current_window_handle
    rootuser = get_rootuser()

    for i in range(len(rootuser)):
        url = rootuser[i][2]
        js='window.open(\"'+url+'\");'
        print js
        driver.execute_script(js)

        handles = driver.window_handles
        print handles

        for handle in handles:
            if handle!=driver.current_window_handle:
                print 'switch to',handle
                driver.switch_to.window(handle)
                print driver.current_window_handle
                break

        driver.maximize_window()

        if is_visible(driver,locator_1) and is_visible(driver,locator_2) and is_visible(driver,locator_3):

            data['follow'] = driver.find_element_by_xpath(locator_1).text
            data['fans'] = driver.find_element_by_xpath(locator_2).text
            data['tweets'] = driver.find_element_by_xpath(locator_3).text

        data['username'] = rootuser[i][1]
        data['url'] = rootuser[i][2]

        driver.close()
        driver.switch_to_window(main_handle)

        if out_put(data) == 0:
            driver.quit()
            return 0

def get_rootuser():
    rootuser = []
    conn = MySQLdb.connect(db='sina', user=u,passwd=p,charset="utf8")
    cursor = conn.cursor()
    cursor.execute("select * from rootuser")
    for row in cursor.fetchall():
        rootuser.append(row)

    return rootuser

# 一直等待某元素可见，默认超时10秒
def is_visible(driver,locator, timeout=10):
    try:
        ui.WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, locator)))
        return True
    except TimeoutException:
        return False

time_1 = time()

LoginUrl = 'http://weibo.com/login'

start(LoginUrl)

time_2 = time()
print time_2-time_1

