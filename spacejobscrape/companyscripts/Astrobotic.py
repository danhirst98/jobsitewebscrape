'''
Date Created: July 10, 2019 12:34 pm
Author: JJ Fiedler
'''

import requests
import re
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import spacejobscrape.helperscripts.JobClasses as JC
from spacejobscrape.helperscripts.writeXML import createjoblist

def runScrape(verbose,upload,alljobs,timeout):
    #Sets the company for the script. Change each company
    company = JC.Company(8, "Astrobotic", "https://www.astrobotic.com/", "contact@astrobotic.com")

    #Uses webdriver and chromedriver to get html from javascript
    chromedriver = "/Users/JJ/Documents/ProgrammingStuff/chromedriver"
    driver = webdriver.Chrome(chromedriver)
    driver.get("https://www.astrobotic.com/careers")
    html = driver.execute_script("return document.documentElement.outerHTML")
    page_content = BeautifulSoup(html, "html.parser")
    jobContainer = page_content.findAll("div", attrs={"class":"rbox-opening-li"})
    driver.close()

    #Creates list of titles, locations and links to the application website
    titles = []
    locations = []
    links = []

    for job in jobContainer:
        title = job.find("a", attrs={"class":"rbox-opening-li-title"}).text
        location = job.find("div", attrs={"class":"rbox-job-shortdesc"}).text
        link = job.find("a", attrs={"class":"rbox-opening-li-title"})["href"]

        #Removing information not necessary for location (i.e. Full-time, Location:, etc)
        if location.find("Location") != -1 or location.find("Full-time") != -1 or location.find("Contract") != -1:
            if location.find("Full-time")==54:
                location = location[13:54]
            elif location.find("Full-time")==29:
                location = location[13:29]
            elif location.find("Full-time")==25:
                location = location[13:25]
            else:
                location = location[13:54]

        titles.append(title)
        locations.append(location)
        links.append(link)

    print("There are %s jobs to scrape. Starting scrape..." % str(len(links)))


    # Visits each job page and scrapes further info
    descriptions = []
    for i in range(len(links)):
        page_link = links[i]

        #Getting jobID from page links
        jobID = ""
        jobIDList = re.findall("\d", page_link)

        for num in jobIDList:
            jobID = jobID + num

        #Editing the description link
        descLink = "https://app.recruiterbox.com/widget/4972/opening/%s/" % (jobID)

        page_response = requests.get(descLink, timeout=timeout)
        jsonData = json.loads(page_response.content)
        page_content = BeautifulSoup(jsonData["description"], "html.parser")
        descContainer = page_content.findAll("p") + page_content.findAll("li")

        for par in descContainer:
            desc = par.text
            descriptions.append(desc)

        title = str(titles[i])
        print("Job %s scraped - %s" % (str(i + 1), str(title)))

    createjoblist(titles, locations, descriptions, company)
    return True
