#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 14:15:17 2019

@author: DanHirst
"""
import importlib
import os
from companyscripts.helperscripts.UploadXML import uploadXML


#Deletes contents of recentXML, ready to create new one
folder = str(os.path.dirname(os.path.abspath(__file__)))+"/recentXML/"
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)


companydir = str(os.path.dirname(os.path.abspath(__file__)))+"/companyscripts/"
#Iterates through each file in companyscripts and runs the file.
for filename in os.listdir(companydir):
    if filename.endswith(".py"): 
        print("\n\n"+str(os.path.splitext(filename)[0])+"\n")
        module = importlib.import_module("companyscripts.%s" % os.path.splitext(filename)[0])
        
#XML_Upload.uploadXML()

