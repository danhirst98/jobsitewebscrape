#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 11:51:31 2019

@author: DanHirst
"""
from bs4 import BeautifulSoup
import requests

from spacejobscrape.helperscripts.JobClasses import Company
from spacejobscrape.helperscripts.writeXML import createjoblist

def runScrape(timeout=10):
    #Sets the company for the script. Change each company
    company = Company(1,"SpaceX","www.spacex.com","elon@spacex.com")



    page_link = 'https://www.spacex.com/careers/list/robots.txt'
    page_response = requests.get(page_link, timeout=timeout)
    page_content = BeautifulSoup(page_response.content, "html.parser")

    oddJobs = page_content.findAll('tr',attrs={"class":"odd"})
    evenJobs = page_content.findAll('tr',attrs={"class":"even"})

    #Creates list of titles, locations and links to the application website
    titles = []
    locations = []
    links = []
    for job in oddJobs and evenJobs:
        link= job.a["href"]
        title = job.a.text
        location = job.findAll("div", {"class": "field-name-field-job-location"})[0].text

        titles.append(title)
        locations.append(location)
        links.append(link)

    print("There are %s jobs to scrape. Starting scrape..." % str(len(links)))


    #Visits each job page and scrapes further info
    descriptions = []
    for i in range(len(links)):
        page_link = links[i]
        page_response = requests.get(page_link, timeout=timeout)
        page_content = BeautifulSoup(page_response.content, "html.parser")

        title = str(titles[i])

        desc = str(page_content.find('div',{"id":"content"}))
        descriptions.append(desc)
        print("Job %s scraped - %s" % (str(i+1),str(title)))

    createjoblist(titles,locations,descriptions,company)
    return True

if __name__=="__main__":
    runScrape(10)
