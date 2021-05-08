####################################
### Created by K18039-後藤 廉
####################################
### 内容：日付・時間の実装の確認用
### ファイル：datetime_test.py
####################################

# 現在日時の取得
from datetime import datetime
import datetime


#########################################################
# 日付
print('=====================')
now = datetime.datetime.now()
print(type(now))
aa = str(now.date())
print(type(aa))
daytmp = datetime.datetime.strptime(aa, '%Y-%m-%d')
day=daytmp.date()
print(type(day))
print(day)
print('=====================')
#########################################################
# 時間
now2 = datetime.datetime.now()
print(type(now2))
print(now2)
bb = now2.strftime("%H:%M:%S")
cc = now2.time()
print('debug')
print('{0:%H:%M:%S}'.format(now2.time()))
print('jikann')
print(type('{0:%H:%M:%S}'.format(now2.time())))
print('hizuke')
print(type('{0:%Y-%m-%d}'.format(now2.date())))
print (bb)
print (type(bb))
timetmp = datetime.datetime.strptime(bb, '%H:%M:%S')
time = timetmp.time()
print(type(time))
print(time)
print('=====================')
#########################################################