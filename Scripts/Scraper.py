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
    "Pandey, Sampurnanand":"SAMPURNANAND", "Singh, Upasana":"UPASANA", 
    "Sellers, Eric R": "ERIC", "Sperry, Jonathan A":"JONATHAN"
    }

class Scrape:
    
    
    def __init__(self, Username, Password, URL):
        self.Username = Username
        self.Password = Password
        self.URL = URL
        self.ModifiedURL = self.MakeURL(self.URL)
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(options=self.options)
        self.DaysSinceLastReport = 1
        self.SecondsSinceLastReport = self.DaysSinceLastReport * 60 * 60 * 24
        self.N = 1000
        self.elements = range(0,self.N)
        self.ToDoCounter = 0
        self.NewTasks = []
        self.PreviousTasks = []
        self.PriorityTasks = []
        
    
    def MakeURL(self, URL):
        
        NoHTTPURL = ''
        for i in range(0, len(URL)):
            if i > 6:
                NoHTTPURL += URL[i]
            else:
                pass
            
        ModifiedURL = 'http://' + '{}:{}@'.format(self.Username, self.Password) + NoHTTPURL
        return ModifiedURL
    
    
    def Clicker(self, xpath):
        # time.sleep(1)
        result = None
        tried = 0
        while result is None:
            tried += 1
            try:
                Element = self.driver.find_element_by_xpath(xpath)
                Element.click()
                result = Element
            except:
                pass
            
            if tried >= 100:
                print("Couldn't find {}".format(xpath))
                break        


    def Handler(self):
        
        
        ColumnOptions = '//*[@id="mi_71_column-options"]'
        self.Clicker(ColumnOptions)
        
        
        CreatedDate = '//*[contains(text(), "Created Date")]'
        self.Clicker(CreatedDate)
        
        
        ArrowButton = '/html/body/div[4]/div[2]/div/div[4]/div[1]/div[1]/div[3]/div[1]/button/span/span'
        self.Clicker(ArrowButton)
        
        
        BacklogPriority = '//*[contains(text(), "Backlog Priority")]'
        self.Clicker(BacklogPriority)
        
        
        ArrowButton = '/html/body/div[4]/div[2]/div/div[4]/div[1]/div[1]/div[3]/div[1]/button/span/span'
        self.Clicker(ArrowButton)
        
        
        OK = '//button[@id="ok"]'
        self.Clicker(OK)
        
        CreatedDateColumn = '//*[@id="vss_11"]/div[1]/div[1]/div[7]/div[2]'
        self.Clicker(CreatedDateColumn)
        self.Clicker(CreatedDateColumn)

    def TaskExtractor(self, element):
        # going = False
        # while going == False:
            
        #     NumTasks = '//*[@id="vss_186"]/div/div[2]/div[1]'
        #     NumTasks = self.driver.find_element_by_xpath(NumTasks)
        #     if NumTasks.text != 'Querying...':
                
        #         going = True
            
        # NumTasks = NumTasks.text
        # list(NumTasks)
        # NumTasks = int(NumTasks[0] + NumTasks[1])
        
        # result = None
        # tried = 0
        # counter = 0
        # while result is None:
        #     tried += 1
        #     try:

        xpath = '//*[@id="vss_11"]/div[2]'
        ScrollDown = self.driver.find_element_by_xpath(xpath)
        ScrollDown.send_keys(Keys.ARROW_DOWN)
        # result = ScrollDown()
        #         if result is not None:
        #             counter += 1
        #         if counter == NumTasks - 2:
        #             result = True
        #             print(counter)

        #     except:
        #         pass
            
            # if tried >= 100:
            #     print("Couldn't find {}".format(xpath))
            #     break        

        self.TaskPriority = 0

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
        
        Priority = self.driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]/div[8]'.format(element))
        Priority = Priority.text

        if Priority == '3':
            self.TaskPriority = int(Priority)
        else:
            pass


        self.Person = Names[self.TaskPerson.text]
        self.TaskTime = time.strptime(TaskTime.text, "%m/%d/%Y %I:%M %p")
        self.TaskTimeSec = time.mktime(self.TaskTime)
        Today = time.gmtime()
        self.TodaySec = time.mktime(Today)
                
        
