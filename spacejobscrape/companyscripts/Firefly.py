'''
Author: JJ Fiedler
'''

import requests
import json
from bs4 import BeautifulSoup
from spacejobscrape.helperscripts import FireflyAuto
import spacejobscrape.helperscripts.JobClasses as JC
from spacejobscrape.helperscripts.writeXML import createjoblist

def runScrape(verbose,upload,alljobs,timeout):
    #Sets the company for the script. Change each company
    company = JC.Company(13,"Firefly","https://firefly.com/","N/A")

    #Running autogui for Firefly to get json links
    jsonLinks = FireflyAuto.run()

    jsonURL_1 = jsonLinks[0]
    jsonURL_2 = jsonLinks[1]

    #Requesting json data
    jsonResponse_1 = requests.get(jsonURL_1, timeout=timeout)
    data_1 = json.loads(jsonResponse_1.content)

    jsonRepsonse_2 = requests.get(jsonURL_2, timeout=timeout)
    data_2 = json.loads(jsonRepsonse_2.content)


    #Creates list of titles, locations and links to the application website
    titles = []
    locations = []
    linkIDs = []

    #Parsing json data to get titles, locations, and link ID numbers
    for items in data_1["jobRequisitions"]:
        titles.append(items["requisitionTitle"])
        try:
            locations.append(items["requisitionLocations"][0]["nameCode"]["shortName"])
            linkIDs.append(items["customFieldGroup"]["stringFields"][0]["stringValue"])
        except IndexError:
            locations.append("N/A")
            continue

    for items in data_2["jobRequisitions"]:
        titles.append(items["requisitionTitle"])
        try:
            locations.append(items["requisitionLocations"][0]["nameCode"]["shortName"])
            linkIDs.append(items["customFieldGroup"]["stringFields"][0]["stringValue"])
        except IndexError:
            locations.append("None")
            continue


    print("There are %s jobs to scrape. Starting scrape..." % str(len(titles)))

    #Visits each job page and scrapes further info
    descriptions = []
    for i in range(len(titles)):

        #Editing description link based on link ID numbers
        link = 'https://workforcenow.adp.com/mascsr/default/careercenter/public/events/staffing/v1/job-requisitions/' + linkIDs[i] + '?cid=241aedef-e1d0-4fca-8d2a-bb3ff0afed85&timeStamp=1563828327993&lang=en_US&ccId=19000101_000001&locale=en_US'

        #HTML is found in json data. Getting json response first then parsing the html
        jsonResponse = requests.get(link, timeout=timeout)
        data = json.loads(jsonResponse.content)
        jsonHTML = BeautifulSoup(data["requisitionDescription"], "html.parser")
        desc = jsonHTML.text

        title = str(titles[i])
        descriptions.append(desc)
        print("Job %s scraped - %s" % (str(i + 1), str(title)))

    createjoblist(titles, locations, descriptions, company)
    return True
