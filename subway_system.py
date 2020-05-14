import math
#import random

# Subway system and stop class

class Stop():
    # Variables
    stopID = -1
    neighborhood = ''
    station_name = ''
    line = ''
    transfers = [] # List of Stop objects.
    latitude = 0
    longitude = 0
    prevStop = 0 # reference to previous stop's node
    nextStop = 0 # reference to next stop's node
    lastVisited = None # reference to last stop visited (set by search algorithm)
    #current_state = None

    #heuristic uses the number of times the algorithm has "transferred"
    #and the number of stops left to the goal if the current and ending stops are on the same line
    transferCount = 0
    #initialized as a large number to encourage staying on a train that stops at the goal stop
    stopsToGoal = 1000

    def __init__(self, stopID, neighborhood, station_name, line, transfers, latitude, longitude):#, current_state):
        self.stopID = str(stopID)
        self.neighborhood = neighborhood
        self.station_name = station_name
        self.line = line
        self.transfers = transfers # List of stopIDs that can be transfered it
        self.latitude = latitude
        self.longitude = longitude
        #self.current_state = current_state

    def setNextStop(self, next):
        self.nextStop = next
        return

    def setPrevStop(self, prev):
        self.prevStop = prev
        return

    def setTransfers(self, transfers_list):
        self.transfers = transfers_list
        return

    def getNextStop(self):
        return self.nextStop

    def getPrevStop(self):
        return self.prevStop

    def __str__(self):
        return '[' + self.stopID + ': ' + self.station_name + ', ' + self.line + ']'

    # Comparisons for heuristic + priority queue
    def __lt__(self, stop2):
        #lat2 = 40.714111
        #long2 = -74.008585
        #return self.getDist(self.latitude, stop2.latitude, self.longitude, stop2.longitude)
        #return self.getDist(self.latitude, lat2, self.longitude, long2)
        return self.heuristic(self.start, self.end) < stop2.heuristic(self.start, self.end)

    # Will involve measurement of distance to the landmark
    
    def __eq__ (self, stop2):
        a = stop2.stopID == self.stopID
        b = False
        for stop in range(len(self.transfers)):
            if self.transfers[stop].stopID == stop2.stopID:
                b = True

        return a or b

    def checkEnd(self, end):
        if self.__eq__(end):
            return -10000
        return 0

    # Apply latitude/longitude distance formula
    def getDist(self, lat1, lat2, long1, long2):
        lat1 = math.radians(float(lat1))
        lat2 = math.radians(float(lat2))
        long1 = math.radians(float(long1))
        long2 = math.radians(float(long2))

        radius = 6371

        d_long = long2 - long1
        d_lat = lat2 - lat1

        a = (math.sin(d_lat/2) ** 2) + math.cos(lat1) * math.cos(lat2) * (math.sin(d_long/2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return radius * c

    def heuristic(self, start, end):

        #totalDist = distToStart + distToGoal
        totalDist = (self.getDist(self.latitude, start.latitude, self.longitude, start.longitude) 
            + self.getDist(self.latitude, end.latitude, self.longitude, end.longitude))

        #print (totalDist + 3 * self.transferCount)
        #print (self.transferCount)

        return (totalDist + 10 * self.transferCount + self.stopsToGoal + self.checkEnd(end))

    def __hash__(self):
        return hash(str(self))

# ================================================================================

# Stop Directory
#stop_order: connects line names to routes
directory_data = open('stop_directory.csv','r').read().split('\n')

# Transfers Directory: connections stopIDs to available transfers at the same location
transfers_data = open('stop_transfers.csv', 'r').read().split('\n')

#Stop Order Directory: connects line names to stops they visit
stop_order_data = open('stop_order.csv', 'r').read().split('\n')

class Subway_System():

    def __init__(self, directory, transfers, train_lines):
        self.transfers = self.setupTransfers(transfers) # Dictionary: key stopID -> value list of transferable stops
        self.directory = self.setupDirectory(directory) # Dictionary of Stop Nodes: key stopID -> Stop Node
        self.system = self.setupSystem(train_lines)  # Dictionary of Routes : Stop Order
        self.addNodeTransfers()
        self.addPrevNext()
        self.total_stops = len(self.directory) # Total node(stops) in the search space

    def setupTransfers(self, transfers):
        # {stopID : list of transferable stops}
        transfers_dict = {}
        for line in transfers:
            data = line.split(',')
            train = data[0]
            transfer_stops = data[1:]
            transfers_dict[train] = transfer_stops
        # print("Transfers DICT:", transfers_dict)
        return transfers_dict

    def setupDirectory(self, directory):
        # { stopID : Stop object }
        directory_dict = {}
        for line in directory:
            if line != "Stop ID,Neighborhood,Station Name,Line,canTransfer,Latitude,Longitude":
                data = line.split(',') # Stop ID,Neighborhood,Station Name,Line,canTransfer,Latitude,Longitude
                _stopID = data[0]
                _neighborhood = data[1]
                _station_name = data[2]
                _train = data[3]
                _transfers = self.transfers[_stopID]
                #print("TRANSFERS:", _transfers)
                #_transfers = _transfers
                _latitude = data[5]
                _longitude = data[6]
                #current_state = Current_State('', '', 0)
                directory_dict[_stopID] = Stop(_stopID, _neighborhood, _station_name, _train, _transfers, _latitude, _longitude)#, current_state)
        return directory_dict

    def setupSystem(self, stop_order):
        #associated with stop_order
        # {line : list of stops in correct order (south -> north)} 
        system_dict = {}
        train = ""
        order = []
        for line in stop_order:
            data = line.split(',')
            train = data[0]
            order = data[1:]
            order = list(map(lambda x: self.directory[x], order))
            system_dict[train] = order

        # print("SYSTEM DICT:", system_dict)
        return system_dict

    def addNodeTransfers(self):
        # Builds out transfers instance variable (list) inside Stop nodes
        for id, node in self.directory.items():
            # print("Before:", id, "->", node.transfers)
            node.transfers = list(map(lambda x: self.directory[x], node.transfers))
            # print("After:", id, "->", node.transfers)
        return

    def addPrevNext(self):
        # Add prevStop and nextStop instance variables for all stops
        for train, order in self.system.items():
            #print("=======================================================")
            #print("Train", train, "->", order)
            #print()
            for i in range(len(order)):
                if i == 0:
                    order[i].setPrevStop(None)
                    order[i].setNextStop(order[i+1])
                elif i == len(order)-1:
                    order[i].setPrevStop(order[i-1])
                    order[i].setNextStop(None)
                else:
                    order[i].setPrevStop(order[i-1])
                    order[i].setNextStop(order[i+1])
            #for item in order:
                #print("[", item.getPrevStop(), "->", item, '->', item.getNextStop(), "]")
        return

    # Get the first StopID that matches a user-inputted station name and line
    def findStop(self, stop_name, line):
        if not line:
            for stop in self.directory:
                if stop_name in self.directory[stop].station_name:
                    return self.directory[stop]
            return False
        else:
            for stop in self.directory:
                if stop_name in self.directory[stop].station_name and line == stop.line:
                    return self.directory[stop]
            return False

            # Get the first StopID that matches a user-inputted station name

    def findStop(self, stop_name):
        for stop in self.directory:
            if stop_name in self.directory[stop].station_name:
                return self.directory[stop]
        return False

    #calculate the number of stops between two stations on the same line
    def stopsToEnd(self, line, stop):
        return abs(self.idIndex(line, stop.stopID) - self.idIndex(line, stop.end.stopID))

    #find the "index" of a given stop on a given line's route assuming that the stop appears on its route.
    def idIndex(self, line, stopID1):
        for i in range(len(self.system[line])):
            if self.system[line][i].stopID == stopID1:
                return i

        #Yell at user for bad input
        #print ('The ' + line + ' train does not stop at Stop #' + stopID1 + '. Please try again.')
        return 100000

    # calculate the number of stops needed to the end goal, INCLUDING TRANSFERS
    def transferStopsToEnd(self, stop):
        noTransfer = self.idIndex(stop.line, stop.stopID)
        endTransferLines = []

        #if there's no transfer, use the single line method
        if noTransfer < 100:
            return noTransfer

        #find lines stopping at end
        for endTransfer in stop.end.transfers:
            endTransferLines.append(endTransfer.line)

        #check if you can transfer from stop to a train that stops at end
        for transfer in stop.transfers:
            return self.stopsToEnd(transfer.line, transfer)

        #heuristic will not prioritize taking trains that do not stop at end, 
        #or transferring at stops that lack transfers to a train that stops at end
        return 100000

    def __str__(self):
        return 'Thank you for riding with the MTA New York City Transit!'

class Current_State():
    start = ''
    end = ''
    transfers_made = 0
    stops_visted = 0
    current_stop = ''
    
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.transfers_made = 0
        self.stops_visted = 0
        self.current_state = start

    def increment_transfer(self):
        self.transfer_made += 1

    def increment_stops(self):
        self.stops_visted += 1

    def update_stop(self, stop):
        self.current_stop = stop
        
    def __str__(self):
        ret = 'Start: ' + self.start.station_name + '\n'
        ret += 'End: ' + self.start.station_name + '\n'
        ret += 'Transfers Made: ' + str(self.transfers_made) + '\n'
        ret += 'Stops Visited: ' + str(self.stops_visited) + '\n'
        return ret
    