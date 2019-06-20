#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 23:03:52 2019

@author: DanHirst
"""

from numpy import loadtxt
from pathlib import Path
from spacejobscrape.helperscripts.JobClasses import Job
import os


def isRepeatJob(job):
    if type(job)!=Job:
        raise TypeError("isRepeatJob must have argument of type job")
    
    basefile = "spacejobscrape"
    path=os.path.abspath(__file__)
    path = path.split(basefile)[0]+basefile+"/"
    
    newidlistname = path+"%s-newidlist.txt" % str(job.company.name)
    config = Path(newidlistname)
    #If file does not exists, make file and add first id
    if not config.is_file():
        open(newidlistname,"a+").write("%s\n" % str(job.id))
        return False
    idlist = loadtxt(newidlistname,dtype=str)
    if str(job.id) in idlist:
        return True
    else:
        open(newidlistname,"a+").write("%s\n" % str(job.id))
        return False