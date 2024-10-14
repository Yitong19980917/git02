from TrainTicket import TrainTicket
from datetime import datetime

from_city = "无锡"
to_city = "泗阳"
date = '2024-10-04'
target_time = datetime(2024, 9, 29, 15, 28, 0)  # 设置抢票目标时间点
t = TrainTicket(from_city,to_city,date)
t.check()
t.purchase(target_time)



