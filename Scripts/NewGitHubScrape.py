#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 20:18:19 2020

@author: max
"""

from selenium import webdriver
import TFSScrape as TFS

Username = '***REMOVED***'
Password = '***REMOVED***'
URL = 'https://github.com/***REMOVED***/Scrape'

S = TFS.Scraper(Username, Password, URL)    
URL = S.ModifiedURL
print(URL)
driver = webdriver.Chrome()
driver.get(URL)


p_element = driver.find_element_by_class_name('Box-row Box-row--focus-gray py-2 d-flex position-relative js-navigation-item')
print(p_element.text)

driver.close()