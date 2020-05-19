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
    stopID = -1        # Unique Stop ID for every stop on every train line
    neighborhood = ''  # Neighborhood it operates in
    station_name = ''
    line = ''          # Train name
    transfers = []     # List of Stop objects.
    latitude = 0
    longitude = 0
    prevStop = 0       # Reference to previous stop's node
    nextStop = 0       # Reference to next stop's node
    lastVisited = None # Reference to last stop visited (set by search algorithm)
    express = ""       # Determines whether this is an express/local train
    accessibility = "" # Determines the extent the stop is ADA accessible

    #heuristic uses the number of times the algorithm has "transferred"
    #and the number of stops left to the goal if the current and ending stops are on the same line
    transferCount = 0
    #initialized as a large number to encourage staying on a train that stops at the goal stop
    stopsToEnd = 100

    # Constructor to initialize the Stop Node
    def __init__(self, stopID, neighborhood, station_name, line, transfers, latitude, longitude, express, accessibility):
        self.stopID = str(stopID)
        self.neighborhood = neighborhood
        self.station_name = station_name
        self.line = line
        self.transfers = transfers
        self.latitude = latitude
        self.longitude = longitude
        self.express = express
        self.accessibility = accessibility

    # Mutator: changes value of this Stop Node's reference to the next Stop Node
    def setNextStop(self, next):
        self.nextStop = next
        return

    # Mutator: changes value of this Stop Node's reference to the previous Stop Node
    def setPrevStop(self, prev):
        self.prevStop = prev
        return

    # Mutator: changes value of this Stop Node's transfers list
    def setTransfers(self, transfers_list):
        self.transfers = transfers_list
        return

    # Accessor: returns reference to next Stop Node in the order defined by Subway_System's system variable
    def getNextStop(self):
        return self.nextStop

    # Accessor: returns reference to previous Stop Node in the order defined by Subway_System's system variable
    def getPrevStop(self):
        return self.prevStop

    # Returns all the possible lines to switch to:
    def getTransferLines(self):
        #find available line transfers
        transferLines = []
        for transfer in self.transfers:
            transferLines.append(transfer.line)
        return transferLines

    # Determines if this Stop Node's heuristic value is less than the given Stop Node's heuristic value
    # Comparisons for heuristic + priority queue
    def __lt__(self, stop2):

        myVal = self.heuristic(self.start, self.end)
        otherVal = stop2.heuristic(stop2.start, stop2.end)

        return (myVal < otherVal)

    # Determines if this Stop Node shares the same station as the given Stop Node parameter
    # Two Stop Nodes are "equal" if you can transfer between them without exiting the station
    def __eq__ (self, stop2):
        # Stops are also equal if they have the same stopID
        a = stop2.stopID == self.stopID
        b = False
        for stop in range(len(self.transfers)):
            if self.transfers[stop].stopID == stop2.stopID:
                b = True
        return a or b

    # Checks if this stop is the end stop/destination:
    def checkEndStop(self, end):
        if self == end:
            return -100000000
        return 0

    # Determines if this Stop's line will lead to the the end stop/destination
    def checkEndLines(self, end):
        if self.line in end.getTransferLines():
            return -50
        return 0

    # Returns a constant value based on whether it is an express or local stop to be used in the heuristic:
    def localOrExpress(self):
        if self.express == 'express':
            return -25
        return 25

    # Apply latitude/longitude distance formula to get distance between two coords
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

    # Determines the heuristic centered around this Stop Node:
    def heuristic(self, start, end):
        #totalDist = distToStart + distToGoal
        totalDist = (self.getDist(self.latitude, start.latitude, self.longitude, start.longitude)
            + self.getDist(self.latitude, end.latitude, self.longitude, end.longitude))
        return 200 * totalDist + 0 * self.transferCount + self.checkEndStop(end) + self.checkEndLines(end) + 0 * (20 * self.stopsToEnd + 6 * self.localOrExpress()) + 2 * (100 - self.stopsToEnd) * self.localOrExpress() * (100 * self.transferCount)

    # Returns the hash of this Stop Node object
    def __hash__(self):
        return hash(str(self))

    # Display Function
    def __str__(self):
        return '[' + self.stopID + ': ' + self.station_name + ', ' + self.line + ']'


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
    # Initialize components of subway system and call the necessary functions to set up the three main data variables
    def __init__(self, directory, transfers, train_lines):
        self.transfers = self.setupTransfers(transfers)       # Dictionary: key stopID -> value list of transferable stops
        self.directory = self.setupDirectory(directory)       # Dictionary of Stop Nodes: key stopID -> Stop Node
        self.system = self.setupSystem(train_lines)           # Dictionary of Routes: key trainline ->  List of Stop Nodes in order from southernmost to northernmost
        self.total_stops = len(self.directory)                # Total node(stops) in the search space
        # Changes all the stopIDs in the transfers var from ints to references to their associated Stop Nodes
        self.addNodeTransfers()
        # Determines all the prevStop and nextStop values in all the Stop Nodes in system var
        self.addPrevNext()
        # Read in API Key:
        try:
            file = open("api_key.txt")
            api_key = file.readline()
            file.close()
        except:
            sys.exit("No api_key.txt found.")
        # Set up Google Maps Client for data requests:
        self.gmaps = googlemaps.Client(key=api_key)

    # Reads transfer data into a dictionary: key stopID -> value list of transferable stops
    # Serves as a reference for what transfers are at what stations
    def setupTransfers(self, transfers):
        transfers_dict = {}
        for line in transfers:
            data = line.split(',')
            train = data[0]
            transfer_stops = data[1:]
            transfers_dict[train] = transfer_stops
        # print("Transfers DICT:", transfers_dict)
        return transfers_dict

    # Reads stop_directory data into a dictionary of Stop Nodes: key stopID -> Stop Node
    # Serves as easy access to all Stop Nodes based on stopID
    def setupDirectory(self, directory):
        directory_dict = {}
        for line in directory:
            if line != "Stop ID,Neighborhood,Station Name,Line,canTransfer,Latitude,Longitude,Express,Accessibility": # Skip Header
                data = line.split(',')
                _stopID = data[0]
                _neighborhood = data[1]
                _station_name = data[2]
                _train = data[3]
                _transfers = self.transfers[_stopID]
                _latitude = data[5]
                _longitude = data[6]
                _express = data[7]
                _accessibility = data[8]
                directory_dict[_stopID] = Stop(_stopID, _neighborhood, _station_name, _train, _transfers, _latitude, _longitude, _express, _accessibility)
        return directory_dict

    # Uses stop_order data passed in as a parameter to create the subway system "graph"
    # Result is a dictionary of Routes: key trainline ->  List of Stop Nodes in order from southernmost to northernmost
    # Serves as the search space
    def setupSystem(self, stop_order):
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

    # Changes all the stopIDs in the transfers var from ints to references to their associated Stop Nodes
    def addNodeTransfers(self):
        for id, node in self.directory.items():
            # For every stopID in transfers, replace it with its associated Stop Node from directory var:
            node.transfers = list(map(lambda x: self.directory[x], node.transfers))
        return

    # Determines all the prevStop and nextStop values in all the Stop Nodes in system var
    def addPrevNext(self):
        # For each Stop Node in system var, get the Node before and after it in its respective list
        for train, order in self.system.items():
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
        return

    # Get the first StopID that matches a user-inputted station NAME and LINE
    # Based on substrings of Stop names
    def findStop(self, stop_name, line):
        #put all of this inside if (accessible) if that is needed
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

    # Get the first StopID that matches a user-inputted station NAME only
    # Based on substrings of Stop names
    def findStop(self, stop_name):
        # Relate user input names to stops:
        options = []
        for stop in self.directory:
            if stop_name in self.directory[stop].station_name:
                options.append(self.directory[stop])
        # Randomly choose between stations with the same name or search keyword
        if options:
            return options
        # Prevent inputs that are not stop names
        return []

    # Calculate the number of stops between two stations on the same line
    def stopsToEnd(self, line, stop):
        lineInd = self.idIndex(line, stop.stopID)
        endInd = self.idIndex(line, stop.end.stopID)
        if lineInd >= 0 and endInd >= 0:
            return abs(self.idIndex(line, stop.stopID) - self.idIndex(line, stop.end.stopID))
        # Return heuristic value that disfavors stops on different lines
        return 100

    # Find the "index" of a given stop on a given line's route, assuming that the stop appears on its route.
    def idIndex(self, line, stopID):
        for i in range(len(self.system[line])):
            if self.system[line][i] == self.directory[stopID]:
                return i
        # Yell at programmer if the stops are on different lines
        return -1

    # Get walking directions from origin to nearest subway station
    # Params:
    # - start_addr: text query address of origin, NOT lat,long
    def startToStation(self, start_addr): # Assumes the start station is unknown
        retDict = {"start":{"address" : "", "name" : "", "latitude" : 0, "longitude" : 0},
                   "nearest_station": -1,
                   "walking_instructions" : []}
        # Find a place that most matches the user's inputted start address:
        try:
            place = self.gmaps.find_place(input=start_addr, input_type="textquery",fields=["formatted_address", "geometry", "name"], language="en", location_bias="rectangle:40.495992,-74.257159|40.915568,-73.699215")["candidates"][0]
        except:
            return {"error": "We couldn't find a place matching the address you entered. Please try again."}
        # Get the place's information:
        place_lat = place['geometry']['location']['lat']
        retDict["start"]["latitude"] = place_lat
        place_lng = place['geometry']['location']['lng']
        retDict["start"]["longitude"] = place_lng
        retDict["start"]["address"] = place['formatted_address']
        retDict["start"]["name"] = place['name']
        # Find the nearest train station to the start place:
        nearest = self.gmaps.places_nearby(location=[place_lat, place_lng], rank_by="distance", type="subway_station")['results'][0]
        station_name = nearest['name']
        station_lat = nearest['geometry']['location']['lat']
        station_lng = nearest['geometry']['location']['lng']
        # Get the stopID in the directory for that station:
        stopID = -1
        leastDist = 1000000000
        for id, node in self.directory.items():
            dist = node.getDist(node.latitude, station_lat, node.longitude, station_lng)
            if dist < leastDist:
                leastDist = dist
                stopID = id
        retDict["nearest_station"] = stopID
        # Get walking directions from the start address to the nearest station:
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
        # Find a place that most matches the user's inputted end address:
        try:
            place = self.gmaps.find_place(input=end_addr, input_type="textquery",fields=["formatted_address", "geometry", "name"], language="en", location_bias="rectangle:40.495992,-74.257159|40.915568,-73.699215")["candidates"][0]
        except:
            return {"error": "We couldn't find a place matching the address you entered. Please try again."}
        # Get the place's information:
        place_lat = place['geometry']['location']['lat']
        retDict["end"]["latitude"] = place_lat
        place_lng = place['geometry']['location']['lng']
        retDict["end"]["longitude"] = place_lng
        retDict["end"]["address"] = place['formatted_address']
        retDict["end"]["name"] = place['name']
        # Find the nearest train station to the destination:
        nearest = self.gmaps.places_nearby(location=[place_lat, place_lng], rank_by="distance", type="subway_station")['results'][0]
        station_name = nearest['name']
        station_lat = nearest['geometry']['location']['lat']
        station_lng = nearest['geometry']['location']['lng']
        # Get the stopID in the directory for that station:
        stopID = -1
        leastDist = 1000000000
        for id, node in self.directory.items():
            dist = node.getDist(node.latitude, station_lat, node.longitude, station_lng)
            if dist < leastDist:
                leastDist = dist
                stopID = id
        retDict["nearest_station"] = stopID
        # Get walking directions from the nearest station to the destination to the user's desired end location:
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
        # If there's no transfer, use the single line method:
        if noTransfer < 100:
            ret = noTransfer
            #print(ret)
            return ret
        # Check if you can transfer from stop to a train that stops at end:
        for transfer in stop.transfers:
            # ??? # There should probably be a better way to ensure that end is set
            transfer.end = stop.end
            # If a transfer is on the same line as the goal, return the single line stops to end:
            if transfer.line in endTransferLines:
                return self.stopsToEnd(transfer.line, transfer)
        # Heuristic will disfavor taking trains that do not stop at end, or transferring at stops that lack transfers to a train that stops at end
        return 100

    # Display
    def __str__(self):
        return 'Thank you for riding with the MTA New York City Transit!'
