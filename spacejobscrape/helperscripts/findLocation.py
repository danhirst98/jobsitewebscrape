#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  5 16:02:47 2019

@author: DanHirst
"""

import requests
import json
import country_converter as coco
from spacejobscrape.helperscripts.JobClasses import Location
import time

def findLocation(locstr):
    """
    Converts a string of location into a Location object

    :param locstr: location, in any format (str)
    :return: Location object with country, state and city separated (Location object)
    """

    #Uses Location IQ API call to convert string to standardised format
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

    #Tries 5 times in case code encounters a rate limit
    for i in range(5):
        response = json.loads(requests.get(url, params=data).text)

        #Tests for whether request limit or other error has happened with LocationIQ. Tries again after sleeping to overcome rate limits
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
                    #TODO: change exit calls to Error calls and handle as needed.
                    exit(405)
                else:
                    print("LocationIQ returned unknown error %s." % str(response["error"]))
                    exit(405)
        break
                
    #Isolates important information to create Location object
    address = response[0]["address"]
    city = address["city"]
    state = address["state_code"]
    country = coco.convert(names=address["country_code"], to='ISOnumeric')
    
    return Location(country,state.upper(),city)

def findLocations(loclist):
    """
    Iterates through list of locations and converts all to Location objects

    :param loclist: list of location strings (list of strings)
    :return: List of Location objects
    """
    #If loclist is only one str, converts to list to keep code going
    if type(loclist)==str:
        loclist = list(loclist)

    #Removes any repeating locations to minimise number of required findLocation calls
    locset = set(loclist)

    locdict = {}
    starttime = time.time()
    for locstr in locset:
        #Converts str to Location obj
        loc = findLocation(locstr)
        locdict[locstr] = loc

        #Identifies time taken to perform API call. Can only call twice a second so limits the number of function calls to 1 every 0.5 secs
        endtime = time.time()
        timediff = endtime-starttime
        if timediff<0.5:
            time.sleep(0.5-timediff)
        starttime = endtime

    #replaces each str in loclist with the corresponding Location object
    for i in range(len(loclist)):
        loclist[i] = locdict[loclist[i]]
    
    return loclist