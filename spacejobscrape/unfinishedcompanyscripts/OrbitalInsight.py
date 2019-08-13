'''
Date Created: July 16, 2019 9:15 AM
Author: JJ Fiedler
'''

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import spacejobscrape.helperscripts.JobClasses as JC
from spacejobscrape.helperscripts.writeXML import createjoblist

def runScrape(verbose,upload,alljobs,timeout):
    # Sets the company for the script. Change each company
    company = JC.Company(16, "OrbitalInsight", "https://orbitalinsight.com/", "sales@orbitalinsight.com")

    # Uses webdriver and chromedriver to get html from javascript
    chromedriver = "/Users/JJ/Documents/ProgrammingStuff/chromedriver"
    driver = webdriver.Chrome(chromedriver)
    driver.get("https://orbitalinsight.com/company/careers/#positions")
    html = driver.execute_script("return document.documentElement.outerHTML")
    page_content = BeautifulSoup(html, "html.parser")
    driver.close()

    #No overarching div that contains all jobs. Getting each item individually in a list
    titleContainer = page_content.find_all("h3", attrs={"class":"career__title"})
    locationContainer = page_content.findAll("div", attrs={"class":"career__meta--location"})
    linkContainer = page_content.findAll("a", attrs={"class":"btn"})

    # Removing Join Us link and Email link
    numJobs = len(titleContainer)
    linkContainer = linkContainer[1:numJobs+1]

    #Creates list of titles, locations and links to the application website
    titles = []
    locations = []
    links = []

    for i in range(len(titleContainer)):
        title = titleContainer[i].text
        location = locationContainer[i].text
        link = linkContainer[i]["href"]

        titles.append(title)
        locations.append(location)
        links.append(link)

    print("There are %s jobs to scrape. Starting scrape..." % str(len(links)))

    # Visits each job page and scrapes further info
    descriptions = []
    for i in range(len(links)):
        page_link = links[i]
        driver = webdriver.Chrome(chromedriver)
        driver.get(page_link)
        html = driver.execute_script("return document.documentElement.outerHTML")
        page_content = BeautifulSoup(html, "html.parser")
        driver.close()

        desc = page_content.find("div", attrs={"class":"columns small-12 medium-8"}).text

        title = str(titles[i])

        descriptions.append(desc)
        print("Job %s scraped - %s" % (str(i + 1), str(title)))

    createjoblist(titles,locations,descriptions,company)
    return True