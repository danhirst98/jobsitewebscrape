#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 18:40:34 2019

@author: DanHirst
"""

import xml.etree.ElementTree as ET
from slug import slug
from datetime import datetime,timedelta
import hashlib
from numpy import loadtxt
from os import rename

#Indent function to make XML pretty
def indent(elem, level=0):
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem       

def writejob(element,eid,cname,curl,cemail,jobtitle,jobdesc,jobcountry,jobstate,jobcity,jobzip="",jobdate=datetime.today().strftime('%Y-%m-%d'),jobexp=(datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d'),active=1,approved=0,filled=0,feat=0,tags="",metas=""):
    
    
    #Creates hash for id. If the hashinput is the same as a previous job on the site, it will overwrite. 
    
    #Can change the hash input if there are multiple jobs in the same place
    #TODO: Open up set file, check to see if hash is in table. If hash is already in table, then return without creating job. Must also create a new hash table every day to provide a new table to compare against. 
    hashinput = str(jobtitle+cname+jobdesc+jobcity)
    id = int(hashlib.sha1(hashinput.encode("ascii")).hexdigest(),16)
    newhash = open("newidlist.txt","w+")
    newhashtxt = loadtxt("newidlist.txt")
    open("idlist.txt","w+")
    hash = loadtxt("idlist.txt")
    if id in hash or id in newhashtxt:
        return

    newhash.write("%s\n" % id)

   
    
    #MASTER SCRIPT MUST CHANGE OVERWRITE OLD HASHTABLE WITH NEW, COMPLETED HASHTABLE
    
    job = ET.SubElement(element,'job')
    
    #add each subelement to the xml
    ET.SubElement(job,'id').text = str(id)
    ET.SubElement(job,'employer_id').text = str(eid)    
    ET.SubElement(job,'company_name').text = str(cname)    
    ET.SubElement(job,'company_url').text = str(curl)
    
    ET.SubElement(job,'company_email').text = str(cemail)
  
    ET.SubElement(job,'job_title').text = str(jobtitle)
    
    ET.SubElement(job,'job_slug').text = slug(str(jobtitle))
    
    ET.SubElement(job,'job_description').text = str(jobdesc)
    
    ET.SubElement(job,'job_country').text = str(jobcountry)
    
    ET.SubElement(job,'job_state').text = str(jobstate)
    
    ET.SubElement(job,'job_city').text = str(jobcity)
    
    #only add jobzip to XML if zipcode is present
    if jobzip:
        ET.SubElement(job,'job_zip_code').text = str(jobzip)
        
    ET.SubElement(job,'job_created_at').text = str(jobdate)
    
    ET.SubElement(job,'job_expires_at').text = str(jobexp)

    ET.SubElement(job,'is_active').text = str(active)
 
    ET.SubElement(job,'is_approved').text = str(approved)
    
    ET.SubElement(job,'is_filled').text = str(filled)
    
    ET.SubElement(job,'is_featured').text = str(feat)
    
    #Only add tags to XML if tags are present
    if tags:
        tags = ET.SubElement(job,'tags')
        #For each tag in list, add subelement
        for tg in tags :
            if len(tg)!=2:
                raise Exception('Wrong number of parameters for tags. Each tag must have 2 values in the list - 1 for type and 1 for title')
            tag = ET.SubElement(tags,'tag')
            ET.SubElement(tag,'type').text = str(tg[0])
            ET.SubElement(tag,'title').text = str(tg[1])
            ET.SubElement(tag,'slug').text = slug(str(tg[1]))
   
    if metas:
        metas = ET.SubElement(job,'metas')
        for mt in metas:
            #For each meta in list, add subelement
            if len(mt)!=2:
                raise Exception('Wrong number of parameters for metas. Each meta must have 2 values in the list - 1 for name and 1 for value')
            meta = ET.SubElement(metas,'meta')
            ET.SubElement(meta,'name').text = str(mt[0])
            ET.SubElement(meta,'value').text = str(mt[1])
       
 
    return
 


#BUG: If we set the length of the active days to a small value, then every day a person will have to approve every single job that is in the whole system. The solution is to create another hash table that stores all the hashes from the day before. If the hash is in the table, we will not import or we just will not approve it. This might mean we have to have a larger hashinput
def writeXML(joblist,daysactive):
    #Initial job elements
    wpjb = ET.Element('wpjb')
    jobs = ET.SubElement(wpjb,'jobs')
    
    #allows 1 job to be made into XML by passing list
    if joblist is dict:
        joblist = [joblist]
    
    
    for job in joblist:
        
        #Compulsory arguments
        eid = job['eid']
        cname = job['cname']
        curl = job['curl']
        cemail = job['cemail']
        jobtitle = job['jobtitle']
        jobdesc = job['jobdesc']
        jobcountry = job['jobcountry']
        jobstate = job['jobstate']
        jobcity = job['jobcity']
        
        #Conditional statements for non-compulsory arguments
        if 'jobzip' in job.keys():
            jobzip = job['jobzip']
        else:
            jobzip = ""
        if 'jobdate' in job.keys():
            jobdate = job['jobdate']
        else:
            jobdate=datetime.today().strftime('%Y-%m-%d')
        if 'jobexp' in job.keys():
            jobexp = job['jobexp']
        else:
            jobexp=(datetime.today() + timedelta(days=daysactive)).strftime('%Y-%m-%d')
        if 'active' in job.keys():
            active = job['active']
        else:
            active = 1
        if 'approved' in job.keys():
            approved = job['approved']
        else:
            approved = 0
        if 'filled' in job.keys():
            filled = job['filled']
        else:
            filled = 0
        if 'feat' in job.keys():
            feat = job['feat']
        else:
            feat = 0
        if 'tags' in job.keys():
            tags = job['tags']
        else:
            tags = ""
        if 'metas' in job.keys():
            metas = job['metas']
        else:
            metas = ""
    
            
        writejob(jobs,eid,cname,curl,cemail,jobtitle,jobdesc,jobcountry,jobstate,jobcity,jobzip,jobdate,jobexp,active,approved,filled,feat,tags,metas)
        
        #TODO: Remove after creating main() script and adding this function
        rename("./newidlist.txt","./idlist.txt")
        
        #Write XML file
        indent(wpjb)
        tree = ET.ElementTree(wpjb)
        tree.write("./XML/xmlwritetest1.xml")
 


#TEST: check for XML functionality       
dict = {'eid':"3",'cname':"SpaceX",'curl':"www.spacex.com",'cemail':"sugma@spacex.com",'jobtitle':"Chief Elon",'jobdesc':"youre going to be a huge Elon, cant wait",'jobcountry':"USA",'jobstate':"NC",'jobcity':"Chapel Hill",'metas':[[0,1],[1,2]]}


list = [dict,dict,dict]

writeXML(list,3)

        

