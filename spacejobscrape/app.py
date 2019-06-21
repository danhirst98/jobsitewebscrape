import os
import glob
import subprocess

def run():


    # Deletes contents of recentXML, ready to create new one
    recentxmlfiles = glob.glob('./spacejobscrape/recentXML/*.xml')
    for f in recentxmlfiles:
        os.remove(f)

    companyfiles = glob.glob('./spacejobscrape/companyscripts/*.py')
    for f in companyfiles:
        print(f)
        cmd = ['python', str(f)]
        subprocess.call(cmd)


    #TODO: Run XML upload
