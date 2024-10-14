
import json
import requests
import prettytable as pt

# 读取文件 城市字母文件
f = open('../city.json', encoding='utf-8')
json_data = json.loads(f.read())
# 输入内容
from_city = "无锡"
to_city = "泗阳"
date = '2024-10-04'
print(json_data)
print(date)
print(json_data[from_city])
print(json_data[to_city])

# 确定请求链接
url = f'https://kyfw.12306.cn/otn/leftTicket/queryG?leftTicketDTO.train_date={date}&leftTicketDTO.from_station={json_data[from_city]}&leftTicketDTO.to_station={json_data[to_city]}&purpose_codes=ADULT'
# url = "https://kyfw.12306.cn/otn/leftTicket/queryG?leftTicketDTO.train_date={date}&leftTicketDTO.from_station={json_data[from_city]}&leftTicketDTO.to_station={json_data[to_city]}&purpose_codes=ADULT"
# 模拟伪装 ---> headers 请求头

headers = {
    # Cookie 用户信息, 表示常用于检测是否有登陆账号
    'Cookie':"_uab_collina=172724904537462317949747; JSESSIONID=97FC797FB71F7FAD806C2CB175CD6D8C; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; _jc_save_wfdc_flag=dc; _jc_save_showIns=true; route=c5c62a339e7744272a54643b3be5bf64; BIGipServerotn=552075530.64545.0000; BIGipServerpassport=837288202.50215.0000; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_fromDate=2024-09-26; _jc_save_toDate=2024-09-26",

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
}
# 发送请求
response = requests.get(url=url, headers=headers)
print(response.json())



# 实例化一个对象
tb = pt.PrettyTable()
# 输出添加字段名
tb.field_names = [
    '序号',
    '车次',
    '出发时间',
    '到达时间',
    '耗时',
    '特等座',
    '一等',
    '二等',
    '软卧',
    '硬卧',
    '硬座',
    '无座',
]
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
    dit = {
        '序号': page,
        '车次': num,
        '出发时间': start_time,
        '到达时间': end_time,
        '耗时': use_time,
        '特等座': topGrade,
        '一等': first_class,
        '二等': second_class,
        '软卧': soft_sleeper,
        '硬卧': hard_sleeper,
        '硬座': hard_seat,
        '无座': no_seat,
    }
    # print(dit)
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
    page += 1 # 每次循环+1

print(tb)