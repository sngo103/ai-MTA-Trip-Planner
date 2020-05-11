from csv import reader
import csv

transfers_data = {}
transfers = {}
with open('stop_directory.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    for row in csv_reader:
        print(row)
        transfers[row[0]] = []
        try:
            transfers_data[row[1]+row[2]].append(row[0])
        except:
            transfers_data[row[1]+row[2]] = []
            transfers_data[row[1]+row[2]].append(row[0])

print("transfers_data:")
print(transfers_data)
print("==================================================================================")
print("transfers:")
print(transfers)
print("==================================================================================")

for key, value in transfers_data.items():
    print(key, '->', value)
    currVals = value.copy()
    removals = value.copy()
    while len(currVals) > 0:
        currVal = currVals[0]
        currVals.remove(currVal)
        removals.remove(currVal)
        print("---", currVal, "->", removals)
        transfers[currVal] = removals
        removals = value.copy()

print(transfers)
# with open('test.csv', 'a') as f:
#     for key, value in transfers.items():
#         retStr = key + ","
#         retStr += str(value)
#         retStr = retStr.translate({ord(i): None for i in "[]' "})
#         retStr = retStr.strip(",")
#         print(retStr)
#         f.write(retStr)

with open('test.csv', 'w', newline='') as write_obj:
    csv_writer = csv.writer(write_obj)
    for key, value in transfers.items():
        if key == "Stop ID":
            retVals = ['Stop ID', 'Transferable Stops']
        else:
            retVals = value
            retVals.insert(0, key)
        print(retVals)
        csv_writer.writerow(retVals)
