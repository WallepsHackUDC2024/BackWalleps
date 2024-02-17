from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
import requests
import json

f = open('data.json')
 
# returns JSON object as 
# a dictionary
data = json.load(f)
f.close()
devices = [{"id":1,"user_id":1,"device_name":"electric_stove","times_week":7,"daytime":"12:00","duration":2},{"id":1,"user_id":1,"device_name":"fridge","times_week":7,"daytime":"12:00","duration":2}]
timedelta_home = 6
arrive_home = 9


trams = True

if not trams:
    response = requests.get("https://api.preciodelaluz.org/v1/prices/all?zone=PCB")
    response = response.json()
    if "error" in response:
        print("Error")
        exit()
    wanted_keys = list(response.keys())[arrive_home:arrive_home+timedelta_home]
    prices = []
    for key in wanted_keys:
        prices.append(response[key]["price"])
else:
    prices = [1,1,1,1,1,1,1,1,2,2,3,3,3,3,2,2,2,2,3,3,3,3,2,2]
    prices = prices[arrive_home:arrive_home+timedelta_home]
wcnf = WCNF()
for index, device in enumerate(devices):
    minimum = []
    for i in range(timedelta_home):
        minimum.append((i+1)+(index*timedelta_home))
        wcnf.append([(i+1)+(index*timedelta_home)], weight=int(prices[i] * data[device["device_name"]]["kWh"]))
    wcnf.append(minimum)

for i in range(timedelta_home):
    same_time = []
    for index in range(len(devices)):
        same_time.append(-((i+1)+(index*timedelta_home)))
    wcnf.append(same_time)

best = []
best_cost = 10000
with RC2(wcnf) as rc2:
    for m in rc2.enumerate():
        cost = sum(map(abs, m))
        if cost <= best_cost:
            best = m
            best_cost = cost
print(best)

result = []
for i in range(len(best)):
    if best[i] > 0:
        result.append({"device":devices[(i-1)//timedelta_home]["device_name"],"time":i%timedelta_home+arrive_home, "times_week":devices[(i-1)//timedelta_home]["times_week"]})
        
print(result) 