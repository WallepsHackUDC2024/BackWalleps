from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
import requests
import json

import src.Device.model as DeviceModel
import src.User.model as UserModel


def get_prices(tram:bool, arrive_home:int, timedelta_home:int):
    if not tram:
        response = requests.get("https://api.preciodelaluz.org/v1/prices/all?zone=PCB")
        response = response.json()
        if "error" in response:
            print("Error")
            exit()
        all_keys = list(response.keys())+list(response.keys())
        wanted_keys = all_keys[arrive_home:arrive_home+timedelta_home]
        prices_reduced = []
        prices = []
        for key in all_keys:
            prices.append(response[key]["price"])
        for key in wanted_keys:
            prices_reduced.append(response[key]["price"])
        return prices, prices_reduced
    prices = [1,1,1,1,1,1,1,1,2,2,3,3,3,3,2,2,2,2,3,3,3,3,2,2,1,1,1,1,1,1,1,1,2,2,3,3,3,3,2,2,2,2,3,3,3,3,2,2]
    prices_reduced = prices[arrive_home:arrive_home+timedelta_home]
    return prices, prices_reduced


def read_json(file_name:str):
    f = open(file_name)
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    f.close()
    return data


def minimum_one_hour(wcnf:WCNF, devices: DeviceModel, timedelta_home:int, prices:list, data:dict):
    for index, device in enumerate(devices):
        minimum = []
        for i in range(timedelta_home):
            minimum.append((i+1)+(index*timedelta_home))
            wcnf.append([(i+1)+(index*timedelta_home)], weight=int(prices[i] * data[device.device_name]["kWh"]))
        wcnf.append(minimum)
        
def max_one_per_device(wcnf:WCNF, devices: DeviceModel, timedelta_home:int):
    for index, device in enumerate(devices):
        for i in range(timedelta_home):
            for j in range(i+1, timedelta_home):
                wcnf.append([-((i+1)+index*timedelta_home),-((j+1)+index*timedelta_home)])

def max_one_per_hour(wcnf:WCNF, devices: DeviceModel, timedelta_home:int):
    if len(devices) > 1:
        for i in range(timedelta_home):
            same_time = []
            for index in range(len(devices)):
                same_time.append(-((i+1)+(index*timedelta_home)))
            wcnf.append(same_time)
            
            
def get_solution(wcnf:WCNF):
    best = []
    best_cost = 10000
    with RC2(wcnf) as rc2:
        return rc2.compute()




def solve(devices: DeviceModel, user: UserModel, sections:bool):
    timedelta_home = user.home_duration
    arrive_home = user.home_hours

    extended_prices, prices = get_prices(sections, arrive_home, timedelta_home)
        
    wcnf = WCNF()
    
    data = read_json('predictor/data.json')
    minimum_one_hour(wcnf, devices, timedelta_home, prices, data)
    max_one_per_device(wcnf, devices, timedelta_home)
    max_one_per_hour(wcnf, devices, timedelta_home)

    solution = get_solution(wcnf)
    print(solution)
    result = []
    
    prices_dict = {1:0.094415, 2:0.124286, 3:0.171914}
    
    for i in range(len(solution)):
        if solution[i] > 0:
            if sections:
                current_spent = data[devices[i//timedelta_home].device_name]["kWh"] * prices_dict[extended_prices[devices[i//timedelta_home].daytime]] * 4 * devices[i//timedelta_home].times_week
                expected_spent = data[devices[i//timedelta_home].device_name]["kWh"] * prices_dict[extended_prices[(i%timedelta_home+arrive_home)%24]] * 3 * devices[i//timedelta_home].times_week
            else:
                current_spent = data[devices[i//timedelta_home].device_name]["kWh"] * extended_prices[devices[i//timedelta_home].daytime] * 4 * devices[i//timedelta_home].times_week /1000
                expected_spent = data[devices[i//timedelta_home].device_name]["kWh"] * extended_prices[(i%timedelta_home+arrive_home)%24] * 3 * devices[i//timedelta_home].times_week /1000

            result.append({"device":devices[i//timedelta_home].device_name,"time":(i%timedelta_home+arrive_home)%24, "times_week":devices[i//timedelta_home].times_week, "current_spent":current_spent, "expected_spent":expected_spent})
            
    return result 