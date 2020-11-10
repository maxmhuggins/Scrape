#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 19:06:22 2020

@author: ***REMOVED***
This is an attempt to scrape info from tfs to automate the task report.
"""

from selenium import webdriver

my_url = 'http://***REMOVED***:uCfE2ahPM8C89CZ@conw-mstf-01-pv.snaponglobal.com:8080/tfs/Embedded%20Engineering%20Collection/Agile%20Sanctuary/_backlogs/Taskboard?_a=requirements'


driver = webdriver.Chrome()

driver.get(my_url)


p_element = driver.find_element_by_id(id_='vss_7')
print(p_element.text)

driver.close()