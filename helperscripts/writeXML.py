#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 18:40:34 2019

@author: DanHirst
"""

import xml.etree.ElementTree as ET
from slug import slug
from datetime import datetime
from companyscripts.helperscripts.JobClasses import Job
from companyscripts.helperscripts.isRepeatJob import isRepeatJob
from companyscripts.helperscripts.isNewJob import isNewJob
import os
from companyscripts.helperscripts.indent import indent

#TODO: Figure out how to make writejob and updatejob independent of an element. Will make the subsequent code more versatile

def writejob(element,job):
        
    if type(job)!=Job:
        raise TypeError("Argument job must be type Job")
        
    #Creation of job xml format
    jobel = ET.SubElement(element,'job')
    
    #add each subelement to the xml
    ET.SubElement(jobel,'id').text = str(job.id)
    ET.SubElement(jobel,'employer_id').text = str(job.company.id)    
    ET.SubElement(jobel,'company_name').text = str(job.company.name)    
    ET.SubElement(jobel,'company_url').text = str(job.company.url)    
    ET.SubElement(jobel,'company_email').text = str(job.company.email)  
    ET.SubElement(jobel,'job_title').text = str(job.title)    
    ET.SubElement(jobel,'job_slug').text = slug(str(job.company.name)+str(job.title)+str(job.startdate))    
    ET.SubElement(jobel,'job_description').text = ET.CDATA(job.desc)   
    ET.SubElement(jobel,'job_country').text = str(job.location.country)    
    ET.SubElement(jobel,'job_state').text = str(job.location.state)    
    ET.SubElement(jobel,'job_city').text = str(job.location.city)  
    ET.SubElement(jobel,'job_created_at').text = str(job.startdate)    
    ET.SubElement(jobel,'job_expires_at').text = str(job.enddate)
    ET.SubElement(jobel,'is_active').text = str(job.active) 
    job.approved = 0
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
       
    return
 
def updateJob(element,job):
    job.approved = 1
    jobel = ET.SubElement(element,'job')    
    ET.SubElement(jobel,'id').text = str(job.id)
    ET.SubElement(jobel,'job_expires_at').text = str(job.enddate)
    ET.SubElement(jobel,'is_active').text = str(job.active) 
    ET.SubElement(jobel,'is_approved').text = str(job.approved)    
    return


def writeXML(joblist):
    #Initial job elements
    wpjb = ET.Element('wpjb')
    jobelement = ET.SubElement(wpjb,'jobs')
    
    #allows 1 job to be made into XML by passing list
    if joblist is Job:
        joblist = [joblist]
        
    for job in joblist:
        if isRepeatJob(job):
            continue
        elif not isNewJob(job):
            updateJob(jobelement,job)
        else:
            writejob(jobelement,job)
    
    #Write XML file
    today = datetime.today().strftime('%Y-%m-%d-%H.%M.%S')
    tree = ET.ElementTree(wpjb)
    root = tree.getroot()
    xmlpretty = root
    indent(xmlpretty)
    
    #TODO: See if we can remove this. It's not pretty and if we change the name of the base directory stuff starts going tits up
    basefile = "spacejobscrape"
    
    path=os.path.abspath(__file__)
    path = path.split(basefile)[0]+basefile+"/"
    
    #UNCOMMENT IF YOU WANT TO SEE XML - FOR DEBUGGING
    #ET.dump(xmlpretty)
    newfilename = "%s-%s-IMPORT.xml" % (str(job.company.name),str(today))
    file = open("%s/%s/%s" % (path,"XML",newfilename),"w")
    file.write(ET.tostring(xmlpretty).decode())
    
    #Adds the file to another folder that displays only the XMLs from the most recent run of main.py
    file = open("%s/%s/%s" % (path,"recentXML",newfilename),"w")
    file.write(ET.tostring(xmlpretty).decode())
        
    print("Finished writing XML, saved to %s" % newfilename)
    
    companyset = set([job.company.name for job in joblist])
    for company in companyset:
        os.rename("%s/%s-newidlist.txt" % (path,company),"%s/idlists/%s-idlist.txt" % (path,company))

#TODO: Write function that adds all the jobs no matter if they are in the previous idlist




