#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 08:28:25 2019

@author: DanHirst
"""
from spacejobscrape.helperscripts.JobClasses import Job,Tag,Meta,Company,Location
from spacejobscrape.helperscripts.writeXML import writeXML

import unittest

class TestScrapes(unittest.TestCase):
    def test_astranis(self):
        from spacejobscrape.companyscripts.Astranis import runScrape
        self.assertEqual(runScrape(),True,"There was an error preventing the code from returning true")

    def test_spacex(self):
        from spacejobscrape.companyscripts.SpaceX import runScrape
        self.assertEqual(runScrape(),True,"There was an error preventing the code from returning true")

    def test_xprize(self):
        from spacejobscrape.companyscripts.XPrize import runScrape
        self.assertEqual(runScrape(),True,"There was an error preventing the code from returning true")



if __name__=='__main__':
    unittest.main()