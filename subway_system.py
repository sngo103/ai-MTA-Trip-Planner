# Team Wish Upon A*
# Samantha Ngo, Daniel Rozenzaft, Anton Goretsky
# CSCI 35000 - Artificial Intelligence
# AI MTA Trip Planner: Class Structure
# 2020-05-18

import math, random
import sys
import json
import googlemaps
import api
from datetime import datetime

# Stop Class, a.k.a. the Node
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
    express = ""
    accessibility = ""

    #heuristic uses the number of times the algorithm has "transferred"
    #and the number of stops left to the goal if the current and ending stops are on the same line
    transferCount = 0
    #initialized as a large number to encourage staying on a train that stops at the goal stop
    stopsToEnd = 100

    def __init__(self, stopID, neighborhood, station_name, line, transfers, latitude, longitude, express, accessibility):#, current_state):
        self.stopID = str(stopID)
        self.neighborhood = neighborhood
        self.station_name = station_name
        self.line = line
        self.transfers = transfers # List of stopIDs that can be transfered it
        self.latitude = latitude
        self.longitude = longitude
        self.express = express
        self.accessibility = accessibility

    def setNextStop(self, next):
        self.nextStop = next
        return

    def setPrevStop(self, prev):
        self.prevStop = prev
        return

    def setTransfers(self, transfers_list):
        self.transfers = transfers_list
        return

    def getTransferLines(self):
        #find available line transfers
        transferLines = []
        for transfer in self.transfers:
            transferLines.append(transfer.line)
        return transferLines

    def getNextStop(self):
        return self.nextStop

    def getPrevStop(self):
        return self.prevStop

    def __str__(self):
        return '[' + self.stopID + ': ' + self.station_name + ', ' + self.line + ']'

    # Comparisons for heuristic + priority queue
    def __lt__(self, stop2):

        myVal = self.heuristic(self.start, self.end)
        otherVal = stop2.heuristic(stop2.start, stop2.end)

        return (myVal < otherVal)

    # Will involve measurement of distance to the landmark

    def __eq__ (self, stop2):
        #stops are equal if they have the same stopID
        a = stop2.stopID == self.stopID

        #b is not included in measurement for start evaluation, since the transfers of stop are not equally good
        '''c = self.startEval and stop2.startEval
        if c:
            return a'''

        #a stop is as good as it's transfers when we're not evaluating a starting stop
        b = False
        for stop in range(len(self.transfers)):
            if self.transfers[stop].stopID == stop2.stopID:
                b = True
        return a or b

    def checkEndStop(self, end):
        if self == end:
            return -100000000
        return 0

    def checkEndLines(self, end):
        if self.line in end.getTransferLines():
            return -50
        return 0

    def localOrExpress(self):
        if self.express == 'express':
            return -25
        return 25

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
        return 50 * totalDist + 50 * self.transferCount + self.checkEndStop(end) + self.checkEndLines(end) + 20 * self.stopsToEnd + 6 * self.localOrExpress() + 2 * (100 - self.stopsToEnd) * self.localOrExpress()

    def __hash__(self):
        return hash(str(self))

# =========================================================================================================================================================
# Initialization Data
# Stop Directory: connects line names to route details
directory_data = open('stop_directory.csv','r').read().split('\n')
# Transfers Directory: connections stopIDs to available transfers at the same location
transfers_data = open('stop_transfers.csv', 'r').read().split('\n')
#Stop Order Directory: connects line names to stops they visit
stop_order_data = open('stop_order.csv', 'r').read().split('\n')

