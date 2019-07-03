'''
Created July 2, 2019 7:12 pm
Author: JJ Fiedler
'''

from bs4 import BeautifulSoup
import requests
from spacejobscrape.helperscripts.JobClasses import Company
from spacejobscrape.helperscripts.writeXML import createjoblist

def runScrape(verbose,upload,alljobs,timeout):
    company = Company(4,"SpaceX","www.generationorbit.com","info@GOLauncher.com")

    company_careers_url = "https://spaceworksgo.bamboohr.com/jobs/embed2.php"

    page_response = requests.get(company_careers_url, timeout=timeout)
    page_content = BeautifulSoup(page_response.content, "html.parser")

    jobsContainer = page_content.findAll("li", attrs={"class":"BambooHR-ATS-Jobs-Item"})

    # Creates list of titles, locations and links to the application website
    titles = []
    links = []
    locations = []

    for jobs in jobsContainer:
        title = jobs.a.text
        location = jobs.find("span", attrs={"class":"BambooHR-ATS-Location"}).text + ", USA"
        link = jobs.a["href"]

        if link.startswith("//"):
            link = link.replace("//", "http://")

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

        descContainer = page_content.findAll("p")

        title = str(titles[i])
        j = 0

        #Searches through each p tag and gets the description
        for par in descContainer:
            if par.text == "POSITION SUMMARY":
                desc = descContainer[j+1].text
                descriptions.append(desc)
            j = j + 1

        print("Job %s scraped - %s" % (str(i + 1), str(title)))

        createjoblist(titles, locations, descriptions, company)
        return True