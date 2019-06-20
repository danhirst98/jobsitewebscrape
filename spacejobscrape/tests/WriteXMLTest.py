#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 08:28:25 2019

@author: DanHirst
"""
from companyscripts.helperscripts.JobClasses import Job,Tag,Meta,Company,Location
from companyscripts.helperscripts.writeXML import writeXML



#TEST: check for XML functionality       
location = Location(840,"CA","Hawthorne")
company = Company(1,"SpaceX","www.spacex.com","elon@spacex.com")
CEO = Job("CEO","Just tweet about anime or something",company,location,[],[],3)
COO = Job("COO","Actually do all the work",company,location,[],[],3)
CFO = Job("CFO","Get money",company,location,[Tag(0,1),Tag("hello","dolly")],[Meta("hi","hello")],3)

joblist = [CEO,COO,CFO]

writeXML(joblist)
