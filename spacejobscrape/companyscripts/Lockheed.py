'''
Date Created: July 21, 2019
Author: JJ Fiedler
'''

from bs4 import BeautifulSoup
import requests
import json
import spacejobscrape.helperscripts.JobClasses as JC
from spacejobscrape.helperscripts.writeXML import createjoblist

def runScrape(verbose,upload,alljobs,timeout):
    #Sets the company for the script. Change each company
    company = JC.Company(12, "Lockheed Martin", "https://www.lockheedmartin.com/en-us/index.html", "lmcareers.helpdesk@lmco.com")

    #Getting page to find total number of jobs
    page_link = 'https://www.lockheedmartinjobs.com/search-jobs/results?ActiveFacetID=Space&CurrentPage=1&RecordsPerPage=1000&Distance=50&RadiusUnitType=0&Keywords=&Location=&Latitude=&Longitude=&ShowRadius=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=4566966&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=13&FacetFilters%5B0%5D.Display=Puerto+Rico&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&FacetFilters%5B1%5D.ID=6252001&FacetFilters%5B1%5D.FacetType=2&FacetFilters%5B1%5D.Count=4897&FacetFilters%5B1%5D.Display=United+States&FacetFilters%5B1%5D.IsApplied=true&FacetFilters%5B1%5D.FieldName=&FacetFilters%5B2%5D.ID=Space&FacetFilters%5B2%5D.FacetType=5&FacetFilters%5B2%5D.Count=1082&FacetFilters%5B2%5D.Display=Space&FacetFilters%5B2%5D.IsApplied=true&FacetFilters%5B2%5D.FieldName=job_level&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&CategoryFacetTerm=&CategoryFacetType=&LocationFacetTerm=&LocationFacetType=&KeywordType=&LocationType=&LocationPath=&OrganizationIds=&PostalCode=&fc=&fl=6252001%2C4566966&fcf=&afc=&afl=&afcf='
    page_response = requests.get(page_link, timeout=timeout)
    page_json = json.loads(page_response.content)
    page_content = BeautifulSoup(page_json["results"], "html.parser")

    #Getting total nunmber of jobs
    totalJobsStr = page_content.find("p").text
    totalJobs = ''
    for i in totalJobsStr:
        if i.isdigit():
            totalJobs = totalJobs + str(i)

    #Removing number of jobs per page from string
    totalJobs = totalJobs[2:]

    #Editing page_link and getting new page to reflect thes total number of jobs
    page_link = 'https://www.lockheedmartinjobs.com/search-jobs/results?ActiveFacetID=Space&CurrentPage=1&RecordsPerPage=' + totalJobs + '&Distance=50&RadiusUnitType=0&Keywords=&Location=&Latitude=&Longitude=&ShowRadius=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=4566966&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=13&FacetFilters%5B0%5D.Display=Puerto+Rico&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&FacetFilters%5B1%5D.ID=6252001&FacetFilters%5B1%5D.FacetType=2&FacetFilters%5B1%5D.Count=4897&FacetFilters%5B1%5D.Display=United+States&FacetFilters%5B1%5D.IsApplied=true&FacetFilters%5B1%5D.FieldName=&FacetFilters%5B2%5D.ID=Space&FacetFilters%5B2%5D.FacetType=5&FacetFilters%5B2%5D.Count=1082&FacetFilters%5B2%5D.Display=Space&FacetFilters%5B2%5D.IsApplied=true&FacetFilters%5B2%5D.FieldName=job_level&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&CategoryFacetTerm=&CategoryFacetType=&LocationFacetTerm=&LocationFacetType=&KeywordType=&LocationType=&LocationPath=&OrganizationIds=&PostalCode=&fc=&fl=6252001%2C4566966&fcf=&afc=&afl=&afcf='
    page_response = requests.get(page_link, timeout=timeout)
    page_json = json.loads(page_response.content)
    page_content = BeautifulSoup(page_json["results"], "html.parser")
    titleContainer = page_content.findAll('span', attrs={'class':'job-title'})
    locationContainer = page_content.findAll('span', attrs={'class':'job-location'})
    linkContainer = page_content.findAll('a')

    #Removing unnessary "a" tags
    linkContainer = linkContainer[2:]

    #Creates list of titles, locations and links to the application website
    titles = []
    locations = []
    links = []

    for i in range(len(titleContainer)):
        title = titleContainer[i].text
        location = locationContainer[i].text
        link = 'https://www.lockheedmartinjobs.com' + linkContainer[i]["href"]

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

        desc = page_content.find('div', attrs={'class':'ats-description'}).text
        descriptions.append(desc)
        print("Job %s scraped - %s" % (str(i + 1), str(title)))

    createjoblist(titles,locations,descriptions,company)
    return True
