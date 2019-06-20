#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  5 16:02:47 2019

@author: DanHirst
"""

import requests
import json
import country_converter as coco
from companyscripts.helperscripts.JobClasses import Location
import time

def findLocation(locstr):
    url = "https://us1.locationiq.com/v1/search.php"
    #BUG: If job is in CA, LocationIQ reads as Canada. Can add countrycodes, but am right now just appending USA to the end is working fine. 
    data = {
        'key': 'f44315769abf5d',
        'q': str(locstr),
        'format': 'json',
        'normalizecity':'1',
        'addressdetails':'1',
        'statecode':'1'
        }
    
    for i in range(5):
        response = json.loads(requests.get(url, params=data).text)
        
        if type(response)==dict:
            if "error" in response:
                if response["error"]=="Rate Limited Second":
                    print("LocationIQ second rate limit exceeded. Trying again in 1 second...")
                    time.sleep(1)
                    continue
                elif response["error"]=="Rate Limited Minute":
                    print("LocationIQ minute rate limit exceeded. Trying again in 1 minute...")
                    time.sleep(60)
                    continue
                elif response["error"]=="Rate Limited Day":
                    print("LocationIQ day rate limit exceeded. Try again in a day, and find a way to reduce requests in future.")
                    exit(0)
                else:
                    print("LocationIQ returned unknown error %s." % str(response["error"]))
                    exit(0)
        break
                
    #Add checks if there is no response
    address = response[0]["address"]
    city = address["city"]
    state = address["state_code"]
    country = coco.convert(names=address["country_code"], to='ISOnumeric')
    
    return Location(country,state.upper(),city)

def findLocations(loclist):
    if type(loclist)==str:
        loclist = list(loclist)
    locset = set(loclist)
    locdict = {}
    for locstr in locset:
        loc = findLocation(locstr)
        locdict[locstr] = loc
    for i in range(len(loclist)):
        loclist[i] = locdict[loclist[i]]
    
    return loclist