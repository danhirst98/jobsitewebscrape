'''
Date Created: August 24, 2019 9:51 pm
Author: JJ Fiedler
'''

from bs4 import BeautifulSoup
import requests
import json
import spacejobscrape.helperscripts.JobClasses as JC
from spacejobscrape.helperscripts.writeXML import createjoblist

# Sets the company for the script. Change each company
company = JC.Company(18, "Boeing", "https://www.boeing.com/", "None")

page_link = 'https://jobs.boeing.com/search-jobs/results?ActiveFacetID=6252001&CurrentPage=1&RecordsPerPage=15&Distance=50&RadiusUnitType=0&Keywords=&Location=&Latitude=&Longitude=&ShowRadius=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=6252001&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=914&FacetFilters%5B0%5D.Display=United+States&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=1&SearchType=5&CategoryFacetTerm=&CategoryFacetType=&LocationFacetTerm=&LocationFacetType=&KeywordType=&LocationType=&LocationPath=&OrganizationIds=&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf='
page_response = requests.get(page_link)
json_content = json.loads(page_response.content)
page_content = BeautifulSoup(json_content["results"], "html.parser")

#Getting total jobs from initial page link
totalJobs = page_content.find("h2").text
totalJobs = totalJobs[0:5].strip()

#Editing page link to reflect total number of jobs and grabbing new HTML from JSON
page_link = 'https://jobs.boeing.com/search-jobs/results?ActiveFacetID=6252001&CurrentPage=1&RecordsPerPage=' + totalJobs + '&Distance=50&RadiusUnitType=0&Keywords=&Location=&Latitude=&Longitude=&ShowRadius=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=6252001&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=914&FacetFilters%5B0%5D.Display=United+States&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=1&SearchType=5&CategoryFacetTerm=&CategoryFacetType=&LocationFacetTerm=&LocationFacetType=&KeywordType=&LocationType=&LocationPath=&OrganizationIds=&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf='
page_response = requests.get(page_link)
json_content = json.loads(page_response.content)
page_content = BeautifulSoup(json_content["results"], "html.parser")
jobList = page_content.find("ul", attrs={"class", "sr-main-jobs js-watch js-watch-once"})
jobContainer = jobList.findAll("li")

#Creates list of titles, locations and links to the application website
titles = []
locations = []
links = []

for job in jobContainer:
    title = job.find("h3").text
    location = job.find("span", {"class", "job-location job-info"}).text
    link = 'https://jobs.boeing.com' + job.find("a")["href"]

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
    desc = page_content.find("div", attrs={"class", "job-description-wrap js-jd-content"}).text

    title = str(titles[i])

    descriptions.append(desc)
    print("Job %s scraped - %s" % (str(i + 1), str(title)))