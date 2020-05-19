from main import route, initialize_system
from subway_system import Subway_System
import random

f = open('testing.txt','w')

alphstr = 'abcdefghiklmnopqrstuvwyzABCDEFGHIKLMNOPQRSTUVWY'
directory_data, transfers_data, stop_order_data, mta = initialize_system()


def generateRoute(start, end, mta):
    return route(start, end, mta, False)

for i in range(25):
    start = random.choice(alphstr)
    end = random.choice(alphstr)
    output = generateRoute(start, end, mta)
    f.write('\n\n' + str(i))
    if not output:
        print(i)
    else:
        f.write(output)

    directory_data, transfers_data, stop_order_data, mta = initialize_system()

f.close()




