'''
Date Edited: July 13, 2019 11:24 AM
Author: JJ Fiedler
'''

from bs4 import BeautifulSoup
import requests
import spacejobscrape.helperscripts.JobClasses as JC
from spacejobscrape.helperscripts.writeXML import createjoblist

def runScrape(verbose,upload,alljobs,timeout):
    #Sets the company for the script. Change each company
    company = JC.Company(9,"Bigelow","https://bigelowaerospace.com/","info@bigelowspaceops.com")

    page_link = "https://bigelowaerospace.com/pages/job-opportunities/"
    page_response = requests.get(page_link, timeout=timeout)
    page_content = BeautifulSoup(page_response.content, "html.parser")

    alljobswebpage = page_content.findAll("p")

    #Creates list of titles, locations and links to the application website
    titles = []
    locations = []
    links = []
    for job in alljobswebpage:
        try:
            title = job.a.u.text
            link = job.a["href"]
            location = "North Las Vegas, NV, USA"
            titles.append(title)
            locations.append(location)
            links.append(link)
        except AttributeError:
            break

    print("There are %s jobs to scrape. Starting scrape..." % str(len(links)))

    #Visits each job page and scrapes further info
    descriptions = []
    for i in range(len(links)):
        page_link = links[i]
        page_response = requests.get(page_link, timeout=timeout)
        page_content = BeautifulSoup(page_response.content, "html.parser")

        title = str(titles[i])

        descContainer = page_content.findAll("ul")
        desc = descContainer[1].text
        descriptions.append(desc)

        print("Job %s scraped - %s" % (str(i+1),str(title)))

    createjoblist(titles, locations, descriptions, company)
    return True

