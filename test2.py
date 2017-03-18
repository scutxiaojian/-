from selenium import webdriver

driver = webdriver.PhantomJS(executable_path='/home/cxj/Downloads/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
driver.get('https://www.baidu.com')
elem = driver.find_element_by_id('kw')
elem.send_keys(u'php')
driver.find_element_by_id('su').click()
driver.refresh()
print('title', driver.title)
print(driver.current_url)
print('\nsource', driver.page_source)