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
import matplotlib.pyplot as plt
import subprocess, os


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
# options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

driver.get(URL)
time.sleep(wait*2)
QueriesButton = driver.find_element_by_xpath('//*[@id="mi_258_ms.vss-work-web.work-hub"]')
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

ScrollDown = driver.find_element_by_xpath('//*[@id="vss_11"]/div[2]')
ScrollDown.send_keys(Keys.END)
N = 6 #Need to find out how to handle last task in list
elements = range(0,N)
with open('../Latex/TFSTesting.tex','w') as file:
    
    file.write('\\input{./Sections/Top}\n')
    file.write('''\\large
                \\textsc{{New Tasks}}
                \\normalsize''')

    file.write('\\begin{enumerate}')
    
    for element in elements:
        new_page_element = driver.find_element_by_xpath('//*[@id="row_vss_11_{}"]'.format(element))
        TaskNumber = driver.find_element_by_xpath('//*[@id="row_vss_11_{}"]/div[1]'.format(element))
        TaskDescription = driver.find_element_by_xpath('//*[@id="row_vss_11_{}"]/div[3]'.format(element))
        TaskPerson = driver.find_element_by_xpath('//*[@id="row_vss_11_{}"]/div[4]'.format(element))
        Task = '\\item \\hlcyan{{{}}} {}: {}'.format(TaskNumber.text, TaskPerson.text, TaskDescription.text)
        file.write(Task)
        time.sleep(wait/2)
        
    file.write('\\end{enumerate}\\vspace{.5cm}')
    
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
    
    ScrollDown = driver.find_element_by_xpath('//*[@id="vss_11"]/div[2]')
    ScrollDown.send_keys(Keys.END)
    
    file.write('''\\large
                \\textsc{{Previous Tasks}}
                \\normalsize''')

    file.write('\\begin{enumerate}')
    N = 6 #Need to find out how to handle last task in list
    elements = range(0,N)

    for element in elements:
        new_page_element = driver.find_element_by_xpath('//*[@id="row_vss_11_{}"]'.format(element))
        TaskNumber = driver.find_element_by_xpath('//*[@id="row_vss_11_{}"]/div[1]'.format(element))
        TaskDescription = driver.find_element_by_xpath('//*[@id="row_vss_11_{}"]/div[3]'.format(element))
        TaskPerson = driver.find_element_by_xpath('//*[@id="row_vss_11_{}"]/div[4]'.format(element))
        Task = '\\item \\hlyellow{{{}}} {}: {}'.format(TaskNumber.text, TaskPerson.text, TaskDescription.text)
        file.write(Task)
        time.sleep(wait/2)
        
    file.write('\\end{enumerate}\\vspace{.5cm}')
    
    5
    
    
    
    
    file.write('\\end{document}')


"""
Also need to add in logic to determine the highlight color, which section to put 
strings in, and handling priority tasks. 

can use: time.strptime(x, "%m/%d/%Y %I:%M %p") to get time into workable 
format for the logic to determine what goes in new tasks.
Today is given by time.gmtime(). Simple comparisons can be made for example:
    then = time.strptime(x, "%m/%d/%Y %I:%M %p")
    now = time.gmtime()
    then < now
    True
    
The color can be handled quite simply by which section we are scraping from.

Once this information is determined, the strings should be stored in a list
and the list will be iterated for each section.

In the end, I will need some method of storing old tasks so that the task 
report has older tasks on it. Possibly just use a .txt file to store the
old strings and just append them at the end of the tex file.
    
"""

time.sleep(3)


driver.close()

subprocess.Popen(['rubber', '-d', 'TFSTesting.tex'],  cwd="../Latex")
time.sleep(2)
subprocess.Popen(['rubber', '--clean', 'TFSTesting.tex'],  cwd="../Latex")
time.sleep(3)
print('Opening document')
subprocess.Popen(['okular', 'TFSTesting.pdf'],  cwd="../Latex")
