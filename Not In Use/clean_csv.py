import pandas as pd
import math

df = pd.read_csv('station_data.csv')

df = df.drop_duplicates()
df.reset_index(drop = True, inplace = True)
print (df)


#df2 = df.copy()
transferCSV = ''

n = len(df)

def checkNAN(n):
    return len(str(df.at[i, 'Route' + str(n)])) == 1

def getLine(n):
    return str(df.at[i, 'Route' + str(n)])

for i in range(n):
    df.at[i, 'Free Crossover'] = checkNAN(2)

    if df.at[i, 'Free Crossover']:
        transferCSV += str(i) + ','
        
        #RouteN in station_data.csv stops at N = 12
        j = 1
        #print (str(i) + '; ' + str(checkNAN(j)))
        while checkNAN(j) and j <= 12:
            transferCSV += getLine(j) + ','
            j += 1
        transferCSV = transferCSV[:-1]
        transferCSV += '\n'



df.to_csv('stations.csv', index = False)#, index_label = 'StationID')

f = open('transfers2.csv', 'w')
f.write(transferCSV)
f.close()

