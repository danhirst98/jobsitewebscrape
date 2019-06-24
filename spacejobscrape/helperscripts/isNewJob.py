#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 23:07:32 2019

@author: DanHirst
"""
from numpy import loadtxt
from spacejobscrape.helperscripts.JobClasses import Job
from pathlib import Path

    
def isNewJob(job):
    """
    Checks whether job was in the previous run of the webscrape script
    :param job: Job object
    :return: whether job was scraped when the script ran the last time (boolean)
    """

    if type(job)!=Job:
        raise TypeError("isNewJob must have argument of type job")

    
    idlistname = "./spacejobscrape/idlists/%s-idlist.txt" % str(job.company.name)


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