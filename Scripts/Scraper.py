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
    
    
    def Parser(self, Section):
        
        for i in range(0,len(self.Tasks)):
            self.Tasks[i]['{}'.format(Section)]
            
            """
            
            This is fucked. How to do this?????
            
            """
        
    def Clicker(self, xpath):
        time.sleep(.5)
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

    def TaskExtractor(self, Section):
        elements = range(0,1000)
        
        try:
            
            for element in elements:
                xpath = '//*[@id="vss_11"]/div[2]'
                ScrollDown = self.driver.find_element_by_xpath(xpath)
                ScrollDown.send_keys(Keys.ARROW_DOWN)
        
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
            if self.Tasks[i]['Type'] == 'To Do':
                hl = 'yellow'
                if self.Tasks[i]['Priority'] == '1':
                    
                    self.PriorityTasks.append(
                        '\\item \\hl{{}}{{}} {{}}: {{}}'.format(
                        hl, self.Tasks[i]['Number'], self.Tasks[i]['Person'], 
                        self.Tasks[i]['Description']))
                    
                elif self.Tasks[i]['Time'] - self.TodaySec < self.SecondsSinceLastReport:
                    self.NewTasks.append(
                        '\\item \\hl{{}}{{}} {{}}: {{}}'.format(
                        hl, self.Tasks[i]['Number'], self.Tasks[i]['Person'], 
                        self.Tasks[i]['Description']))
                else:
                    self.PreviousTasks.append(
                        '\\item \\hl{{}}{{}} {{}}: {{}}'.format(
                        hl, self.Tasks[i]['Number'], self.Tasks[i]['Person'], 
                        self.Tasks[i]['Description']))
            
            
            if self.Tasks[i]['Type'] == 'Test':
                hl = 'cyan'
                if self.Tasks[i]['Priority'] == '1':
                    
                    self.PriorityTasks.append(
                        '\\item \\hl{}{{{}}} {}: {}'.format(
                        hl, self.Tasks[i]['Number'], self.Tasks[i]['Person'], 
                        self.Tasks[i]['Description']))
                    
                elif self.Tasks[i]['Time'] - self.TodaySec < self.SecondsSinceLastReport:
                    self.NewTasks.append(
                        '\\item \\hl{}{{{}}} {}: {}'.format(
                        hl, self.Tasks[i]['Number'], self.Tasks[i]['Person'], 
                        self.Tasks[i]['Description']))
                else:
                    self.PreviousTasks.append(
                        '\\item \\hl{}{{{}}} {}: {}'.format(
                        hl, self.Tasks[i]['Number'], self.Tasks[i]['Person'], 
                        self.Tasks[i]['Description']))
        
        
            if self.Tasks[i]['Type'] == 'Completed':
                hl = 'green'
                if self.Tasks[i]['Priority'] == '1':
                    
                    self.PriorityTasks.append(
                        '\\item \\hl{}{{{}}} {}: {}'.format(
                        hl, self.Tasks[i]['Number'], self.Tasks[i]['Person'], 
                        self.Tasks[i]['Description']))
                    
                elif self.Tasks[i]['Time'] - self.TodaySec < self.SecondsSinceLastReport:
                    self.NewTasks.append(
                        '\\item \\hl{}{{{}}} {}: {}'.format(
                        hl, self.Tasks[i]['Number'], self.Tasks[i]['Person'], 
                        self.Tasks[i]['Description']))
                else:
                    self.PreviousTasks.append(
                        '\\item \\hl{}{{{}}} {}: {}'.format(
                        hl, self.Tasks[i]['Number'], self.Tasks[i]['Person'], 
                        self.Tasks[i]['Description']))
                    
# \item \hlyellow{12157} ERIC: Could Not Finish Flow


# '\\item \\hl{{}}{{}} {{}}: {{}}'.format(
#     hl, self.Task[i]['Number'], self.Task[i]['Person'], 
#     self.Task[i]['Description'])
