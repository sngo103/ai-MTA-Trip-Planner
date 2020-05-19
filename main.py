# Team Wish Upon A*
# Samantha Ngo, Daniel Rozenzaft, Anton Goretsky
# CSCI 35000 - Artificial Intelligence
# AI MTA Trip Planner: Main A* Algorithm and Driver File
# 2020-05-18

from queue import PriorityQueue
from subway_system import Subway_System
import sys, math

def main():
    if len(sys.argv) != 1:
        sys.exit("---Incorrect usage. Must be 'python main.py'")

    directory_data, transfers_data, stop_order_data, mta = initialize_system()
    print("=====================================================================")
    print(" AI MTA TRIP PLANNER by Team Wish Upon A*")
    print("=====================================================================")
    print("Welcome, user, my name is AI Greg! I'm here to help you get to where you're going.\n")
    print("First, do you need accessible stations? Type Yes or No. Then press Enter.")
    accessible = input().strip()
    while(not(accessible.lower() == "yes" or accessible.lower() == "no")):
        print("Sorry, I didn't understand that. Please type exactly Yes or No. Then press Enter.")
        accessible = input()
    if accessible.lower() == "yes":
        accessible = True
    elif accessible.lower() == "no":
        accessible = False
    start_walking = []
    end_walking = []
    print("\nGreat, now what is your starting point? You can type the address or name of a place.")
    print("Not sure what the name is? Enter what you know, we'll figure it out.")
    start = input().strip()
    startNodes = mta.findStop(start, accessible)
    if startNodes == []:
        try:
            print("\nLet me try and figure out what station you mean...")
            start_walking = mta.startToStation(start)
            start = mta.directory[start_walking["nearest_station"]]
            print("I estimated your start station to be", '(', start.station_name, ')', start.line)
        except:
            sys.exit("Sorry, I cannot figure out what your start point is. Please try a different query.")
    else:
        print("Which of these do you mean? Please select one by inputting its index.")
        possibleStarts = list(map(lambda x: x.station_name + " (" + x.line + ")", startNodes))
        for i in range(len(possibleStarts)):
            print(i, ":", possibleStarts[i])
        try:
            startIndex = int(input().strip())
        except:
            startIndex = input().strip()
        while((not isinstance(startIndex, int)) or (not (startIndex < len(possibleStarts) and startIndex > -1))):
            print("Sorry, I didn't get that. Please try again.")
            print("Which of these do you mean? Please select one by inputting its index.")
            for i in range(len(possibleStarts)):
                print(i, ":", possibleStarts[i])
            startIndex = int(input().strip())
        start = startNodes[startIndex]
        print("Starting Point:", possibleStarts[startIndex])
    print("Okay, now what is your ending point? You can type the address or name of a place.")
    print("Not sure what the name is? Enter what you know, we'll figure it out.\n")
    end = input().strip()
    endNodes = mta.findStop(end, accessible)
    if endNodes == []:
        try:
            print("Let me try and figure out what station you mean...")
            end_walking = mta.stationToEnd(end)
            end = mta.directory[end_walking["nearest_station"]]
            print("I estimated your end station to be", end.station_name, end.line)
        except:
            sys.exit("Sorry, I cannot figure out what your start point is. Please try a different query.")
    else:
        print("\nWhich of these do you mean? Please select one by inputting its index.")
        possibleEnds = list(map(lambda x: x.station_name + " " + x.line + " Train", endNodes))
        for i in range(len(possibleEnds)):
            print(i, ":", possibleEnds[i])
        try:
            endIndex = int(input().strip())
        except:
            endIndex = input().strip()
        while((not isinstance(endIndex, int)) or (not (endIndex < len(possibleEnds) and endIndex > -1))):
            print("Sorry, I didn't get that. Please try again.")
            print("Which of these do you mean? Please select one by inputting its index.")
            for i in range(len(possibleEnds)):
                print(i, ":", possibleEnds[i])
            endIndex = int(input().strip())
        end = endNodes[endIndex]
        print("Ending Point:", possibleEnds[endIndex])
    print("\nThank you! Give me one moment. Calculating...")
    directions = route(start, end, mta, accessible)
    print("...done! Here are your directions:")
    try:
        for item in start_walking["walking_instructions"]:
            if '[' not in item and '-' not in item:
                print(excludeTags(item))
            #print(item)
    except:
        pass
    print(directions)
    try:
        for item in end_walking["walking_instructions"]:
            if '[' not in item and '-' not in item:
                print(excludeTags(item))
            #print(item)
    except:
        pass
    print("\nHave a safe trip!\n")

    # # Start to Station Usage:
    # print(mta.startToStation("Knapp Street Pizza"))
    # print()
    # # Station to End Usage:
    # print(mta.stationToEnd("Kinkun Books"))
    return True

