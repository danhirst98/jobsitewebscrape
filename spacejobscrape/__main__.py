#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 14:15:17 2019

@author: DanHirst
"""
from spacejobscrape import app
import sys,getopt

def main(args):
    unixOptions = "hvuat:c:e:"
    gnuOptions = ["help","verbose","upload","alljobs","timeout=","companies=","email="]
    try:
        arguments, values = getopt.getopt(args, unixOptions, gnuOptions)
    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))
        sys.exit(2)

    verbose = False
    upload = False
    alljobs = False
    timeout = 10
    email = ""
    companies = []
    # evaluate given options
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-v", "--verbose"):
            print("enabling verbose mode")
            verbose=True
        elif currentArgument in ("-h", "--help"):
            print("displaying help")
            exit(1)
        elif currentArgument in ("-u","--upload"):
            print("Will upload jobs to site")
            upload = True
        elif currentArgument in ("-a","--alljobs"):
            print("Will create XML of all jobs, regardless of whether they have been uploaded before")
            alljobs = True
        elif currentArgument in ("-t","--timeout"):
            print("Set website timeout as %s seconds" % currentValue)
            timeout = currentValue
            alljobs = True
        elif currentArgument in ("-c","--companies"):
            companies = currentValue.split()
            print("Will only scrape the following companies:")
            for c in companies:
                print(c)
        elif currentArgument in ("-e","--email"):
            print("Will send summary email to %s" % currentValue)
            email = currentValue

    #Email is a mandatory argument. If there isn't, then the code finishes
    if not email:
        print("-e/--email was not given")
        exit(2)

    app.run(verbose,upload,alljobs,timeout,email,companies)

if __name__ == '__main__':
    main(sys.argv[1:])
