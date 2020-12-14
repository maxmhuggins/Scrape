#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 10:42:39 2020

@author: ***REMOVED***
"""

from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import operator

Names = {
    "David Palos":"PALOS", "Babb, David A":"BABB", "Huggins, Max":"MAX", 
    "Patton, Matthew":"MATTHEW", "Sharma, Kuldeep":"KULDEEP", 
    "Brown, Adam C.":"ADAM", "Pulapa, Rajani K.":"RAJANI", 
    "Bansal, Aman":"AMAN", "Khurana, Simran":"SIMRAN", 
    "Pandey, Sampurnanand":"SAM", "Singh, Upasana":"UPASANA", 
    "Sellers, Eric R": "ERIC", "Sperry, Jonathan A":"JONATHAN",
    "LeCrone, Sean": "SEAN"
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
        self.DaysSinceLastReport = 3
        self.SecondsSinceLastReport = self.DaysSinceLastReport * 60 * 60 * 24
        self.TodaySec = time.mktime(time.gmtime())
        self.Tasks = []
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
        # time.sleep(.5)
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

    def Appender(self, Tasks, hl):
        T = Tasks['Priority']
        print(T)
        # time.sleep(15)
        if T != ' ':

            self.PriorityTasks.append(
                {
                'String':'\\item \\hl{}{{{}}} {}: {}'.format(
                hl, Tasks['Number'], Tasks['Person'], 
                Tasks['Description']),
                
                'Priority':Tasks['Priority']
                }
                                      )
            
        elif Tasks['Time'] + self.SecondsSinceLastReport > self.TodaySec:
            self.NewTasks.append(
                '\\item \\hl{}{{{}}} {}: {}'.format(
                hl, Tasks['Number'], Tasks['Person'], 
                Tasks['Description']))
        else:
            self.PreviousTasks.append(
                '\\item \\hl{}{{{}}} {}: {}'.format(
                hl, Tasks['Number'], Tasks['Person'], 
                Tasks['Description']))

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

    def TaskExtractor(self, Section):
        elements = range(0,1000)
        
        try:
            
            for element in elements:
                xpath = '//*[@id="vss_11"]/div[2]'
                ScrollDown = self.driver.find_element_by_xpath(xpath)
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
                
                Priority = self.driver.find_element_by_xpath(
                    '//*[@id="row_vss_11_{}"]/div[8]'.format(element))
        
                self.TaskPriority = Priority.text
                self.Person = Names[self.TaskPerson.text]
                self.TaskTime = time.strptime(TaskTime.text, "%m/%d/%Y %I:%M %p")
                self.TaskTimeSec = time.mktime(self.TaskTime)
                
                Task = {
                    'Time':self.TaskTimeSec,'Type':Section,'Priority':self.TaskPriority,
                    'Number':self.TaskNumber.text,'Person':self.Person,
                    'Description':self.TaskDescription.text
                        }
                
                self.Tasks.append(Task)
                
        except NoSuchElementException:
            pass
        
    def StringMaker(self):
        self.Tasks.sort(key=operator.itemgetter('Time'), reverse=True)
        
        for i in range(0, len(self.Tasks)):
            Tasks = self.Tasks[i]
            if self.Tasks[i]['Type'] == 'To Do':
                hl = 'yellow'
                self.Appender(Tasks, hl)
                
            
        for i in range(0, len(self.Tasks)):
            Tasks = self.Tasks[i]
            if self.Tasks[i]['Type'] == 'Test':
                hl = 'cyan'
                self.Appender(Tasks, hl)

        
        for i in range(0, len(self.Tasks)):
            Tasks = self.Tasks[i]
            if self.Tasks[i]['Type'] == 'Completed':
                hl = 'green'
                self.Appender(Tasks, hl)
        
        self.PriorityTasks.sort(key=operator.itemgetter('Priority'), reverse=False)

"""
Make the lists have a string and priority, then sort priority tasks by their
priority number. Then simply use the string for the actual document.
"""