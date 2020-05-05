# This file contains functions for the following APIs:
# - Google Maps: https://googlemaps.github.io/google-maps-services-python/docs/index.html#

import sys
import googlemaps
from datetime import datetime

try:
    file = open("api_key.txt")
    api_key = file.readline()
    file.close()
except:
    sys.exit("No api_key.txt found.")
gmaps = googlemaps.Client(key=api_key)

# Sample Code
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
print("Directions from", param_origins, "to", param_dests, "leaving at", str(param_depart_time))
print(distance_test)
