'''
Created on Tuesday May 21 6:39 PM
Author: JJ Fiedler
'''

from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import companyscripts.helperscripts.JobClasses as JC
from companyscripts.helperscripts.writeXML import writeXML
from companyscripts.helperscripts.findLocation import findLocations

#Sets the company for the script. Change each company
company = JC.Company(3, "XPrize", "https://www.xprize.org/home", "test@blueorigin.com")

#Uses webdriver and chromedriver to get html from javascript
chromedriver = "/Users/DanHirst 1/Downloads/chromedriver"
driver = webdriver.Chrome(chromedriver)
driver.get("https://www.xprize.org/about/careers")
html = driver.execute_script("return document.documentElement.outerHTML")
page_content = BeautifulSoup(html, "html.parser")
jobsLink = page_content.find("iframe", {"id":"grnhse_iframe"})["src"]

#Sets the main link to embedded javascript link
main_link = str(jobsLink)
page_response = requests.get(main_link, timeout=5)
page_content = BeautifulSoup(page_response.content, "html.parser")
jobContainer = page_content.findAll("div", attrs={"class":"opening"})

#Creates list of titles, locations and links to the application website
titles = []
locations = []
links = []

for job in jobContainer:
    link = job.a["href"]
    title = job.a.text
    location = job.find("span",attrs={"class":"location"}).text

    #Converts Headquarters location to city name
    if location == "Headquarters":
        location = "Culver City"

    location = location + ", USA"
    titles.append(title)
    locations.append(location)
    links.append(link)

print("There are %s jobs to scrape. Starting scrape..." % str(len(links)))

#Converts each location from string into Location object using an API
locations = findLocations(locations)

#Visits each job page and scrapes further info
jobs = []
for i in range(len(links)):

    page_link = links[i]

    #Gets html link from javascript
    driver.get(str(page_link))
    desc_html = driver.execute_script("return document.documentElement.outerHTML")
    #Gets html from javascript
    desc_content = BeautifulSoup(desc_html, "html.parser")
    desc_link = desc_content.find("iframe", {"id":"grnhse_iframe"})["src"]
    #Gets html from the new link
    page_response = requests.get(desc_link, timeout=10)
    page_content = BeautifulSoup(page_response.content, "html.parser")

    title = str(titles[i])

    location = locations[i]

    #TODO: Add formatting for content. Currently it's just a big mass of text
    descContent = page_content.find("div", attrs={"id":"content"})
    descContainer = descContent.findAll("p")
    desc = descContainer[3].text + " " + descContainer[4].text

    #TODO: Identify tags and metas

    #Creates new job object with all information
    newJob = JC.Job(title,desc,company,location,[],[],3)
    jobs.append(newJob)
    print("Job %s scraped - %s" % (str(i+1),str(title)))

print("Jobs scraped. Writing XML...")
writeXML(jobs)
