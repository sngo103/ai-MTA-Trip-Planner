# This file contains functions for the following APIs:
# - Google Maps

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

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
print("GEOCODE RESULT:", geocode_result)

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
print("REVERSE GEOCODE RESULT:", reverse_geocode_result)

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)
print("Directions RESULT:", directions_result)
