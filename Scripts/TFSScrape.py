#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 19:06:22 2020

@author: ***REMOVED***
This is an attempt to scrape info from tfs to automate the task report.
"""

from selenium import webdriver
import time


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


Username = '***REMOVED***'
Password = 'uCfE2ahPM8C89CZ'
URL = 'http://conw-mstf-01-pv.snaponglobal.com:8080/tfs/Embedded%20Engineering%20Collection/Agile%20Sanctuary/_backlogs/taskboard/Agile%20Sanctuary%5C2020%5CSprint%2016?_a=requirements'
S = Scraper(Username, Password, URL)    
URL = S.ModifiedURL
# print(URL)
driver = webdriver.Chrome()
driver.get(URL)

# TotalTasks = range(12088, 12090)

# # for task in TotalTasks:

# #     p_element = driver.find_element_by_id('tile-{}'.format(task))
# #     print('THIS IS TASK #{}'.format(task))
# #     print(p_element.text)
# #     time.sleep(1)

p_element = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/div/div[3]/div[1]/h1[1]')


print(p_element.text)
# 
# 
# tasks = []
# for task in driver.find_elements_by_class_name('content-section'):
#     title = person.find_element_by_xpath('.//div[@class="title"]/a').text
#     company = person.find_element_by_xpath('.//div[@class="company"]/a').text

#     persons.append({'title': title, 'company': company})



driver.close()