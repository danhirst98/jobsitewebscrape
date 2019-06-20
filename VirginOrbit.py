#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 00:22:08 2019

@author: DanHirst
"""
import sys
from PyQt5.QtGui import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebKit import QWebPage
import bs4 as bs


class Client(QWebPage):
    
    def __init__(self,url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self.on_page_load)
        self.mainFrame().load(QUrl(url))
        
    def on_page_load(self):
        self.app.quit()
        
url = 'https://careers-virginorbit.icims.com/jobs/'
client_response = Client(url)
source = client_response.mainFrame().toHtml
soup = bs.BeautifulSoup(source,'lxml')
