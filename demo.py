from time import sleep
from weibo import APIClient
import json
import io
from selenium import webdriver
import ConfigParser
from selenium.webdriver.common.keys import Keys

cf = ConfigParser.ConfigParser()
cf.read("config.ini")
APP_KEY = cf.get('weibo','APP_KEY')
APP_SECRET = cf.get('weibo','APP_SECRET')
CALLBACK_URL = cf.get('weibo','CALLBACK_URL')
USERID = cf.get('weibo','USERID')
USERPASSWD = cf.get('weibo','USERPASSWD')

driver = webdriver.PhantomJS(executable_path='/home/cxj/Downloads/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')

client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
url = client.get_authorize_url()
# print url

def getCurrentUrl(url):
    driver.get(url)
    userId = driver.find_element_by_xpath("//*[@id='userId']")
    userId.send_keys(USERID)
    password = driver.find_element_by_xpath("//*[@id='passwd']")
    password.send_keys(USERPASSWD)
    sleep(2)
    driver.find_element_by_xpath("//*[@id='outer']/div/div[2]/form/div/div[2]/div/p/a[1]").click()
    sleep(2)
    return driver.current_url

def getCode(url):
    currentUrl = getCurrentUrl(url)
    while 'code'not in currentUrl:
        sleep(1)
        currentUrl = getCurrentUrl(url)
    # print currentUrl
    return currentUrl.split('=')[1]

def outPut(data):
    a = json.dumps(data, ensure_ascii=False, indent=2)
    fout = io.open('test','w',encoding='utf-8')
    fout.write(a)

def getData(code):
    r = client.request_access_token(code)
    access_token = r.access_token
    expires_in = r.expires_in

    client.set_access_token(access_token, expires_in)

    res = client.statuses.public_timeline.get(count=2)
    # res  = client.statuses.user_timeline.get(uid=3937348351)
    # res=client.emotions.get()
    # res = client.friendships.friends.get(uid=3937348351)
    # res = client.users.show.get(uid=5407847973)
    return res

code = getCode(url)
data = getData(code)
outPut(data)
print 'code:'+code
driver.quit()
