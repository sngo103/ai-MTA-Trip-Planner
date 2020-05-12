import numpy as np

# Stop Directory
#stop_order: connects line names to routes
directory_data = open('stop_directory.csv','r').read().split('\n')

# Transfers Directory
transfers_data = open('stop_transfers.csv', 'r').read().split('\n')


class Subway_System():

    def __init__(self, directory, transfers):
        self.transfers = self.set_tails(transfers) # Dictionary: key stopID -> value list of transferable stops
        self.directory = self.set_tails(directory) # Array of Stop Nodes
        self.total_stops = len(directory)  # Total node(stops) in the search space

        #self.boroughs = ['Manhattan'] # Boroughs included in the search space
        #set this up later
        #self.total_lines = len(stop_order)
        #self.line_starts = [] # Array of pointers to start nodes for each line
        #self.stop_order = self.set_tails(stop_order_data)
        #self.id_name = self.set_tails(id_name_data)
        #self.transfers = self.set_tails(transfers_data)

    # Sets up data
    # Makes a dictionary where the keys are 'head' of each line and the 'tails' are the end of each line
    def set_tails(self, dataSet):
        routeDict = {}
        #for line in stop_order:
        for line in dataSet:
            #print (stop_order['Line'])
            thisLine = line.split(',')
            routeDict[thisLine[0]] = thisLine[1:]
        return routeDict

    def __str__(self):
        return 'Thank you for riding with the MTA New York City Transit!'

    #methods to write
    def findSurroundingStops(self, stopID):
        #temporary
        return (-1, -1)

'''test_subway_system = Subway_System()
print(test_subway_system)
print(test_subway_system.stops)'''

class Stop(Subway_System):
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

    def __init__(self, stopID):
        #do we really need all these initializing variables? they're all
        #accessible via the data set. shouldn't just stopID be enough?

        super(Subway_System, self).__init__() # Need parameters?
        mta = Subway_System(directory_data, transfers_data)
        self.stopID = str(stopID)

        my_directory = mta.directory[stopID]
        my_transfers = mta.transfers[stopID]

        self.neighborhood = my_directory[0]
        self.station_name = my_directory[1]
        self.line = my_directory[2]
        self.transfers = my_transfers
        self.latitude = my_directory[4]
        self.longitude = my_directory[5]
        
        surroundingStops = self.findSurroundingStops(stopID)
        self.prevStop = surroundingStops[0]
        self.nextStop = surroundingStops[1]

    def __str__(self):
        return self.stopID + ': ' + self.station_name + ', ' + self.line


brighton = Stop('48')
print(brighton)

# Datasets
# 1. All the stations in order: stopID, Line