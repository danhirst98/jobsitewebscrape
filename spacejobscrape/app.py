import os
import glob
import subprocess

def run():

    #TODO: Iterate through jobs in company scripts, running each one
    #TODO: Run XML upload

    # Deletes contents of recentXML, ready to create new one
    recentxmlfiles = glob.glob('./spacejobscrape/recentXML/*.xml')
    for f in recentxmlfiles:
        os.remove(f)

    companyfiles = glob.glob('./spacejobscrape/companyscripts/*.py')
    for f in companyfiles:
        print(f)
        cmd = ['python', str(f)]
        subprocess.call(cmd)