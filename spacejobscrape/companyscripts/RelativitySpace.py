'''
Date Created: July 4, 2019 1:09 pm
Author: JJ Fiedler
'''

from bs4 import BeautifulSoup
import requests
import json
from spacejobscrape.helperscripts.JobClasses import Company
from spacejobscrape.helperscripts.writeXML import createjoblist

def runScrape(verbose,upload,alljobs,timeout):
    # Sets the company for the script. Change each company
    company = Company(5,"Relativity Space","www.relativityspace.com","None")

    company_careers_url = "https://boards.greenhouse.io/embed/job_board?for=relativity&b=https%3A%2F%2Fwww.relativityspace.com%2Fcareers"
    page_response = requests.get(company_careers_url, timeout=timeout)
    page_content = BeautifulSoup(page_response.content, "html.parser")

    jobContainer = page_content.findAll("div", attrs={"class":"opening"})

    # Creates list of titles, locations and links to the application website
    titles = []
    links = []
    locations = []

    for jobs in jobContainer:
        title = jobs.a.text
        location = jobs.span.text
        link = jobs.a["href"]

        titles.append(title)
        links.append(link)
        locations.append(location)

    print("There are %s jobs to scrape. Starting scrape..." % str(len(links)))

    #Visits each job page and scrapes further info
    descriptions = []
    for i in range(len(links)):
        page_link = links[i]
        page_response = requests.get(page_link)
        page_content = BeautifulSoup(page_response.content, "html.parser")

        descContainer = page_content.findAll("script", attrs={"type": "application/ld+json"})

        descJSON = json.loads(descContainer[0].text)

        descContent = BeautifulSoup(descJSON["description"], "html.parser")
        descContainer_2 = descContent.findAll("p")
        descContainer_3 = descContent.findAll("div")

        if descContainer_2[0].text == "Team and Role Overview":
            desc = descContainer_2[1].text
            if (str(descContainer_2[1]))=="<p> </p>":
                desc = descContainer_3[0].text
                descriptions.append(desc)
            else:
                descriptions.append(desc)
        else:
            try:
                if descContainer_3[0].text[0:4]=="Team":
                    if (str(descContainer_3[1]))=="<div> </div>":
                        desc = descContainer_3[2].text
                        descriptions.append(desc)
                    else:
                        desc = descContainer_3[1].text
                        descriptions.append(desc)
            except IndexError:
                continue

    createjoblist(titles, locations, descriptions, company)
    return True







