# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 02:41:56 2020

@author: Jamila
"""

#pip install geopy - install geographic library

import json
import requests
from geopy import distance


userloc=(-79.99721507,40.44287929)#example coords, should be taken from user input

def rackLoc(userloc): #take coordinates and return bike rack lat/long within a .5 mile radius and if inside or outside
    with open ('bikerackgeocodeexport.csv','r') as f:
        coordlist=[]
        f.readline()
        for line in f:           
            coverage=(line.split(',')[7])
            coordinates=(line.split(',')[1:3])
            coordlist.append(coordinates)
            dist=distance.distance(userloc,coordinates).feet
            if dist <= 2640: #half a mile, approx. 10 min walking; we can change this
                print('%.2f feet away, %s'%(dist,coverage))
        return(coordinates)
        #can sort by distance after adding theft count
        #Should we put this into a table?
        

def Weather(coordinates): #return weather info based on the bike rack lat and long
    APIkey='845bf124b058d7198bdf344ea6d5d46d'
    lat=str(coordinates[1])
    long=str(coordinates[0])
    #API call and format response as json
    headers = {'Content-Type': 'application/json'}
    url = 'http://api.openweathermap.org/data/2.5/weather?lat='+lat+'&lon='+long+'&appid='+APIkey
    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))    
    
        #extract relevant info
        for line in data:
            weather= dict(data['weather'][0]) #weather description
#            tempinfo=(data['main'])#all temp info
            temp=(((data['main']['feels_like'])-273.15)* 9/5 + 32)
            #Kelvin to Farenheit: (285.27 - 273.15) * 9/5 + 32
        print('Current weather near this bike rack: %s, temperature %.2f F'%(weather['description'],temp))
    
