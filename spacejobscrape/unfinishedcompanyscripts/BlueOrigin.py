'''
Created on Tuesday May 23 12:47 PM
Author: JJ Fiedler
'''

from bs4 import BeautifulSoup
import json
import os
import subprocess
import shlex
import spacejobscrape.helperscripts.JobClasses as JC
from spacejobscrape.helperscripts.writeXML import createjoblist

company = JC.Company(4, "Blue Origin", "https://www.blueorigin.com/", "jobs@blueorigin.com")

#Running external workday scrape script
args = shlex.split("python3 WorkdayScrape.py -u 'https://blueorigin.wd5.myworkdayjobs.com/BlueOrigin' -d './BlueOriginJSON'")
print("Running external workday scrape script...")
subprocess.run(args)


#Basepath for the folder containing json files
basepath = "/Users/JJ/Documents/ProgrammingStuff/PythonFiles/JobSiteWebscrape/BlueOriginJSON/"

#Creates list of titles, locations and links to the application website
titles = []
locations = []
links = []

#Gets file names
with os.scandir(basepath) as entries:
    for entry in entries:
        if entry.is_file():
            #Opens all json files and gets the appropriate data
            with open(basepath + entry.name) as json_file:
                data = json.load(json_file)
                #Getting title, description and link from JSON files
                title = data['labels'][0]
                location = data['labels'][1]
                desc = data['description']
                link = data['link']
                #Removing extra string that's on location
                if location.find(", More...") == -1:
                    location = location + ", USA"
                else:
                    location = location[:-9] + ", USA"

                titles.append(title)
                locations.append(location)
                links.append(link)

print("There are %s jobs to scrape. Starting scrape..." % str(len(links)))

descriptions = []

for i in range(len(links)):
    title = str(titles[i])

    location = locations[i]

    descriptions.append(desc)
    print("Job %s scraped - %s" % (str(i+1),str(title)))

createjoblist(titles,locations,descriptions,company)

