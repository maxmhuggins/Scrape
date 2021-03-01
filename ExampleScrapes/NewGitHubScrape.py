#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 20:18:19 2020

@author: max
"""

from selenium import webdriver
import TFSScrape as TFS

Username = 'maxmhuggins'
Password = 'Huggies192*!'
URL = 'https://github.com/maxmhuggins/Scrape/blob/master/Latex/Sections/'

S = TFS.Scraper(Username, Password, URL)    
URL = S.ModifiedURL
print(URL)
driver = webdriver.Chrome()
driver.get(URL)


p_element = driver.find_element_by_xpath('/html/body/div[4]/div/main/div[3]/div/div[3]/div[2]/table')
print(p_element.text)

driver.close()