'''
Date Created: July 24, 2019
Author: JJ Fiedler
'''

import json
import requests
from bs4 import BeautifulSoup
import spacejobscrape.helperscripts.JobClasses as JC
from spacejobscrape.helperscripts.writeXML import createjoblist

def runScrape(verbose,upload,alljobs,timeout):
    #Sets the company for the script. Change each company
    company = JC.Company(14,"Collins Aerospace","https://www.rockwellcollins.com/","None")

    #Getting total number of jobs from base link
    page_link = 'https://jobs.collinsaerospace.com/search-jobs/'
    page_response = requests.get(page_link, timeout=timeout)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    resultsString = page_content.find("h1", attrs={"role":"status"}).text
    totalJobs = ""

    #Getting total number of jobs
    for i in range(len(resultsString)):
        if resultsString[i].isdigit():
            totalJobs += resultsString[i]

    #Getting json data from new link
    jsonLink = 'https://jobs.collinsaerospace.com/search-jobs/results?ActiveFacetID=6252001&CurrentPage=1&RecordsPerPage=' + totalJobs + '&Distance=50&RadiusUnitType=0&Keywords=&Location=&Latitude=&Longitude=&ShowRadius=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=6252001&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=2254&FacetFilters%5B0%5D.Display=United+States&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&CategoryFacetTerm=&CategoryFacetType=&LocationFacetTerm=&LocationFacetType=&KeywordType=&LocationType=&LocationPath=&OrganizationIds=&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf='
    page_response = requests.get(jsonLink, timeout=timeout)
    page_json = json.loads(page_response.content)
    page_content = BeautifulSoup(page_json["results"], "html.parser")
    jobContainer = page_content.findAll("li")

    #Removing page filter item
    jobContainer = jobContainer[1:]

    #Creates list of titles, locations and links to the application website
    titles = []
    locations = []
    links = []

    for job in jobContainer:
        title = job.find("h2").text
        location = job.find("span", attrs={"class":"job-location"}).text
        link = 'https://jobs.collinsaerospace.com' + job.a["href"]

        titles.append(title)
        locations.append(location)
        links.append(link)

    # Visits each job page and scrapes further info
    descriptions = []
    for i in range(len(links)):
        page_link = links[i]
        page_response = requests.get(page_link,timeout=timeout)
        page_content = BeautifulSoup(page_response.content, "html.parser")

        title = str(titles[i])

        desc = page_content.find('div', attrs={"class":"ats-description"}).text
        descriptions.append(desc)
        print("Job %s scraped - %s" % (str(i + 1), str(title)))

    createjoblist(titles, locations, descriptions, company)
    return True


