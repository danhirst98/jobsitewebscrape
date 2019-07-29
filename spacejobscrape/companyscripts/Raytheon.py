'''
Date Created: July 28, 2019
Author: JJ Fiedler
'''

import json
import requests
from bs4 import BeautifulSoup
import spacejobscrape.helperscripts.JobClasses as JC
from spacejobscrape.helperscripts.writeXML import createjoblist

def runScrape(verbose,upload,alljobs,timeout):
    # Sets the company for the script. Change each company
    company = JC.Company(15, "Raytheon", "https://www.raytheon.com/", "None")

    # Getting total number of jobs from base link
    page_link = 'https://jobs.raytheon.com/search-jobs/United%20States?orgIds=4679&alp=6252001&alt=2'
    page_response = requests.get(page_link)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    totalJobs = page_content.find("h1", {"role":"status"}).text
    totalJobs = totalJobs[:4]

    #Editing link to get total number of jobs
    page_link = 'https://jobs.raytheon.com/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=' + totalJobs + '&Distance=50&RadiusUnitType=0&Keywords=&Location=United+States&Latitude=&Longitude=&ShowRadius=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=6252001&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=3478&FacetFilters%5B0%5D.Display=United+States&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=1&SearchType=6&CategoryFacetTerm=&CategoryFacetType=&LocationFacetTerm=&LocationFacetType=&KeywordType=&LocationType=&LocationPath=&OrganizationIds=4679&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf='
    page_response = requests.get(page_link)
    page_json = json.loads(page_response.content)
    page_content = BeautifulSoup(page_json["results"], "html.parser")
    jobsContainer = page_content.findAll("li")

    #Removing country list item
    jobsContainer = jobsContainer[1:]

    #Creates list of titles, locations and links to the application website
    titles = []
    locations = []
    links = []

    for job in jobsContainer:
        title = job.find("h2").text
        location = job.find("span", attrs={"class":"job-location"}).text
        link = 'https://jobs.raytheon.com' + job.a["href"]

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
        desc = page_content.find("div", attrs={"class":"ats-description"}).text

        title = str(titles[i])

        descriptions.append(desc)
        print("Job %s scraped - %s" % (str(i + 1), str(title)))

    createjoblist(titles,locations,descriptions,company)
    return True