# Subway System Class
class Subway_System():
    def __init__(self, directory, transfers, train_lines):
        self.transfers = self.setupTransfers(transfers) # Dictionary: key stopID -> value list of transferable stops
        self.directory = self.setupDirectory(directory) # Dictionary of Stop Nodes: key stopID -> Stop Node
        self.system = self.setupSystem(train_lines)  # Dictionary of Routes : Stop Order
        self.addNodeTransfers()
        self.addPrevNext()
        self.total_stops = len(self.directory) # Total node(stops) in the search space
        try:
            file = open("api_key.txt")
            api_key = file.readline()
            file.close()
        except:
            sys.exit("No api_key.txt found.")
        self.gmaps = googlemaps.Client(key=api_key)

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
            if line != "Stop ID,Neighborhood,Station Name,Line,canTransfer,Latitude,Longitude,Express,Accessibility":
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
                _express = data[7]
                _accessibility = data[8]
                directory_dict[_stopID] = Stop(_stopID, _neighborhood, _station_name, _train, _transfers, _latitude, _longitude, _express, _accessibility)
        return directory_dict

    def setupSystem(self, stop_order):
        # Associated with stop_order
        # {line : list of stops in correct order (south -> north)}
        system_dict = {}
        train = ""
        order = []
        for line in stop_order:
            data = line.split(',')
            train = data[0]
            order = data[1:]
            #print(order)
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
        # Relate user input names into stops

        options = []
        for stop in self.directory:
            if stop_name in self.directory[stop].station_name:
                options.append(self.directory[stop])

        # Randomly choose between stations with the same name or search keyword
        if options:
            return random.choice(options)

        # Prevent inputs that are not stop names
        return False

    # Calculate the number of stops between two stations on the same line
    def stopsToEnd(self, line, stop):
        lineInd = self.idIndex(line, stop.stopID)
        endInd = self.idIndex(line, stop.end.stopID)
        if lineInd >= 0 and endInd >= 0:
            return abs(self.idIndex(line, stop.stopID) - self.idIndex(line, stop.end.stopID))

        # Function doesn't like stations on different lines
        return 100

    # Find the "index" of a given stop on a given line's route, assuming that the stop appears on its route.
    def idIndex(self, line, stopID):
        for i in range(len(self.system[line])):
            if self.system[line][i] == self.directory[stopID]:
                return i

        #Yell at programmer if the stops are on different lines
        #print ('The ' + line + ' train does not stop at ' + str(self.directory[stopID]) + '. Please try again.')
        return -1

    # Get walking directions from origin to nearest subway station
    # Params:
    # - start_addr: text query address of origin, NOT lat,long
    def startToStation(self, start_addr): # Assumes the start station is unknown
        retDict = {"start":{"address" : "", "name" : "", "latitude" : 0, "longitude" : 0},
                   "nearest_station": -1,
                   "walking_instructions" : []}
        try:
            place = self.gmaps.find_place(input=start_addr, input_type="textquery",fields=["formatted_address", "geometry", "name"], language="en", location_bias="rectangle:40.495992,-74.257159|40.915568,-73.699215")["candidates"][0]
        except:
            return {"error": "We couldn't find a place matching the address you entered. Please try again."}
        place_lat = place['geometry']['location']['lat']
        retDict["start"]["latitude"] = place_lat
        place_lng = place['geometry']['location']['lng']
        retDict["start"]["longitude"] = place_lng
        retDict["start"]["address"] = place['formatted_address']
        retDict["start"]["name"] = place['name']
        nearest = self.gmaps.places_nearby(location=[place_lat, place_lng], rank_by="distance", type="subway_station")['results'][0]
        station_name = nearest['name']
        station_lat = nearest['geometry']['location']['lat']
        station_lng = nearest['geometry']['location']['lng']
        stopID = -1
        leastDist = 1000000000
        for id, node in self.directory.items():
            dist = node.getDist(node.latitude, station_lat, node.longitude, station_lng)
            if dist < leastDist:
                leastDist = dist
                stopID = id
        retDict["nearest_station"] = stopID
        param_origin = [place_lat, place_lng]
        param_dest = [station_lat, station_lng]
        param_mode = "walking"
        param_depart_time = datetime(year=2020, month=6, day=5, hour=10, minute=0, second=0)
        param_arrive_time = 0
        retDict["walking_instructions"].append("Directions from " + start_addr + " to " + station_name + " departing at " + str(param_depart_time))
        retDict["walking_instructions"] += api.directions(origin=param_origin, destination=param_dest, mode=param_mode, depart_time=param_depart_time, arrive_time=param_arrive_time)
        return retDict

    # Get walking directions from nearest subway station to destination
    # Params:
    # - end_addr(str): text query address of destination, NOT lat,long
    def stationToEnd(self, end_addr): # End station can be known or unknown
        retDict = {"end":{"address" : "", "name" : "", "latitude" : 0, "longitude" : 0},
                   "nearest_station": -1,
                   "walking_instructions" : []}
        try:
            place = self.gmaps.find_place(input=end_addr, input_type="textquery",fields=["formatted_address", "geometry", "name"], language="en", location_bias="rectangle:40.495992,-74.257159|40.915568,-73.699215")["candidates"][0]
        except:
            return {"error": "We couldn't find a place matching the address you entered. Please try again."}
        place_lat = place['geometry']['location']['lat']
        retDict["end"]["latitude"] = place_lat
        place_lng = place['geometry']['location']['lng']
        retDict["end"]["longitude"] = place_lng
        retDict["end"]["address"] = place['formatted_address']
        retDict["end"]["name"] = place['name']
        nearest = self.gmaps.places_nearby(location=[place_lat, place_lng], rank_by="distance", type="subway_station")['results'][0]
        station_name = nearest['name']
        station_lat = nearest['geometry']['location']['lat']
        station_lng = nearest['geometry']['location']['lng']
        stopID = -1
        leastDist = 1000000000
        for id, node in self.directory.items():
            dist = node.getDist(node.latitude, station_lat, node.longitude, station_lng)
            if dist < leastDist:
                leastDist = dist
                stopID = id
        retDict["nearest_station"] = stopID
        param_origin = [station_lat, station_lng]
        param_dest = [place_lat, place_lng]
        param_mode = "walking"
        param_depart_time = datetime(year=2020, month=6, day=5, hour=10, minute=0, second=0)
        param_arrive_time = 0
        retDict["walking_instructions"].append("Directions from " + station_name + " to " + end_addr + " departing at " + str(param_depart_time))
        retDict["walking_instructions"] += api.directions(origin=param_origin, destination=param_dest, mode=param_mode, depart_time=param_depart_time, arrive_time=param_arrive_time)
        return retDict

    # Calculate the number of stops needed to the end goal, INCLUDING TRANSFERS
    def transferStopsToEnd(self, stop):
        noTransfer = self.stopsToEnd(stop.line, stop)
        endTransferLines = stop.end.getTransferLines()

        # If there's no transfer, use the single line method

        if noTransfer < 100:
            ret = noTransfer
            #print(ret)
            return ret

        # Check if you can transfer from stop to a train that stops at end
        for transfer in stop.transfers:

            # There should probably be a better way to ensure that end is set
            transfer.end = stop.end

            # If a transfer is on the same line as the goal, return the single line stops to end
            if transfer.line in endTransferLines:
                return self.stopsToEnd(transfer.line, transfer)

        # Heuristic will not prioritize taking trains that do not stop at end, or transferring at stops that lack transfers to a train that stops at end
        return 100

    def __str__(self):
        return 'Thank you for riding with the MTA New York City Transit!'
