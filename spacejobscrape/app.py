import os
import glob
import subprocess
from spacejobscrape.helperscripts.UploadXML.uploadXML import uploadXML
def run(upload):


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

    if upload:
        uploadXML()
