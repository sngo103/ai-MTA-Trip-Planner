from csv import reader
import csv
import pandas

# df = pandas.read_csv('stop_directory.csv')
# print(df)
# new_vals = ["NEITHER"] * 740
# df.insert(8, "Accessibility", new_vals)
# df.to_csv('new_stop_directory.csv', index=False)

# # Fix indices in stop_directory.csv:
# # df = pandas.read_csv('new.csv')
# # print(df)
# # df = df.drop(['Stop ID'], axis=1)
# # df.to_csv('stop_directory.csv', index=True)
#
# # Generate transfers_directory
# transfers_data = {}
# transfers = {}
# with open('stop_directory.csv', 'r') as read_obj:
#     csv_reader = reader(read_obj)
#     for row in csv_reader:
#         #print(row)
#         transfers[row[0]] = []
#         if row[5] != '-1' and row[6] != '-1':
#             try:
#                 transfers_data[row[5]+row[6]].append(row[0])
#             except:
#                 transfers_data[row[5]+row[6]] = []
#                 transfers_data[row[5]+row[6]].append(row[0])
#
# # print("transfers_data:")
# # print(transfers_data)
# # print("==================================================================================")
# # print("transfers:")
# # print(transfers)
# # print("==================================================================================")
#
# for key, value in transfers_data.items():
#     # print(key, '->', value)
#     currVals = value.copy()
#     removals = value.copy()
#     while len(currVals) > 0:
#         currVal = currVals[0]
#         currVals.remove(currVal)
#         removals.remove(currVal)
#         # print("---", currVal, "->", removals)
#         transfers[currVal] = removals
#         removals = value.copy()
#
# # print(transfers)
# # with open('test.csv', 'a') as f:
# #     for key, value in transfers.items():
# #         retStr = key + ","
# #         retStr += str(value)
# #         retStr = retStr.translate({ord(i): None for i in "[]' "})
# #         retStr = retStr.strip(",")
# #         print(retStr)
# #         f.write(retStr)
#
# with open('stop_transfers.csv', 'w', newline='') as write_obj:
#     csv_writer = csv.writer(write_obj)
#     for key, value in transfers.items():
#         if key == "Stop ID":
#             retVals = ['Stop ID', 'Transferable Stops']
#         else:
#             retVals = value
#             retVals.insert(0, key)
#         # print(retVals)
#         csv_writer.writerow(retVals)


# # ! BROKEN : Set all coordinates to those from geocode api ============================================================================================
# import sys
# import json
# import googlemaps
# from datetime import datetime
#
# try:
#     file = open("api_key.txt")
#     api_key = file.readline()
#     file.close()
# except:
#     sys.exit("No api_key.txt found.")
# gmaps = googlemaps.Client(key=api_key)
#
# geo_results = gmaps.geocode(address="Brighton Beach Q Train Subway Station, Brooklyn", components={'administrative_area': 'NY','country': 'US'}, bounds={'northeast': {'lat': 40.9175771, 'lng': -73.70027209999999}, 'southwest': {'lat': 40.4773991, 'lng': -74.25908989999999}})
# print(geo_results)
#
# f = open('new_new_directory.csv', 'a')
#
# with open('stop_directory.csv', 'r') as read_obj:
#     csv_reader = reader(read_obj)
#     for row in csv_reader:
#         # print(row)
#         if row[0] != 'Stop ID':
#             _address = row[2] + " " + row[3] + " Subway Train Station, "
#             if row[1] in ["Brighton", "4 Avenue", "Broadway Jamaica", "Canarsie", "Franklin", "Sea Beach", "West End", "Crosstown", "Culver", "Fulton", "Clark", "Eastern Parkway", "New Lots", "Nostrand"]:
#                 _address += "Brooklyn"
#             elif row[1] in ["Astoria", "Myrtle", "Archer Av", "Liberty", "Queens Boulevard", "Rockaway", "Flushing"]:
#                 _address += "Queens"
#             elif row[1] in ["Broadway", "Nassau", "63rd Street", "6 Avenue", "8 Avenue", "Broadway-7th Ave", "Lenox", "Lexington", "2 Avenue"]:
#                 _address += "Manhattan"
#             elif row[1] in ["Concourse", "Dyre Av", "Jerome", "Pelham", "White Plains Road"]:
#                 _address += "The Bronx"
#             else:
#                 print("Missing Borough")
#                 sys.exit()
#             geo_results = gmaps.geocode(address=_address, components={'administrative_area': 'NY','country': 'US'}, bounds={'northeast': {'lat': 40.9175771, 'lng': -73.70027209999999}, 'southwest': {'lat': 40.4773991, 'lng': -74.25908989999999}})
#             try:
#                 latitude = str(geo_results[0]["geometry"]["location"]["lat"])
#                 longitude = str(geo_results[0]["geometry"]["location"]["lng"])
#                 station_name = geo_results[0]["address_components"][0]["long_name"]
#             #print(station_name, ": LAT(", latitude, ") LONG(", longitude, ")")
#             except:
#                 latitude = "Unknown"
#                 longitude = "Unknown"
#                 station_name = "Unknown"
#                 print(geo_results)
#             #print(station_name, ": LAT(", latitude, ") LONG(", longitude, ")")
#             if station_name != row[2]:
#                 print(row[0] + ":|" + station_name + "|!=|" + row[2])
#                 input()
#                 entry = row[0] + "," + row[1] + "," + row[2] + "," + row[3] + "," + row[4] + "," + latitude + "," + longitude + "\n"
#             else:
#                 entry = row[0] + "," + row[1] + "," + row[2] + "," + row[3] + "," + row[4] + "," + latitude + "," + longitude + "\n"
#             #print("New Entry:", entry)
#             f.write(entry)
#         else:
#             f.write(row[0] + "," + row[1] + "," + row[2] + "," + row[3] + "," + row[4] + "," + row[5] + "," + row[6] + "\n")
