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
    nextStop = 0 # reference to next stop's node'

    def __init__(self, stopID, neighborhood, station_name, line, transfers, latitude, longitude):
        self.stopID = str(stopID)
        self.neighborhood = neighborhood
        self.station_name = station_name
        self.line = line
        self.transfers = transfers
        self.latitude = latitude
        self.longitude = longitude
        
    def setNextStop(self, next):
        self.nextStop = next
        return
    
    def setPrevStop(self, prev):
        self.prevStop = prev
        return

    def getNextStop(self, next):
        return self.nextStop
    
    def getPrevStop(self, prev):
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
        self.system = 0 # TBD, Dictionary of Routes (Stop Order) 
        self.total_stops = len(directory)  # Total node(stops) in the search space

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
            _latitude = data[5]
            _longitude = data[6]
            directory_dict[_stopID] = Stop(_stopID, _neighborhood, _station_name, _train, _transfers, _latitude, _longitude)
        # print(directory_dict)
        return directory_dict

    def __str__(self):
        return 'Thank you for riding with the MTA New York City Transit!'

mta = Subway_System(directory_data, transfers_data, stop_order_data)
