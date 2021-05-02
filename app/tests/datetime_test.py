from datetime import datetime
import datetime

# Date
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

# Time
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
