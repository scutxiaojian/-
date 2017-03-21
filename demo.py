# coding=UTF-8
import pickle
import random
from time import sleep, time

from selenium.webdriver import DesiredCapabilities
from weibo import APIClient
import json
import io
from selenium import webdriver
import ConfigParser
import re
from selenium.webdriver.common.keys import Keys


def get_code(url):
    codetime = 1
    print 'authUrl:'+url
    driver = webdriver.PhantomJS(executable_path=phantomjsPath, desired_capabilities=dcap)
    driver.get(url)
    sleep(2)
    while 'http://api.weibo.com/oauth2/default.html?code=' not in driver.current_url and codetime != 8:
        print 'login_'+str(codetime)
        try:
            userId = driver.find_element_by_xpath("//*[@id='userId']")
            userId.send_keys(USERID)
            password = driver.find_element_by_xpath("//*[@id='passwd']")
            password.send_keys(USERPASSWD)
            sleep(2)
            driver.find_element_by_xpath("//*[@id='outer']/div/div[2]/form/div/div[2]/div/p/a[1]").click()
            sleep(2)
        except:
            codetime = codetime + 1
            continue
        print 'current_url:'+driver.current_url
        codetime  = codetime + 1

    currentUrl = driver.current_url
    code = currentUrl.split('=')[1]
    driver.quit()

    print 'code:' + code
    if re.match(r'[a-z][A-Z][0-9]',code):
        return 'code error!'
    return code

def out_put(data):
    parseData = json.dumps(data, ensure_ascii=False, indent=2)
    f = io.open('test','w',encoding='utf-8')
    f.write(parseData)
    f.close()
    print 'success!'

def get_data(code):
    r = client.request_access_token(code)
    access_token = r.access_token
    expires_in = r.expires_in

    client.set_access_token(access_token, expires_in)
    try:
        # res = client.statuses.public_timeline.get(count=2)
        # res  = client.statuses.user_timeline.get(uid=3937348351)
        # res=client.emotions.get()
        # res = client.friendships.friends.get(uid=3937348351)
        res = client.users.show.get(screen_name='姚晨')
        # res = client.users.show.get(uid=5407847973)
    except:
        return 'APIError!'
    return res

cf = ConfigParser.ConfigParser()
cf.read("config.ini")
APP_KEY = cf.get('weibo','APP_KEY')
APP_SECRET = cf.get('weibo','APP_SECRET')
CALLBACK_URL = cf.get('weibo','CALLBACK_URL')
USERID = cf.get('weibo','USERID')
USERPASSWD = cf.get('weibo','USERPASSWD')
phantomjsPath=cf.get('path','phantomjsPath')

UA = eval(cf.get('UA', 'UA'))
UserAgent = UA[random.randint(0, 3)]
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (UserAgent)


client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
url = client.get_authorize_url()

code = get_code(url)
data = get_data(code)
out_put(data)
