import pandas as pd
df = pd.read_csv('station_data.csv')

print(df)

#rows are stations

#df.drop(condition)

def stopsThere(rowID, train):
    
    #maximum of 12 trains at one station (times square - 42 st)
    for routeID in range(12):
        if df.iat[rowID, routeID] == train:
            return True
    return False


def getTrain(rowID, routeID):
    return pd.at[rowID, 'Route'+routeID]


def getStops(dfr, train):
    for station in range(len(df)):
        if not stopsThere(station, train):
            #print (df.loc[station, 'Station Name'])
            #print (df.index[station] == station)
            df = df.drop(station)#, inplace = False)
    print(df)

#badData = df[df

getStops(df, 'B')

