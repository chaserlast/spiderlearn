from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
import time

#browser = webdriver.Chrome()
# 动作链
# url = 'https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
# browser.get(url)
# browser.switch_to.frame('iframeResult')
# source = browser.find_element_by_css_selector('#draggable')
# target = browser.find_element_by_css_selector('#droppable')
# action = ActionChains(browser)
# action.drag_and_drop(source,target)
# action.perform()


# browser.get('https://www.taobao.com/')
# # lis = browser.find_element_by_css_selector((' .service-bd li'))
# # print(lis)
# input_first = browser.find_element(By.ID,'q')
# input_first.send_keys('iphone')
# time.sleep(1)
# button = browser.find_element_by_class_name('btn-search')
# button.click()

# print(browser.page_source)
# browser.close()



# 使用back()和forward()方法
# browser.get('https://www.baidu.com/')
# browser.get('https://www.taobao.com/')
# browser.get('https://www.toutiao.com/')
# browser.back()
# time.sleep(1)
# browser.forward()
# time.sleep(1)
# browser.close()

#多选项卡的使用
browser = webdriver.Chrome()
browser.get('https://www.baidu.com/')
browser.execute_script('window.open()')

print(browser.window_handles)
browser.switch_to.window(browser.window_handles[1])
browser.get('https://www.zhihu.com/')
time.sleep(1)
browser.execute_script('window.open()')
browser.switch_to.window(browser.window_handles[2])
browser.get('https://www.taobao.com/')