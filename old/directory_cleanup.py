stop_order_data = open('stop_order.csv', 'r').read().split('\n')
containment = {}

for line in stop_order_data:
    line_route = line.split(',')[1:]
    for stopID in line_route:
        containment[stopID] = True

excluded = []
for id in range(765):
    if str(id) not in containment:
        excluded.append(id)

print(excluded)
