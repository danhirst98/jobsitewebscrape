'''
Date Created: July 7, 2019 10:54 pm
Author: JJ Fiedler
'''

import requests
from bs4 import BeautifulSoup
import spacejobscrape.helperscripts.JobClasses as JC
from spacejobscrape.helperscripts.writeXML import createjoblist

def runScrape(verbose,upload,alljobs,timeout):
    #Sets the company for the script. Change each company
    company = JC.Company(6, "Rocket Lab", "www.rocketlabusa.com", "None")

    page_link = 'https://www.rocketlabusa.com/careers/positions/'
    page_response = requests.get(page_link, timeout=timeout)
    page_content = BeautifulSoup(page_response.content, "html.parser")

    jobsContainer = page_content.findAll("a", attrs={"class":"job"})

    #Creates list of titles, locations and links to the application website
    titles = []
    locations = []
    links = []

    for jobs in jobsContainer:
        title = jobs.h3.text
        location = jobs.h5.text
        link = "https://www.rocketlabusa.com" + jobs["href"]

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

        desc = page_content.find("div", attrs={"class", "job__info-subtitle"}).text
        descriptions.append(desc)

        title = str(titles[i])

        print("Job %s scraped - %s" % (str(i + 1), str(title)))

    createjoblist(titles, locations, descriptions, company)
    return True
