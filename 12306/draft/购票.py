from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime

# 配置webdriver路径
driver = webdriver.Chrome()

try:
    # 全屏打开浏览器窗口
    driver.maximize_window()
    # 打开12306登录页面
    driver.get('https://kyfw.12306.cn/otn/resources/login.html')

    # # 登录
    # time.sleep(2)  # 等待页面加载1
    # driver.find_element(By.CSS_SELECTOR, '#J-userName').send_keys('18852077330')
    # driver.find_element(By.CSS_SELECTOR, '#J-password').send_keys('zx123456')
    # driver.find_element(By.CSS_SELECTOR, '#J-login').click()
    #
    # # 等待登录完成
    # time.sleep(2)
    #
    # driver.find_element(By.CSS_SELECTOR, '#id_card').send_keys("7419")
    # # 点击发送验证码按钮
    # driver.find_element(By.CSS_SELECTOR, '#verification_code').click()
    #
    # time.sleep(20)
    # driver.find_element(By.CSS_SELECTOR, "#sureClick").click()
    # time.sleep(2)
    #
    # driver.find_element(By.CSS_SELECTOR, '#link_for_ticket').click()
    # print("登陆成功")

    #等待用户登录
    time.sleep(30)



    print("目标时间已到，继续执行后续代码...")

    # 输入出发地和目的地
    driver.find_element(By.ID, 'fromStationText').click()
    driver.find_element(By.ID, 'fromStationText').clear()
    driver.find_element(By.ID, 'fromStationText').send_keys('无锡')
    driver.find_element(By.ID, 'fromStationText').send_keys(Keys.ENTER)

    driver.find_element(By.ID, 'toStationText').click()
    driver.find_element(By.ID, 'toStationText').clear()
    driver.find_element(By.ID, 'toStationText').send_keys('泗阳')
    driver.find_element(By.ID, 'toStationText').send_keys(Keys.ENTER)

    # 输入出发日期
    driver.find_element(By.ID, 'train_date').click()
    driver.find_element(By.ID, 'train_date').clear()
    driver.find_element(By.ID, 'train_date').send_keys('2024-10-04')
    #点击查询
    driver.find_element(By.ID, 'query_ticket').click()

    # 等待到指定时间，例如 2024-10-03 08:30:00
    # target_time = datetime(2024, 9, 27, 14, 52, 0)  # 目标时间点
    # while datetime.now() < target_time:
    #     time.sleep(0.1)  # 每隔0.1秒检查一次

    time.sleep(1)

    train = ['G8266','G8270','G7508','G8286','G8300','G2588','G8274']

    for item in train:
      path = f"//tbody//*[contains(@id,'{item}')]//a[@class='btn72']"
      # 选择车次并预定
      try:
          btn72 = driver.find_element(By.XPATH, path)
          btn72.click()
          time.sleep(0.5)
          # 选择乘车人
          driver.find_element(By.CSS_SELECTOR, '#normalPassenger_0').click()

          # #选择席位
          # driver.find_element(By.XPATH,"//*[@id='seatType_1']/option[@value='O']").click()

          # 提交订单
          driver.find_element(By.ID, 'submitOrder_id').click()

          # 确认提交
          time.sleep(3)
          driver.find_element(By.ID, 'qr_submit_id').click()
          print("抢票成功")
          break

      except Exception:
          print(f"{item}车次已售罄")

      time.sleep(1)




finally:
    # 关闭浏览器
    input("\n回车键退出")

