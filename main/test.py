import datetime

date=datetime.datetime.now().__str__().split(' ')
time=date[1].replace(':', "'")

print(time)