'''
Date Created: July 15, 2019 4:10 PM
Author: JJ Fiedler
'''

from bs4 import BeautifulSoup
import requests
import spacejobscrape.helperscripts.JobClasses as JC
from spacejobscrape.helperscripts.writeXML import createjoblist


def runScrape(verbose,upload,alljobs,timeout):
    # Sets the company for the script. Change each company
    company = JC.Company(10, "OneWeb", "https://www.oneweb.world/", "contact@oneweb.net")

    page_link = 'https://boards.greenhouse.io/embed/job_board?for=oneweb&b=https%3A%2F%2Fwww.oneweb.world%2Fcareers'
    page_response = requests.get(page_link, timeout=timeout)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    jobContainer = page_content.findAll("div", attrs={"class":"opening"})

    # Creates list of titles, locations and links to the application website
    titles = []
    locations = []
    links = []

    for job in jobContainer:
        title = job.a.text.strip()
        location = job.span.text.strip()
        tempLink = job.a["href"]
        ID = tempLink[50:]
        link = "https://boards.greenhouse.io/embed/job_app?for=oneweb&token=" + ID + "&b=https%3A%2F%2Foneweb.world%2Fcareers-opportunities%2F"

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

        descContainer = page_content.findAll("p")

        for par in descContainer:
            desc = par.text
            descriptions.append(desc)

        title = str(titles[i])
        print("Job %s scraped - %s" % (str(i + 1), str(title)))

    createjoblist(titles, locations, descriptions, company)
    return True


