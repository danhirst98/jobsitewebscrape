#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 23:03:52 2019

@author: DanHirst
"""

from numpy import loadtxt
from pathlib import Path

from spacejobscrape.helperscripts.JobClasses import Job


def addJobToIDList(job):
    """
    Adds the job to the newidlist file

    :param job: Job object
    :return: void
    """

    newidlistname = "./spacejobscrape/%s-newidlist.txt" % str(job.company.name)

    open(newidlistname, "a+").write("%s\n" % str(job.id))


def isRepeatJob(job):
    """
    Check to see if the job has been already been imported during this run of the webscrape. If not, append id to the end of the newidlist for replacement at the end of the scrape

    :param job: Job object
    :return: whether job has already been scraped in this instance of the scrape (boolean)
    """
    if type(job) != Job:
        raise TypeError("isRepeatJob must have argument of type job")

    newidlistname = "./spacejobscrape/%s-newidlist.txt" % str(job.company.name)
    config = Path(newidlistname)
    # If file does not exists, make file and add first id
    print(config.is_file())
    if not config.is_file():
        addJobToIDList(job)
        return False

    idlist = loadtxt(newidlistname, dtype=str)
    if str(job.id) in idlist:
        return True
    else:
        # Adds id to the bottom of the newidlist file
        addJobToIDList(job)
        return False
