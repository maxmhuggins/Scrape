#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 10:42:39 2020

@author: ***REMOVED***
"""

from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

Names = {
    "David Palos":"PALOS", "Babb, David A":"BABB", "Huggins, Max":"MAX", 
    "Patton, Matthew":"MATTHEW", "Sharma, Kuldeep":"KULDEEP", 
    "Brown, Adam C.":"ADAM", "Pulapa, Rajani K.":"RAJANI", 
    "Bansal, Aman":"AMAN", "Khurana, Simran":"SIMRAN", 
    "Pandey, Sampurnanand":"SAMPURNANAND", "Singh, Upasana":"UPASANA"
    }

class Scrape:
    
    
    def __init__(self, Username, Password, URL):
        self.Username = Username
        self.Password = Password
        self.URL = URL
        self.ModifiedURL = self.MakeURL(self.URL)
        self.wait = 1
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(options=self.options)
        self.DaysSinceLastReport = .5
        self.SecondsSinceLastReport = self.DaysSinceLastReport * 60 * 60 * 24
        self.N = 1000
        self.elements = range(0,self.N)
        self.ToDoCounter = 0
        self.NewTasks = []
        self.PreviousTasks = []
        
    
    def MakeURL(self, URL):
        
        NoHTTPURL = ''
        for i in range(0, len(URL)):
            if i > 6:
                NoHTTPURL += URL[i]
            else:
                pass
            
        ModifiedURL = 'http://' + '{}:{}@'.format(self.Username, self.Password) + NoHTTPURL
        return ModifiedURL


    def Handler(self):
        
        # self.driver.refresh()
        time.sleep(self.wait)
        ColumnOptionsButton = self.driver.find_element_by_xpath('''//*[@id="mi_71_column-options"]''')
        ColumnOptionsButton.click()
        time.sleep(self.wait)
        
        CreatedDate = self.driver.find_element_by_xpath('//*[contains(text(), "Created Date")]')
        CreatedDate.click()
        time.sleep(self.wait)
        
        ArrowButton = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[4]/div[1]/div[1]/div[3]/div[1]/button/span/span')
        ArrowButton.click()
        time.sleep(self.wait)

        OK = self.driver.find_element_by_xpath('//button[@id="ok"]')
        OK.click()
        time.sleep(self.wait)

    
    def TaskExtractor(self, element):
        ScrollDown = self.driver.find_element_by_xpath('//*[@id="vss_11"]/div[2]')
        ScrollDown.send_keys(Keys.ARROW_DOWN)

        new_page_element = self.driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]'.format(element))
        
        self.TaskNumber = self.driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]/div[1]'.format(element))
        
        self.TaskDescription = self.driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]/div[3]'.format(element))
        
        self.TaskPerson = self.driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]/div[4]'.format(element))
        
        TaskTime = self.driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]/div[7]'.format(element))
        self.Person = Names[self.TaskPerson.text]
        self.TaskTime = time.strptime(TaskTime.text, "%m/%d/%Y %I:%M %p")
        self.TaskTimeSec = time.mktime(self.TaskTime)
        Today = time.gmtime()
        self.TodaySec = time.mktime(Today)
        
        
        
        
        
        
        