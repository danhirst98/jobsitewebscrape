#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 18:40:34 2019

@author: DanHirst
"""

from slug import slug
from datetime import datetime
from spacejobscrape.helperscripts.JobClasses import Job
from spacejobscrape.helperscripts.isRepeatJob import isRepeatJob,addJobToIDList
from spacejobscrape.helperscripts.isNewJob import isNewJob
import os
from spacejobscrape.helperscripts.indent import indent
from spacejobscrape.helperscripts.findLocation import findLocations
from lxml import etree as ET


def createjoblist(title,location,desc,company,tags=[],metas=[]):
    """
    Converts lists of raw data into job objects for XML creation.

    :param title: list of job titles (list of strings)
    :param location: list of locations (list of strings)
    :param desc: list of job descriptions (with HTML formatting) (list of strings)
    :param company: list of companies (list of Company objects)
    :param tags: list of Tags such as job type and category (list of Tag Objects)
    :param metas: list of Meta objects
    :return: void
    """
    location_refactored = findLocations(location)
    joblist = []
    for i in range(len(title)):
        newJob = Job(title[i],desc[i],company,location_refactored[i],tags,metas,3)
        joblist.append(newJob)
    writeXML(joblist,True)
    return


def writejob(job):
    """
    Converts job object into XML for upload into WPJobBoard

    :param job: job object
    :return: Job formatted as XML (lxml.etree.Element object)
    """
    if type(job)!=Job:
        raise TypeError("Argument job must be type Job")
        
    #Creation of job xml format
    jobel = ET.Element('job')
    
    #add each subelement to the xml
    ET.SubElement(jobel,'id').text = str(job.id)
    ET.SubElement(jobel,'employer_id').text = str(job.company.id)    
    ET.SubElement(jobel,'company_name').text = str(job.company.name)    
    ET.SubElement(jobel,'company_url').text = str(job.company.url)    
    ET.SubElement(jobel,'company_email').text = str(job.company.email)  
    ET.SubElement(jobel,'job_title').text = str(job.title)    
    ET.SubElement(jobel,'job_slug').text = slug(str(job.company.name)+str(job.title)+str(job.startdate))
    ET.SubElement(jobel,'job_description').text = ET.CDATA(str(job.desc))
    ET.SubElement(jobel,'job_country').text = str(job.location.country)
    ET.SubElement(jobel,'job_state').text = str(job.location.state)    
    ET.SubElement(jobel,'job_city').text = str(job.location.city)  
    ET.SubElement(jobel,'job_created_at').text = str(job.startdate)    
    ET.SubElement(jobel,'job_expires_at').text = str(job.enddate)
    ET.SubElement(jobel,'is_active').text = str(job.active) 
    ET.SubElement(jobel,'is_approved').text = str(job.approved)
    ET.SubElement(jobel,'is_filled').text = str(job.filled)    
    ET.SubElement(jobel,'is_featured').text = str(job.feat)   
    
    #Only add tags to XML if tags are present
    if job.tags:
        tags = ET.SubElement(jobel,'tags')
        #For each tag in list, add subelement
        for tg in job.tags:
            tag = ET.SubElement(tags,'tag')
            ET.SubElement(tag,'type').text = str(tg.type)
            ET.SubElement(tag,'title').text = str(tg.title)
            ET.SubElement(tag,'slug').text = slug(str(tg.title))
   
    if job.metas:
        metas = ET.SubElement(jobel,'metas')
        for mt in job.metas:
            #For each meta in list, add subelement
            meta = ET.SubElement(metas,'meta')
            ET.SubElement(meta,'name').text = str(mt.name)
            ET.SubElement(meta,'value').text = str(mt.value)
    return jobel
 
def updateJob(job):
    """
    Adds only barebones information to keep the job active and approved for job.daysactive days

    :param job: Job object
    :return: Job formatted as XML (lxml.etree.Element object)
    """
    job.approved = 1
    jobel = ET.Element('job')
    ET.SubElement(jobel,'id').text = str(job.id)
    ET.SubElement(jobel,'job_expires_at').text = str(job.enddate)
    ET.SubElement(jobel,'is_active').text = str(job.active) 
    ET.SubElement(jobel,'is_approved').text = str(job.approved)    
    return jobel


def writeXML(joblist, alljobs):
    """
    Iterates through jobs to create a single XML file with all job information for WPJobBoard upload

    :param joblist: list of Jobs for conversion (list of Job objects)
    :param alljobs: whether we should update jobs (False) or treat them all as new jobs (True) (boolean)
    :return: void
    """
    #Initial job elements
    wpjb = ET.Element('wpjb')
    jobelement = ET.SubElement(wpjb,'jobs')


    #allows 1 job to be made into XML by passing list
    if joblist is Job:
        joblist = [joblist]

    if (alljobs==True):
        for job in joblist:
            wpjb.append(writejob(job))
            addJobToIDList(job)
    else:
        for job in joblist:
            if isRepeatJob(job):
                continue
            elif not isNewJob(job):
                wpjb.append(updateJob(job))
            else:
                wpjb.append(writejob(job))
    
    #Write XML file
    today = datetime.today().strftime('%Y-%m-%d-%H.%M.%S')
    tree = ET.ElementTree(wpjb)
    root = tree.getroot()

    newfilename = "%s-%s-IMPORT.xml" % (str(job.company.name),str(today))
    file = open("./spacejobscrape/%s/%s" % ("XML",newfilename),"w")
    file.write(ET.tostring(root).decode())
    
    #Adds the file to another folder that displays only the XMLs from the most recent run of __main__.py
    file = open("./spacejobscrape/%s/%s" % ("recentXML",newfilename),"w")
    file.write(ET.tostring(root).decode())
        
    print("Finished writing XML, saved to %s" % newfilename)
    companyset = set([job.company.name for job in joblist])
    for company in companyset:
        os.rename("./spacejobscrape/%s-newidlist.txt" % (company),"./spacejobscrape/idlists/%s-idlist.txt" % (company))

    return





