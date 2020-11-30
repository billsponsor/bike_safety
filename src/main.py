"""
Created on Tue Nov 24 14:27:17 2020
@author: Jamila, Kumar, Mika, Christian 
"""

import pandas as pd 
import json
import requests
from geopy import distance
from geopy.geocoders import Nominatim


def welcome():
    print('Welcome to Bike Safe!')
    print('Give us your address and we will tell you where to park your bike!')

#return weather info based on the bike rack lat and long
def Weather(): 
    APIkey='845bf124b058d7198bdf344ea6d5d46d'
    #API call and format response as json
    headers = {'Content-Type': 'application/json'}
    url = 'http://api.openweathermap.org/data/2.5/weather?lat=40.440624&lon=-79.9959&''appid='+APIkey
    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))    
        #extract relevant info
        for line in data:
            weather= dict(data['weather'][0]) #weather description
            #tempinfo=(data['main'])#all temp info
            temp=(((data['main']['feels_like'])-273.15)* 9/5 + 32)
            #Kelvin to Farenheit: (285.27 - 273.15) * 9/5 + 32
        print('Current weather in downtown Pittsburgh: %s, temperature %.2f F'%(weather['description'],temp))

#Get user input- current and destination addresses
def getAddresses():
    CurrentAddress = input("Enter current address (number, street name): ")
    atLocation = input("Is your current address same as destination (Y/N):")
    if atLocation == 'Y':
        destAddress = CurrentAddress
    else:
        destAddress = input("Enter destination address (number, street name): ")
    return(destAddress)

# Get user input- type of coverage
def coverageType():
    choice = input('Enter where do you want to park your bike\n Outdoor, Indoor, or No Preference:')
    if choice == 'Outdoor':
        choice = 'Outdoor'
    elif choice == 'Indoor':
        choice = 'Indoor/Covered'
    else:
        choice = 'NP'
    return (choice)

def addtoLoc(destAddress):    
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.geocode(destAddress+',Pittsburgh')
    destCoor=(location.longitude,location.latitude)
    return destCoor

#take coordinates and return bike rack lat/long within a .25 mile radius and if inside or outside
   
def rackLoc(destCoor,choice): 
    racks_df = pd.read_csv('bike_rack_location.csv')
    racks_df = racks_df[['Longitude', 'Latitude', 'Weather Coverage']] 
    Distance = []
    for i in racks_df.index: 
        point = [str(racks_df['Longitude'][i]) , str(racks_df['Latitude'][i])]
        dist = distance.distance(destCoor, point).feet
        Distance.append(dist)
    racks_df['Distance'] = Distance
    if choice == 'NP':
        return(racks_df[racks_df['Distance'] <= 1320])
    else: 
        racks_df = racks_df[racks_df['Weather Coverage'] == choice]
        return(racks_df[racks_df['Distance'] <= 1320])

#initializing locations from WPRDC csv file
#return: list of locations of all bike racks 
def findLocations(destCoor):
    bike_locations = pd.read_csv("bike_rack_location.csv")
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


