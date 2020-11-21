import pandas as pd 
import requests
from bs4 import BeautifulSoup

#initializing locations from WPRDC csv file
#return: list of locations of all bike racks 
def findLocations():
    bike_locations = pd.read_csv("bike_rack_location.csv")
    bike_locations_loc = bike_locations[['Longitude', 'Latitude']]
    return bike_locations_loc

#finding directions between input start and end coordinates 
#params: long_start, lat_start: starting coordinates; 0 index column in findLocations() is long
#params: long_end, lat_end: ending coordiantes
#return: list of directions 
def getDirections(long_start, lat_start, long_end, lat_end):
    page = requests.get("https://www.mapquest.com/directions/list/1/near-" + str(lat_start) + ","
                        + str(long_start) + "/to/near-" + str(lat_end) + "," + str(long_end))
    page.raise_for_status()
    soup = BeautifulSoup(page.content, 'html.parser')
    narrative = soup.find(id="primaryPanel")
    directions = narrative.find("ol").getText()
    directions_format = directions.split("\n")
    directions_format = [i for i in directions_format if i]
    return directions_format 


locations = findLocations()
longitude_start = locations.iloc[0][0]
latitude_start = locations.iloc[0][1]
longitude_end = locations.iloc[1][0]
latitude_end = locations.iloc[1][1]
directions = getDirections(longitude_start, latitude_start, longitude_end, latitude_end)
#could add this to function getDirections(...)
for i in directions:
    print(i)

