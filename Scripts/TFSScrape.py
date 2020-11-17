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

wait = .5
Username = '***REMOVED***'
Password = 'uCfE2ahPM8C89CZ'
URL = 'http://conw-mstf-01-pv.snaponglobal.com:8080/tfs/Embedded Engineering Collection/Agile Sanctuary/_backlogs'
S = Scraper(Username, Password, URL)    
URL = S.ModifiedURL

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(chrome_options=options)

# driver = webdriver.Chrome()
driver.get(URL)
time.sleep(wait*2)
QueriesButton = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/table[2]/tbody/tr/td/div[1]/div/table/tbody/tr/td[1]/div[2]/div/ul/li[2]/a/span[1]')
QueriesButton.click()
time.sleep(wait)

ColumnOptionsButton = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div/div/div[3]/div[4]/div[2]/div/div/div/div[1]/div[1]/ul/li[14]/span[1]')
ColumnOptionsButton.click()
time.sleep(wait)

CreatedDate = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[4]/div[1]/div[1]/div[2]/select/option[39]')
CreatedDate.click()
time.sleep(wait)

ArrowButton = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[4]/div[1]/div[1]/div[3]/div[1]/button/span/span')
ArrowButton.click()
time.sleep(wait)

OK = driver.find_element_by_xpath('/html/body/div[4]/div[3]/div/button[1]/span')
OK.click()
time.sleep(wait)

CreatedDateButton = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div/div/div[3]/div[4]/div[2]/div/div/div/div[1]/div[3]/div[1]/div[1]/div[8]')
CreatedDateButton.click()
time.sleep(wait)
CreatedDateButton.click()
time.sleep(wait)
CreatedDateButton.click()
time.sleep(wait)
CreatedDateButton.click()
time.sleep(wait)

# ClickHereToScroll = driver.find_element_by_xpath('//*[@id="row_vss_11_1"]')
# ClickHereToScroll.send_keys(Keys.PAGE_DOWN);

N = 100 #Need to find out how to handle last task in list
elements = range(0,N)
for element in elements:
    new_page_element = driver.find_element_by_xpath('//*[@id="row_vss_11_{}"]'.format(element))
    Task = driver.find_element_by_xpath('//*[@id="row_vss_11_{}"]/div[1]'.format(element))
    print('THIS IS TASK #{}'.format(Task.text))
    print(new_page_element.text)
    time.sleep(wait/2)








































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