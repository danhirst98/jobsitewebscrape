#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 21:53:49 2019

@author: DanHirst
"""

import hashlib
from datetime import datetime, timedelta


class Job:
    """
    Object for organising all qualities required for a job.

    Keyword arguments:
    title -- name of job (str)
    desc -- description of job, with html formatting (str)
    company -- company of the job (Company object)
    location -- location of job (Location object)
    tags -- tags of job, including job type and category (list of Tag objects)
    metas -- metas associated with job (list of Meta objects)
    daysactive -- number of days you want the job to be active on the website (int)
    """

    def __init__(self, title, desc, company, location, tags, metas, daysactive):

        # Checks for correct type of input
        if type(title) != str:
            raise TypeError("Wrong input type for job title. Must be str. Was type %s" % type(title))
        if type(desc) != str:
            raise TypeError("Wrong input type for job description. Must be str. Was type %s" % type(desc))
        if type(company) != Company:
            raise TypeError("Wrong input type for job company. Must be Company. Was type %s" % type(company))
        if type(location) != str and type(location) != Location:
            raise TypeError(
                "Wrong input type for job location. Must be string or Location. Was type %s" % type(location))
        if type(daysactive) != int:
            raise TypeError("Wrong input type for job daysactive. Must be int. Was type %s" % type(daysactive))

        # Input to create hash to keep track of duplicate positions
        hashinput = str(title) + str(company.name) + str(desc) + str(location.city)

        # Converts hashinput into hash of 4 bytes (up to around 4 billion)
        self.id = int(hashlib.blake2b(bytes(hashinput, encoding='utf8'), digest_size=4).hexdigest(), 16)
        self.title = title
        self.desc = desc
        self.company = company
        self.location = location
        # Makes startdate today
        self.startdate = datetime.today().strftime('%Y-%m-%d')
        # Makes enddate today+daysactive
        self.enddate = (datetime.today() + timedelta(days=daysactive)).strftime('%Y-%m-%d')
        self.active = 1
        self.approved = 0
        self.filled = 0
        self.feat = 0
        self.tags = tags
        self.metas = metas


# TODO: Add check to see if string says "Remote". If it is, add a 'remote' tag
class Location:
    """
    Object to identify the location of a job

    Keyword arguments:
    country -- country where job is located (str)
    state -- State where job is located (str, ISO3166 2-letter codes - AK,CA etc)
    city -- City where job is located (str)
    """

    def __init__(self, country, state, city):
        if type(city) != str or type(state) != str or (type(country) != str and type(country) != int):
            raise TypeError(
                "Wrong input type for Location. State and City must be string, Country must be a string or ISO3166 Numeric code (int)")

        self.city = city
        self.state = state
        self.country = country


class Company:
    """
    Object to identify company advertising a job

    Keyword arguments:
    cid -- Company id. Unique ID associated with each company for the WPJobBoard database (int)
    name -- Company name (str)
    url -- Company website url (not url for the specific job) (url)
    email -- Contact email for enquiries about the job (str)
    """

    def __init__(self, cid, name, url, email):
        if type(cid) != int or type(name) != str or type(url) != str or type(email) != str:
            raise TypeError("Wrong input type for Company. Id must be int and name, url and email must be strings")
        self.id = cid
        self.name = name
        self.url = url
        self.email = email


# TODO: Finish Tag creation and identity
class Tag:
    def __init__(self, tagtype, title):
        self.type = tagtype
        self.title = title


# TODO: Finish Meta creation and identity
class Meta:
    def __init__(self, name, value):
        self.name = str(name)
        self.value = str(value)
