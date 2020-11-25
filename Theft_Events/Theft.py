"""
Created on Tue Nov 24 14:27:17 2020

@author: Mika, Christian 
"""

import pandas as pd 
import json
import requests

#initializing locations from WPRDC csv file
#return: list of locations of all bike racks 
def findLocations():
    bike_locations = pd.read_csv("bike_rack_locations.csv")
    bike_locations_loc = bike_locations[['Longitude', 'Latitude']]
    return bike_locations_loc

#API call- returns theft count:   
def theftCount(loc):
    parameters = {
        'stolenness' : 'proximity', 
        'location' : loc, 
        'distance' : '1'}
    response = requests.get(
        "https://bikeindex.org:443/api/v3/search/count",
        params = parameters)
    if response.status_code== 200:
        data = json.loads(response.content.decode('utf-8'))
    return(data['proximity'])

#returns all theft counts by bike rack location
def allTheft(all_locs):
    thefts_store = []
    for i in range(len(all_locs)):
        longitude_start = locations.iloc[i][0]
        latitude_start = locations.iloc[i][1]
        api_loc = str(latitude_start) + ',' + str(longitude_start)
        thefts = theftCount(api_loc)
        thefts_store.append(thefts) 
    return thefts_store

#returns proportion of each rack's thefts relative to total 
def proportionTheft(rack_locs_wthefts):
    prop_store = []
    for i in range(len(rack_locs_wthefts)):
        thefts_loc = rack_locs_wthefts.iloc[i][2]
        prop = thefts_loc / totalThefts
        prop_store.append(prop)
    return prop_store

#returns group designation for each rack relative to proportion
def propGroups(locations, min, max, third):
    groups = []
    for i in range(len(locations)):
        prop = locations.iloc[i][3]
        if prop <= (min + third):
            groups.append('Low')
            print("here")
        if prop > (min + third) and prop <= (max - third):
            groups.append('Medium')
        if prop > (max - third):
            groups.append('High')
    return groups

locations = findLocations()
locations_thefts = locations.copy(deep=True)
thefts = allTheft(locations)
locations_thefts["Thefts"] = thefts
totalThefts = locations_thefts["Thefts"].sum()
props = proportionTheft(locations_thefts)
locations_thefts["Proportion"] = props
locations_thefts.sort_values(by='Proportion', inplace=True, ascending=False)
prop_min = locations_thefts["Proportion"].min()
prop_max = locations_thefts["Proportion"].max()
interval = prop_max - prop_min
interval_third = interval/3 
prop_groups = propGroups(locations_thefts, prop_min, prop_max, interval_third)
locations_thefts["Group"] = prop_groups 
print(locations_thefts[["Latitude","Longitude","Group"]])