def initialize_system():
    # Stop Directory
    #stop_order: connects line names to routes
    directory_data = open('stop_directory.csv','r').read().split('\n')
    # Transfers Directory
    transfers_data = open('stop_transfers.csv', 'r').read().split('\n')
    #Stop Order Directory
    stop_order_data = open('stop_order.csv', 'r').read().split('\n')

    mta = Subway_System(directory_data, transfers_data, stop_order_data)

    return directory_data, transfers_data, stop_order_data, mta


def route(start, end, mta, accessibility):
    # start = mta.findStop(start, accessibility)
    # end = mta.findStop(end, accessibility)

    if not start or not end:
        sys.exit("\nNo station with the specified name was found. Please try again, or contact an administrator.'")

    start.end = end
    end.end = end

    # Initialize Frontier and Explored History
    frontier = PriorityQueue()
    frontier.put(start)
    explored = set()

    while not frontier.empty():
        # Pop from pqueue
        currentStop = frontier.get()

        # Might be used to not double print transfer stations
        # if currentStop.line != direc.line

        # Add current stop to explored
        explored.add(currentStop.stopID)

        # If it's not the starting stop
        if currentStop.lastVisited:
            # Add all transfers of last visited stop to explored.
            for stop in currentStop.lastVisited.transfers:
                explored.add(stop.stopID) # Isn't allowed to expand transfers of last visited stop(s)

        # Goal Test, also traces back the route
        if end == currentStop and end.station_name == currentStop.station_name:
            #trace back route
            route = '\n\nArrive at: ' + end.station_name + ' (' + currentStop.line + ')\n'
            while currentStop != start:
                route = currentStop.line + ', ' + currentStop.station_name + ', ' + str(currentStop.transferCount) + ', ' + str(currentStop.heuristic(start, end)) + '\n' + route
                currentStop = currentStop.lastVisited
            start = currentStop
            route = '\n\n\nStart at: ' + start.station_name + ' (' + start.line + ')\n\n\n' + 'Intermediate Stops:\n\n' + route
            return route

        # Get neighbors: nextStop, prevStop, transfers
        neighbor_dirs = []
        if currentStop.nextStop:
            neighbor_dirs.append(currentStop.nextStop)
        if currentStop.transfers: #Already a list, so we can concatenate
            neighbor_dirs += currentStop.transfers
        if currentStop.prevStop:
            neighbor_dirs.append(currentStop.prevStop)

        #Add unexplored neighbors to frontier
        for direc in neighbor_dirs:
            if direc.stopID not in explored:
                direc.start = start
                direc.end = end
                direc.lastVisited = currentStop #Set last visited stop for each unexplored neighbor
                #update transferCount
                if currentStop.line != direc.line and direc != start and direc != end:
                    direc.transferCount = currentStop.transferCount + 1
                else:
                    #print (str(start) + ', ' + str(currentStop) + ', ' + str(direc))
                    direc.transferCount = currentStop.transferCount
                #update stopsToEnd if neighbor and end lines are the same
                direc.stopsToEnd = mta.transferStopsToEnd(direc)

                if accessibility and direc in currentStop.transfers:
                    transferVal = direc.heuristic(start, end)
                    if (direc.accessibility == 'BOTH' or direc.prevStop and direc.accessibility == 'DOWNTOWN' and direc.prevStop.heuristic(start, end) < transferVal
                        or direc.nextStop and direc.accessibility == 'UPTOWN' and direc.nextStop.heuristic(start,end) < transferVal):
                        frontier.put(direc)

                frontier.put(direc)

    #You should never get here
    print("Impossible or Something Broke...")
    print (start)
    print (end)
    return None

def excludeTags(s):
    clean_str = ''
    exclude = False
    for i in range(len(s)):
        if s[i] == '<':
            exclude = True

        elif s[i] == '>':
            exclude = False
        
        elif not exclude:
            if i > 0 and s[i].isupper() and s[i-1].islower():
                clean_str += '. '
            clean_str += s[i]

    return clean_str.replace('&nbsp;', ' ')

if __name__ == "__main__":
    main()