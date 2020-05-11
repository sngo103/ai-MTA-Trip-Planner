import numpy as np

#import data.csv
#id_name: connects IDs to station names
id_name = open('id_name.csv','r').read().split('\n')

#import stop order.csv
#stop_order: connects line names to routes
stop_order = open('stop order.csv','r').read().split('\n')

#import transfers.csv
transfers = open('transfers.csv','r').read().split('\n')

class Subway_System():
    def __init__(self, id_name_data, stop_order_data, transfers_data):
        self.total_stops = 119 # Total node(stops) in the search space
        self.boroughs = ['Manhattan'] # Boroughs included in the search space
        self.total_lines = len(stop_order)
        self.line_starts = [] # Array of pointers to start nodes for each line
        self.stop_order = self.set_tails(stop_order_data)
        self.id_name = self.set_tails(id_name_data)
        self.transfers = self.set_tails(transfers_data)

    # Sets up data
    # Makes a dictionary where the keys are 'head' of each line and the 'tails' are the end of each line
    def set_tails(self, dataSet):
        routeDict = {}
        #for line in stop_order:
        for line in dataSet:
            #print (stop_order['Line'])
            thisLine = line.split(',')
            routeDict[thisLine[0]] = thisLine[1:] 
        print(routeDict)        
        

test = Subway_System()
print(test.stop_order)

'''
class Stop():
    #3 data files
    #id_name: connects IDs to station names
    #stop_order: connects line names to routes
    #transfers: connects station IDs with all the trains stopping there (if there are transfers)
    
    def __init__(self, stationID):
        self.line_name = 
    
    def __init__(self, line_name='Unknown', station_name, station_id, transfers=[]):
        self.line_name = line_name
        self.station_name = station_id
        self.line_name = line_name
        self.transfers = transfers
'''

class Station(Subway_System):
    #3 data files
    #id_name: connects IDs to station names
    #stop_order: connects line names to routes
    #transfers: connects station IDs with all the trains stopping there (if there are transfers)
    
    def __init__(self, stationID, transfers=[], id_name_data, stop_order_data, transfers_data):
        super(Subway_System, self).__init__() # Need parameters?
        mta = Subway_System(id_name_data, stop_order_data, transfers_data)
        if stationID in mta.transfers:
            self.transfers = mta.transfers[stationID]
        else:
            self.transfers = []
    