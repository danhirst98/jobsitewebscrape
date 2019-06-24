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

    #1. Initialise Company Object, with all the information needed to attach to a job page.
    #1.5. Go into Wordpress and create a company account for this company. Most important is the company id
    company = JC.Company(0,"Company Name","www.companyurl.com","Company Email")
    print("Scraping %s..." % company.name)

    #2. Add URL of the company's career page
    company_careers_url = 'https://www.companyname.com/careers'

    page_response = requests.get(company_careers_url, timeout=timeout)
    page_content = BeautifulSoup(page_response.content, "html.parser")

    #3. Identify the parts of the webpage that have all the job information on.
    #If purely HTML, it will probably be some sort of list of <div> with an identifying class, which you can find through the findAll function
    #If the website uses JavaScript, then the process will be a bit more complicated
    jobPostingsOnWebpage = page_content.findAll('div',attrs={"class":"posting"})


    #Creates list of titles, locations and links to the application website
    titles = []
    locations = []
    links = []
    for job in jobPostingsOnWebpage:
        #4. From the HTML objects, separate the link to the job, the job title, and the location (if it is there)
        link= job.a["href"]
        title = job.h5.text
        location = job.find('span',attrs={"class":"sort-by-location"}).text

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

        #4. Identify the job description, and isolate it. Include the HTML formatting (we use it to keep the job pretty on our site)
        desc = str(page_content.find('div',{"class":"content"}))

        tags = getTags()
        metas = getMetas()

        descriptions.append(desc)
        print("Job %s scraped - %s" % (str(i+1),str(title)))

    createjoblist(titles,locations,descriptions,company,tags,metas)


if __name__=="__main__":
    runScrape()