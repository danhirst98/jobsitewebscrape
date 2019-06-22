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
        if "Astranis" in f:
            cmd = ['python', str(f)]
            subprocess.call(cmd)
            exit(2)


    #TODO: Run XML upload
