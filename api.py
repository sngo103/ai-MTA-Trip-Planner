# This file contains functions for the following APIs:
# - Google Maps: https://googlemaps.github.io/google-maps-services-python/docs/index.html#

import sys
import json
import googlemaps
from datetime import datetime

try:
    file = open("api_key.txt")
    api_key = file.readline()
    file.close()
except:
    sys.exit("No api_key.txt found.")
gmaps = googlemaps.Client(key=api_key)

# Sample Code ==================================================================
# # Geocoding an address
# geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
# #print("GEOCODE RESULT:", geocode_result)
#
# # Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
# #print("REVERSE GEOCODE RESULT:", reverse_geocode_result)
#
# # Request directions via public transit
# now = datetime.now()
# directions_result = gmaps.directions("Sydney Town Hall",
#                                      "Parramatta, NSW",
#                                      mode="transit",
#                                      departure_time=now)
# #print("Directions RESULT:", directions_result)
# ==============================================================================

# print("DISTANCE MATRIX API ==========================================================================================================================")
# DISTANCE MATRIX: Gets travel distance and time for a matrix of origins and destinations.
# - Can't specify both arrival_time and departure_time - must pick one
param_origins = ["Coney Island, Brooklyn, NY"]
param_dests = ["Atlantic Terminal, Brooklyn, NY"]
param_mode = "transit"
param_transit_mode = "subway"
param_depart_time = datetime(year=2020, month=5, day=5, hour=10, minute=0, second=0)
param_arrive_time = datetime(year=2020, month=5, day=5, hour=10, minute=25, second=0)
distance_test = gmaps.distance_matrix(origins=param_origins, destinations=param_dests, mode=param_mode,
                                     transit_mode=param_transit_mode, departure_time=param_depart_time)
# print("Distance from", param_origins, "to", param_dests, "leaving at", str(param_depart_time))
# print(distance_test)
# print()

# print("DIRECTIONS API ===============================================================================================================================")
# DIRECTIONS: Gets travel directions
# - Can't specify both arrival_time and departure_time - must pick one
# Parameters:
# - origin (string address or list[lat, long]) – 1 ONLY - The address or latitude/longitude value from which you wish to calculate directions.
# - destination (string address or list[lat, long]) - 1 ONLY - The address or latitude/longitude value from which you wish to calculate directions.
# - mode: “driving”, “walking”, “bicycling” or “transit”
# - waypoints (a single location, or a list of locations, where a location is a string, dict, list, or tuple) – Specifies an array of waypoints. Waypoints alter a route by routing it through the specified location(s).
# - alternatives (bool) – If True, more than one route may be returned in the response.
# - optimize_waypoints (bool) – Optimize the provided route by rearranging the waypoints in a more efficient order.
# - transit_mode (string or list of strings) – Specifies one or more preferred modes: “bus”, “subway”, “train”, “tram”, “rail”=[“train”, “tram”, “subway”]
# - transit_routing_preference (string) – Specifies preferences for transit requests: “less_walking” or “fewer_transfers”
def directions(origin, destination, mode="transit", depart_time=datetime.now(), arrive_time=0):
    retList = []
    if arrive_time != 0:
        directions = gmaps.directions(origin=origin, destination=destination, mode=mode, departure_time=depart_time)
        entry = "Directions from " + origin + " to " + destination + " arriving at " + str(arrive_time)
    else:
        directions = gmaps.directions(origin=origin, destination=destination, mode=mode, arrival_time=arrive_time)
        entry = "Directions from " + origin + " to" + destination + " leaving at " + str(depart_time)
    retList.append(entry)
    directions = directions[0]['legs'][0]['steps']
    #print(directions)
    for macroStep in range(len(directions)):
        if directions[macroStep]['travel_mode'] == 'WALKING':
            entry = "STEP " + str(macroStep) + ": " + directions[macroStep]['html_instructions']
            retList.append(entry)
            if 'steps' in directions[macroStep]:
                steps = directions[macroStep]['steps']
                for microStep in range(len(steps)):
                    step_dist = steps[microStep]['distance']['text']
                    step_time = steps[microStep]['duration']['text']
                    step_mode = steps[microStep]['travel_mode']
                    try:
                        step_html = steps[microStep]['html_instructions']
                        entry = "---STEP " + str(microStep) + ": " + step_html
                        retList.append(entry)
                    except:
                        entry = "---STEP " + str(microStep) + ": You have reached your destination."
        elif directions[macroStep]['travel_mode'] == 'TRANSIT':
            train = directions[macroStep]['transit_details']
            train_direction = train['headsign']
            train_line = train['line']['short_name']
            stops = train['num_stops']
            depart_stop = train['departure_stop']['name']
            arrive_stop = train['arrival_stop']['name']
            entry = "STEP " + str(macroStep) + ": Take " + train_direction + " bound " + train_line + " train " + stops + " stops from " + depart_stop + " to " + arrive_stop
        else:
            sys.exit("Not processing other modes of travel right now.")
    return retList

# param_origin = "Coney Island, Brooklyn, NY" # Can be address or coordinates
# param_waypoints = []
# param_dest = "Atlantic Terminal, Brooklyn, NY"
# param_mode = "transit"
# param_transit_mode = "subway"
# param_depart_time = datetime(year=2020, month=6, day=5, hour=10, minute=0, second=0)
# param_arrive_time = datetime(year=2020, month=6, day=5, hour=10, minute=53, second=0)
# directions(origin=param_origin, destination=param_dest, waypoints=[], mode=param_mode, transit_mode=param_transit_mode, depart_time=param_depart_time, arrive_time=param_arrive_time)
