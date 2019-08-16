'''
Date Created: August 16, 2019 3:57 pm
Author: JJ Fiedler
'''

from bs4 import BeautifulSoup
import requests
import json
import spacejobscrape.helperscripts.JobClasses as JC
from spacejobscrape.helperscripts.writeXML import createjoblist

def runScrape(verbose,upload,alljobs,timeout):
    # Sets the company for the script. Change each company
    company = JC.Company(17, "Odyssey Space Research", "https://www.odysseysr.com/", "None")

    page_link = 'https://www.odysseysr.com/jm-ajax/get_listings/'
    page_response = requests.get(page_link)
    json_content = json.loads(page_response.content)
    page_content = BeautifulSoup(json_content["html"], "html.parser")
    jobContainer = page_content.findAll("a")

    #Creates list of titles, locations and links to the application website
    titles = []
    locations = []
    links = []

    for job in jobContainer:
        title = job.find("h3").text
        location = job.find("div", attrs={"class":"location"}).text.strip()
        link = job["href"]

        titles.append(title)
        locations.append(location)
        links.append(link)

    print("There are %s jobs to scrape. Starting scrape..." % str(len(links)))

    # Visits each job page and scrapes further info
    descriptions = []
    for i in range(len(links)):
        page_link = links[i]
        page_response = requests.get(page_link)
        page_content = BeautifulSoup(page_response.content, "html.parser")
        desc = page_content.find("div", attrs={"class":"job_description"}).text

        title = str(titles[i])

        descriptions.append(desc)
        print("Job %s scraped - %s" % (str(i + 1), str(title)))

    createjoblist(titles,locations,descriptions,company)
    return True