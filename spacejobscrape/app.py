import os
import glob
import subprocess
from spacejobscrape.helperscripts.UploadXML.uploadXML import uploadXML
from spacejobscrape.helperscripts.errorLogger import ErrorLogger

def run(upload):
    """
    Clears recentXML directory then runs each company script in companyscripts, to create an XML for all jobs available at that company

    :param upload: Variable to discern whether the script will try to upload the resultant XML to the WPJobBoard database
    :return: void
    """

    # Deletes contents of recentXML, ready to create new one
    recentxmlfiles = glob.glob('./spacejobscrape/recentXML/*.xml')
    for f in recentxmlfiles:
        os.remove(f)

    errorlogger = ErrorLogger("dan.hirst@seds.org")

    #Calls each file in companyscripts directory
    companyfiles = glob.glob('./spacejobscrape/companyscripts/*.py')
    for f in companyfiles:
        cmd = ['python', str(f)]
        try:
            subprocess.run(cmd)
        except Exception as e:
            errorlogger.addError(e,f)

    if upload:
        uploadXML()

    errorlogger.sendSummaryEmail()
    return True
