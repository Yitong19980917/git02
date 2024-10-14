import time
import json
import requests
from datetime import datetime
import prettytable as pt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class TrainTicket:
    def __init__(self, from_city, to_city, date):
        self.from_city = from_city
        self.to_city = to_city
        self.date = date

    def check(self):

        f = open('city.json', encoding='utf-8')
        json_data = json.loads(f.read())
        url = f'https://kyfw.12306.cn/otn/leftTicket/queryG?leftTicketDTO.train_date={self.date}&leftTicketDTO.from_station={json_data[self.from_city]}&leftTicketDTO.to_station={json_data[self.to_city]}&purpose_codes=ADULT'
        headers = {
            # Cookie 用户信息, 表示常用于检测是否有登陆账号
            'Cookie': "_uab_collina=172724904537462317949747; JSESSIONID=97FC797FB71F7FAD806C2CB175CD6D8C; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; _jc_save_wfdc_flag=dc; _jc_save_showIns=true; route=c5c62a339e7744272a54643b3be5bf64; BIGipServerotn=552075530.64545.0000; BIGipServerpassport=837288202.50215.0000; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_fromDate=2024-09-26; _jc_save_toDate=2024-09-26",

            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
        }
        response = requests.get(url=url, headers=headers)
        # 实例化一个对象
        tb = pt.PrettyTable()
        # 输出添加字段名
        tb.field_names = ['序号', '车次', '出发时间', '到达时间', '耗时', '特等座', '一等', '二等', '软卧', '硬卧', '硬座','无座']
        # 添加序号 每次循环+1
        page = 0
        # for循环遍历, 把列表里面元素 一个一个提出来
        for i in response.json()['data']['result']:
            # 先用 split 分割, 再用列表取值: 根据索引位置
            index = i.split('|')
            num = index[3]  # 车次
            start_time = index[8]  # 出发时间
            end_time = index[9]  # 到达时间
            use_time = index[10]  # 耗时
            topGrade = index[32]  # 特等座
            first_class = index[31]  # 一等
            second_class = index[30]  # 二等
            hard_sleeper = index[28]  # 硬卧
            hard_seat = index[29]  # 硬座
            no_seat = index[26]  # 无座
            soft_sleeper = index[23]  # 软卧
            # 添加每行输出内容
            tb.add_row([page, num, start_time, end_time,
                        use_time,
                        topGrade,
                        first_class,
                        second_class,
                        soft_sleeper,
                        hard_sleeper,
                        hard_seat,
                        no_seat,
                        ])
            page += 1  # 每次循环+1

        print(tb)

    def purchase(self, target_time=None):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get('https://kyfw.12306.cn/otn/resources/login.html')
        time.sleep(30)  # 等待用户登录
        driver.find_element(By.ID, 'fromStationText').click()
        driver.find_element(By.ID, 'fromStationText').clear()
        driver.find_element(By.ID, 'fromStationText').send_keys(self.from_city)
        driver.find_element(By.ID, 'fromStationText').send_keys(Keys.ENTER)

        driver.find_element(By.ID, 'toStationText').click()
        driver.find_element(By.ID, 'toStationText').clear()
        driver.find_element(By.ID, 'toStationText').send_keys(self.to_city)
        driver.find_element(By.ID, 'toStationText').send_keys(Keys.ENTER)

        driver.find_element(By.ID, 'train_date').click()
        driver.find_element(By.ID, 'train_date').clear()
        driver.find_element(By.ID, 'train_date').send_keys(self.date)

        driver.find_element(By.ID, 'query_ticket').click()  # 点击查询
        if target_time:
            while datetime.now() < target_time:
                time.sleep(0.1)  # 每隔0.1秒检查一次
        if not target_time:
            time.sleep(1)
        train = ['G8266', 'G8270', 'G7508', 'G8286', 'G8300', 'G2588', 'G8274']
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

                driver.find_element(By.ID, 'submitOrder_id').click()  # 提交订单
                time.sleep(3)  # 等待订单加载
                driver.find_element(By.ID, 'qr_submit_id').click()  # 确认提交
                print("抢票成功")
                break
            except Exception:
                print(f"{item}车次已售罄")

        input("\n请按回车键退出程序")
