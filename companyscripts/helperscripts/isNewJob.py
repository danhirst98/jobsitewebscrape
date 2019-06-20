#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 23:07:32 2019

@author: DanHirst
"""
from numpy import loadtxt
from companyscripts.helperscripts.JobClasses import Job
from pathlib import Path
import os

    
def isNewJob(job):
    if type(job)!=Job:
        raise TypeError("isNewJob must have argument of type job")
    
    basefile = "JobSiteWebscrape"
    path=os.path.abspath(__file__)
    path = path.split(basefile)[0]+basefile+"/"
    
    idlistname = path+"idlists/%s-idlist.txt" % str(job.company.name)
    
    config = Path(idlistname)
    #If file does not exists, make file and add first id
    if not config.is_file():
        return True
    else:
        idlist = loadtxt(idlistname,dtype=str)
        if str(job.id) in idlist:
            return False
        else:
            return True