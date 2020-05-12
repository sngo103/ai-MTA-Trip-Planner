import numpy as np


class Stop():
    # Variables
    stopID = -1
    neighborhood = ''
    station_name = ''
    line = 0
    transfers = []
    latitude = 0
    longitude = 0
    prevStop = 0 # reference to previous stop's node
    nextStop = 0 # reference to next stop's node
    lastStop = None # reference to last stop visited (set by search algorithm)

    def __init__(self, stopID, neighborhood, station_name, line, transfers, latitude, longitude):
        self.stopID = str(stopID)
        self.neighborhood = neighborhood
        self.station_name = station_name
        self.line = line
        self.transfers = transfers # List of stopIDs that can be transfered it
        self.latitude = latitude
        self.longitude = longitude
        
    def setNextStop(self, next):
        self.nextStop = next
        return
    
    def setPrevStop(self, prev):
        self.prevStop = prev
        return

    def getNextStop(self):
        return self.nextStop
    
    def getPrevStop(self):
        return self.prevStop

    def __str__(self):
        return self.stopID + ': ' + self.station_name + ', ' + self.line


''' *Working
brighton = Stop('49','Brighton','Brighton Beach','Q',[],'40.577621','-73.961376')
print(brighton)
print(brighton.prevStop)
print(brighton.nextStop)
print(brighton.transfers)
'''

# ================================================================================

# Stop Directory
#stop_order: connects line names to routes
directory_data = open('stop_directory.csv','r').read().split('\n')

# Transfers Directory
transfers_data = open('stop_transfers.csv', 'r').read().split('\n')

#Stop Order Directory
stop_order_data = open('stop_order.csv', 'r').read().split('\n')

class Subway_System():

    def __init__(self, directory, transfers, train_lines):
        self.transfers = self.setupTransfers(transfers) # Dictionary: key stopID -> value list of transferable stops
        self.directory = self.setupDirectory(directory) # Dictionary of Stop Nodes: key stopID -> Stop Node
        self.system = self.setupSystem(train_lines)  # TBD, Dictionary of Routes (Stop Order) 
        self.connectStops()
        self.total_stops = len(directory) # Total node(stops) in the search space

    def setupTransfers(self, transfers):
        transfers_dict = {}
        for line in transfers:
            data = line.split(',')
            train = data[0]
            transfer_stops = data[1:]
            transfers_dict[train] = transfer_stops
        # print("Transfers DICT:", transfers_dict)
        return transfers_dict

    def setupDirectory(self, directory):
        directory_dict = {}
        for line in directory:
            data = line.split(',') # Stop ID,Neighborhood,Station Name,Line,canTransfer,Latitude,Longitude
            _stopID = data[0]
            _neighborhood = data[1]
            _station_name = data[2]
            _train = data[3]
            _transfers = self.transfers[_stopID]
            #_transfers = _transfers
            _latitude = data[5]
            _longitude = data[6]
            directory_dict[_stopID] = Stop(_stopID, _neighborhood, _station_name, _train, _transfers, _latitude, _longitude)
        # print(directory_dict)
        return directory_dict

    def setupSystem(self, stop_order):
        # A dictionary: key train -> list of Stop nodes in the correct order
        system_dict = {}
        train = ""
        order = []
        for line in stop_order:
            data = line.split(',')
            train = data[0]
            order = data[1:]
            order = list(map(lambda x: self.directory[x], order))

            #Set previous and next stops
            for stop in range(len(order)):
                if stop < len(order)-1:
                    order[stop].setNextStop(order[stop+1])
                    #print('Set Next Stop: ' + str(order[stop+1]))
                else:
                    order[stop].setNextStop(None)

                if stop > 0:
                    order[stop].setPrevStop(order[stop-1])
                    #print('Set Previous Stop: ' + str(order[stop-1]))
                else:
                    order[stop].setPrevStop(None)

                self.directory[order[stop]] = order[stop]
                #print(self.directory[order[stop]].nextStop)#[stop].prevStop)

                #if order[stop].station_name == '51st St':
                    #print (order[stop].prevStop)

            system_dict[train] = order

        # print("SYSTEM DICT:", system_dict)
        return system_dict

    def connectStops(self):
        for train in self.system:
            order = self.system[train]
            #for i in range(len(order)):
        return

    #Get the StopID given a station name
    def findStop(self, stop_name):
        for stop in self.directory:
            
            if stop_name in self.directory[stop].station_name:
                return self.directory[stop]

        return False

    def __str__(self):
        return 'Thank you for riding with the MTA New York City Transit!'

mta = Subway_System(directory_data, transfers_data, stop_order_data)
