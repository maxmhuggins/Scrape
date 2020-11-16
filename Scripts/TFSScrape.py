#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 19:06:22 2020

@author: ***REMOVED***
This is an attempt to scrape info from tfs to automate the task report.
"""

from selenium import webdriver


class Scraper:
    
    def __init__(self, Username, Password, URL):
        self.Username = Username
        self.Password = Password
        self.URL = URL
        self.ModifiedURL = self.MakeURL(self.URL)
    
    def MakeURL(self, URL):
        
        NoHTTPURL = ''
        for i in range(0, len(URL)):
            if i > 6:
                NoHTTPURL += URL[i]
            else:
                pass
            
        ModifiedURL = 'http://' + '{}:{}@'.format(self.Username, self.Password) + NoHTTPURL
        return ModifiedURL


# Username = '***REMOVED***'
# Password = 'uCfE2ahPM8C89CZ'
# URL = 'http://conw-mstf-01-pv.snaponglobal.com:8080/tfs/Embedded%20Engineering%20Collection/Agile%20Sanctuary/_backlogs/TaskBoard/2020/Sprint%2015?_a=requirements'

# S = Scraper(Username, Password, URL)    
# URL = S.ModifiedURL
# print(URL)
# driver = webdriver.Chrome()
# driver.get(URL)


# p_element = driver.find_element_by_id(id_='vss_7')
# print(p_element.text)

# driver.close()