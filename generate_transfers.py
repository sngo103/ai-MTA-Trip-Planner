#import stop order data set
f = open('stop order.csv', 'r')
f = f.read()
data = f.split('\n')

stopDict = {}
transferDict = {}
output = ''

#produce transferDict dictionary
for line in data:
    line = line.split(',')
    train = line[0]
    stops = line[1:]
    for stop in stops:
        
        #process connections with different stop names
        if not stop.isdigit():
            stop = stop[:-1]
            
        #keep track of all stops
        if stop not in stopDict:
            stopDict[stop] = train

        #separate transfers
        else:
            if stop not in transferDict:
                transferDict[stop] = [stopDict[stop]]
            transferDict[stop].append(train)

print (transferDict)

#generate csv
for stop, trains in transferDict.items():
    output += str(stop) + ','
    for train in trains:
        output += str(train) + ','
    #print(output)
    output = output[:-1] + '\n'

output = output[:-1]

#write to csv file
outputFile = open('transfers.csv', 'w')
outputFile.write(output)
