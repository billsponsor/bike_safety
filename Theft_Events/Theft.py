"""
Created on Tue Nov 24 14:27:17 2020

@author: Mika
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

#Get locaiton and set to string
locations = findLocations()
longitude_start = locations.iloc[0][0]
latitude_start = locations.iloc[0][1]
api_loc = str(latitude_start) + ',' + str(longitude_start)
  
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

#Test functionality: 
print(theftCount(api_loc))



