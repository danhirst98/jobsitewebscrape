#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 11:51:31 2019

@author: DanHirst
"""
from bs4 import BeautifulSoup
import requests
import spacejobscrape.helperscripts.JobClasses as JC
from spacejobscrape.helperscripts.writeXML import createjoblist
from spacejobscrape.helperscripts.tags import getTags
from spacejobscrape.helperscripts.metas import getMetas

def runScrape(timeout=10):
    #Sets the company for the script. Change each company
    company = JC.Company(2,"Astranis","www.astranis.com","test@astranis.com")



    page_link = 'https://jobs.lever.co/astranis'
    page_response = requests.get(page_link, timeout=timeout)

    page_content = BeautifulSoup(page_response.content, "html.parser")

    alljobswebpage = page_content.findAll('div',attrs={"class":"posting"})


    #Creates list of titles, locations and links to the application website
    titles = []
    locations = []
    links = []
    for job in alljobswebpage:
        link= job.a["href"]
        title = job.h5.text
        location = job.find('span',attrs={"class":"sort-by-location"}).text
        #TODO: Add a check to see if they add a country code. Especially if Astranis expands beyond America
        location = location + ', USA'
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

        desc = str(page_content.find('div',{"class":"content"}))

        tags = getTags()
        metas = getMetas()

        descriptions.append(desc)
        print("Job %s scraped - %s" % (str(i+1),str(title)))

    createjoblist(titles,locations,descriptions,company,tags,metas)
    return True


if __name__=="__main__":
    runScrape()