import re

userUrl = 'http://weibo.com/u/1728087525?from=myfollow_all'
userId = userUrl.split('?')[0][19:]
# if not(re.match(r'[0-9]',userId)):
#     print '0'
# a = 'http://weibo.com/yaochen?from=myfollow_all'
# b = a.split('?')[0][17:]
# if not(re.match(r'[0-9]',b)):
#     print '0'
print userId


# print driver.current_window_handle
#
# js='window.open("http://weibo.com/u/1728087525?from=myfollow_all");'
# driver.execute_script(js)
#
# handles = driver.window_handles
# print handles
#
# for handle in handles:
#     if handle!=driver.current_window_handle:
#         print 'switch to ',handle
#         driver.switch_to.window(handle)
#         print driver.current_window_handle
#         break
#
# driver.maximize_window()
#
# sleep(5)
#
# driver.get_screenshot_as_file('01.png')