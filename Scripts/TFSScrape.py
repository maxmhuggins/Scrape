#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 19:06:22 2020

@author: ***REMOVED***
This is an attempt to scrape info from tfs to automate the task report.
"""

from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

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
            
        

wait = 1
Username = '***REMOVED***'
Password = 'uCfE2ahPM8C89CZ'
URL = 'http://conw-mstf-01-pv.snaponglobal.com:8080/tfs/Embedded Engineering Collection/Agile Sanctuary/_backlogs'
S = Scraper(Username, Password, URL)    
URL = S.ModifiedURL

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

# driver = webdriver.Chrome()
driver.get(URL)
time.sleep(wait*2)
QueriesButton = driver.find_element_by_xpath('//*[@id="mi_237_ms.vss-work-web.work-hub"]/span[1]')
QueriesButton.click()
time.sleep(wait)

WorkInTest = driver.find_element_by_xpath('//*[@id="tfs_tnli17"]')
WorkInTest.click()
time.sleep(wait)

ColumnOptionsButton = driver.find_element_by_xpath('//*[@id="mi_71_column-options"]')
ColumnOptionsButton.click()
time.sleep(wait)

CreatedDate = driver.find_element_by_xpath('//*[@id="display-available-list"]/option[39]')
CreatedDate.click()
time.sleep(wait)

ArrowButton = driver.find_element_by_xpath('//*[@class="add ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only"]')
ArrowButton.click()
time.sleep(wait)

OK = driver.find_element_by_xpath('//*[@id="ok"]')
OK.click()
time.sleep(wait)

# GATHER INFO FOR TEST TASKS NOW
#============================================================================#
WorkInToDo = driver.find_element_by_xpath('//*[@id="tfs_tnli18"]')
WorkInToDo.click()


ColumnOptionsButton = driver.find_element_by_xpath('//*[@id="mi_71_column-options"]')
ColumnOptionsButton.click()
time.sleep(wait)

CreatedDate = driver.find_element_by_xpath('//*[@id="display-available-list"]/option[39]')
CreatedDate.click()
time.sleep(wait)

ArrowButton = driver.find_element_by_xpath('//*[@class="add ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only"]')
ArrowButton.click()
time.sleep(wait)

OK = driver.find_element_by_xpath('//*[@id="ok"]')
OK.click()
time.sleep(wait)

# ScrollDown = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div/div/div[3]/div[4]/div[2]/div/div/div/div[1]/div[3]/div[2]')
# ScrollDown.send_keys(Keys.END)
# N = 100 #Need to find out how to handle last task in list
# elements = range(0,N)
# for element in elements:
#     new_page_element = driver.find_element_by_xpath('//*[@id="row_vss_11_{}"]'.format(element))
#     Task = driver.find_element_by_xpath('//*[@id="row_vss_11_{}"]/div[1]'.format(element))
#     print('THIS IS TASK #{}'.format(Task.text))
#     print(new_page_element.text)
#     time.sleep(wait/2)





time.sleep(3)


































# TotalTasks = range(12088, 12090)

# # for task in TotalTasks:

# #     p_element = driver.find_element_by_id('tile-{}'.format(task))
# #     print('THIS IS TASK #{}'.format(task))
# #     print(p_element.text)
# #     time.sleep(1)



# 
# 
# tasks = []
# for task in driver.find_elements_by_class_name('content-section'):
#     title = person.find_element_by_xpath('.//div[@class="title"]/a').text
#     company = person.find_element_by_xpath('.//div[@class="company"]/a').text

#     persons.append({'title': title, 'company': company})



driver.close()