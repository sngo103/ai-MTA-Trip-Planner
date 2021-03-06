from main import route, initialize_system
from subway_system import Subway_System
import random

f = open('testing.txt','w')
f.write('')
f.close()
f = open('testing.txt', 'a')

alphstr = 'abcdefghiklmnopqrstuvwyzABCDEFGHIKLMNOPQRSTUVWY'
directory_data, transfers_data, stop_order_data, mta = initialize_system()


def generateRoute(start, end, mta):
    accessibility = True
    if random.random() > 0.5:
        accessibility = False
    start = random.choice(mta.findStop(start, accessibility))
    end = random.choice(mta.findStop(end, accessibility))
    return route(start, end, mta, accessibility)

for i in range(200):
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




