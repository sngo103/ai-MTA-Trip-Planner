from basic_search import route, initialize_system
from subway_system import Subway_System
from subway_system import Current_State
import random

f = open('testing.txt','a')

alphstr = 'abcdefghiklmnopqrstuvwyzABCDEFGHIKLMNOPQRSTUVWY'
directory_data, transfers_data, stop_order_data, mta = initialize_system()
current_state = None


def generateRoute(start, end, mta, current_state):
    return route(start, end, mta, current_state)

for i in range(200):
    start = random.choice(alphstr)
    end = random.choice(alphstr)
    output = generateRoute(start, end, mta, current_state)
    f.write('\n\n' + str(i))
    if not output:
        print(i)
    else:
        f.write(output)

    directory_data, transfers_data, stop_order_data, mta = initialize_system()

f.close()




