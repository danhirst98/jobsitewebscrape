'''
Date Created: July 8, 2019 3:09 pm
Author: JJ Fiedler
'''

import requests
from bs4 import BeautifulSoup
import spacejobscrape.helperscripts.JobClasses as JC
from spacejobscrape.helperscripts.writeXML import createjoblist

def runScrape(verbose,upload,alljobs,timeout):
    #Sets the company for the script. Change each company
    company = JC.Company(7, "Aerospace Corporation", "https://aerospace.org/", "None")

    page_link = 'https://careers.aerospace.org/go/View-All-Jobs/2443100/?q=&sortColumn=referencedate&sortDirection=desc'
    page_response = requests.get(page_link, timeout=timeout)
    page_content = BeautifulSoup(page_response.content, "html.parser")

    #Getting base pagination links
    paginationLinks = page_content.find("ul", attrs={"class":"pagination"})
    jobLinkContainer = paginationLinks.findAll("li")

    #List to store all links
    mainLinkContainer = []

    for link in jobLinkContainer:
        jobsLink = "https://careers.aerospace.org" + link.a["href"]

        #Editing links to obtain links for all pages on website
        if jobsLink == "https://careers.aerospace.org/go/View-All-Jobs/2443100/100/?q=&sortColumn=referencedate&sortDirection=desc":
            mainLinkContainer.append(jobsLink)

            #Calculating the number of pages left
            numPagesLeft = int(((250 - 100) / 25)-1)

            #Num items on page increases by 25 starting at 125
            paginationAmount = 125

            #Editing the links
            for i in range(numPagesLeft):
                jobsLink = "https://careers.aerospace.org/go/View-All-Jobs/2443100/%s/?q=&sortColumn=referencedate&sortDirection=desc" % (str(paginationAmount))
                paginationAmount += 25

                mainLinkContainer.append(jobsLink)
        else:
            mainLinkContainer.append(jobsLink)


    #Removing duplicate links
    mainLinkContainer = list(dict.fromkeys(mainLinkContainer))

    # Creates list of titles, locations and links to the application website
    titles = []
    locations = []
    links = []

    #Start of main web scrape
    for link in mainLinkContainer:

        page_response = requests.get(link, timeout=timeout)
        page_content = BeautifulSoup(page_response.content, "html.parser")
        titleContainer = page_content.findAll("a", attrs={"class":"jobTitle-link"})
        locationContainer = page_content.select("span.jobLocation.visible-phone")

        #Removing duplicates from the list
        titleContainer = list(dict.fromkeys(titleContainer))

        for item in titleContainer:
            title = item.text
            link = "https://careers.aerospace.org" + item["href"]
            titles.append(title)
            links.append(link)

        for loc in locationContainer:
            location = (loc.span.text).strip()
            locations.append(location)


    print("There are %s jobs to scrape. Starting scrape..." % str(len(links)))

    # Visits each job page and scrapes further info
    descriptions = []
    for i in range(len(links)):
        page_link = links[i]
        page_response = requests.get(page_link,timeout=timeout)
        page_content = BeautifulSoup(page_response.content, "html.parser")
        descContainer = page_content.findAll("span", attrs={"class": "jobdescription"})

        for items in descContainer:
            desc = items.text

        descriptions.append(desc)
        title = str(titles[i])
        print("Job %s scraped - %s" % (str(i + 1), str(title)))

    createjoblist(titles,locations,descriptions,company)
    return True







