import os
import glob
import subprocess
from spacejobscrape.helperscripts.UploadXML.uploadXML import uploadXML
from spacejobscrape.helperscripts.errorLogger import ErrorLogger
import importlib

def run(verbose,upload,alljobs,timeout,email,companies):
    """
    Clears recentXML directory then runs each company script in companyscripts, to create an XML for all jobs available at that company

    :param upload: Variable to discern whether the script will try to upload the resultant XML to the WPJobBoard database
    :return: void
    """

    # Deletes contents of recentXML, ready to create new one
    recentxmlfiles = glob.glob('./spacejobscrape/recentXML/*.xml')
    for f in recentxmlfiles:
        os.remove(f)

    #Creates error logger object. Will report any issues to the given email
    errorlogger = ErrorLogger(email)

    #if company parameter was given, only iterate through the given companies
    if companies:
        companyfiles = companies
    else:
        #Calls each file in companyscripts directory
        companyfiles = glob.glob('./spacejobscrape/companyscripts/*.py')


    for f in companyfiles:
        name = os.path.splitext(os.path.basename(f))[0]
        if name=='__init__':
            continue
        print("\n%s\n" % name)
        name = "spacejobscrape.companyscripts." + name
        mod = importlib.import_module(name)
        mod.runScrape(verbose, upload, alljobs,timeout)

    errorlogger.sendSummaryEmail()
    return True
