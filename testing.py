from basic_search import route, initialize_system
from subway_system import Subway_System
from subway_system import Current_State
import random

f = open('testing.txt','a')

alphstr = 'abcdefghiklmnopqrstuvwyzABCDEFGHIKLMNOPQRSTUVWY'
directory_data, transfers_data, stop_order_data, mta = initialize_system()
current_state = None

for i in range(200):
    start = random.choice(alphstr)
    end = random.choice(alphstr)
    output = route(start, end, mta, current_state)
    f.write('\n\n' + str(i))
    if not output:
        print (i)
        print(start)
        print(end)
    else:
        f.write(output)

f.close()


