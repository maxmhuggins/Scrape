#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 10:42:39 2020

@author: ***REMOVED***
"""
#============================================================================#
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import operator
#============================================================================#
"""
This is the names dictionary. It holds all of the TFS names and assigns them
nicknames to be displayed on the report.
"""
Names = {
    "David Palos":"PALOS", "Babb, David A":"BABB", "Huggins, Max":"MAX", 
    "Patton, Matthew":"MATTHEW", "Sharma, Kuldeep":"KULDEEP", 
    "Brown, Adam C.":"ADAM", "Pulapa, Rajani K.":"RAJANI", 
    "Bansal, Aman":"AMAN", "Khurana, Simran":"SIMRAN", 
    "Pandey, Sampurnanand":"SAM", "Singh, Upasana":"UPASANA", 
    "Sellers, Eric R": "ERIC", "Sperry, Jonathan A":"JONATHAN",
    "LeCrone, Sean": "SEAN", "Robinson, Chance W":"CHANCE"
    }
#============================================================================#
"""
The Scrape class handles most of the scraping from TFS. It also includes some
attributes for the report and handles task dictionaries.
"""
class Scrape:
    
    def __init__(self, Username, Password, Sprint, URL):
        """Either input name here, or uncomment the input commands and do it on 
        startup. The latter is more secure."""
        self.Username = Username
        self.Password = Password
        self.Sprint = Sprint    
        self.TitleSprint = str(self.Sprint)
        self.TitleDate = time.strftime('%m-%d-%y Hr-%H',time.localtime())
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
        
    """The MakeURL method will make an authentication URL so you can get into
    TFS without having to manually log in."""
    def MakeURL(self, URL):
        
        NoHTTPURL = ''
        for i in range(0, len(URL)):
            if i > 6:
                NoHTTPURL += URL[i]
            else:
                pass
            
        ModifiedURL = 'http://' + '{}:{}@'.format(self.Username, self.Password) + NoHTTPURL
        return ModifiedURL
    
    
    """The Clicker method literally clicks on an xpath element. There is a 
    try, except in place for unloaded elements."""       
    def Clicker(self, xpath):
        
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
      
            
    """The Appender method will make a dictionary for each task that includes
    priority and the string that will get put into the latex document."""
    def Appender(self, Tasks, hl):
        
        T = Tasks['Priority']
        if T != ' ':
            if Tasks['Type'] == 'Completed':
                pass
            else:
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
                    {
                    'String':'\\item \\hl{}{{{}}} {}: {}'.format(
                    hl, Tasks['Number'], Tasks['Person'], 
                    Tasks['Description']),
                    
                    'Priority':None
                    }
                                          )
        else:
            self.PreviousTasks.append(
                    {
                    'String':'\\item \\hl{}{{{}}} {}: {}'.format(
                    hl, Tasks['Number'], Tasks['Person'], 
                    Tasks['Description']),
                    
                    'Priority':None
                    }
                                          )
    
    
    """The Handler method makes a unique query that includes the date the task
    was created as well as the backlog priority."""
    def Handler(self):
        
        ColumnOptions = '//*[@id="mi_71_column-options"]'
        self.Clicker(ColumnOptions)
        
        
        CreatedDate = '//*[contains(text(), "Created Date")]'
        self.Clicker(CreatedDate)
        
        
        ArrowButton = """/html/body/div[4]/div[2]/div/div[4]/div[1]/div[1]/
        div[3]/div[1]/button/span/span"""
        self.Clicker(ArrowButton)
        
        
        BacklogPriority = '//*[contains(text(), "Backlog Priority")]'
        self.Clicker(BacklogPriority)
        
        
        ArrowButton = """/html/body/div[4]/div[2]/div/div[4]/div[1]/div[1]/
        div[3]/div[1]/button/span/span"""
        self.Clicker(ArrowButton)
        
        
        OK = '//button[@id="ok"]'
        self.Clicker(OK)
        
        CreatedDateColumn = '//*[@id="vss_11"]/div[1]/div[1]/div[7]/div[2]'
        self.Clicker(CreatedDateColumn)
        self.Clicker(CreatedDateColumn)
    
    
    """The TaskExtractor method grabs all of the relevant data from TFS
    regarding the task, stores it in a dictionary and appends it to a list."""
    def TaskExtractor(self, Section):
        
        elements = range(0,1000)
        
        try:
            
            for element in elements:
                xpath = '//*[@id="vss_11"]/div[2]'
                ScrollDown = self.driver.find_element_by_xpath(xpath)
                ScrollDown.send_keys(Keys.ARROW_DOWN)
                                
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
    
    
    """The StringMaker method will sort the list of dictionaries by date,
    assign colors to the highlighter, then send the task to the Appender"""
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
        
    
    def StringFixer(self, Task):
        Task = Task['String']
        Task = list(Task)
        for i in range(0,len(Task)):
            if Task[i] == '&':
                Task[i] = '\&'
            if Task[i] == '$':
                Task[i] = '\$'
            if Task[i] == '_':
                Task[i] = '\_'                
            else:
                pass
        Task = ''.join(Task)
        return Task
    
    
    def SectionMaker(self, file, CurrentCategory):
        if len(CurrentCategory) == 0:
            file.write('\\textit{No top priority tasks to display.}\\vspace{.5cm}\n')
        else:
            file.write(
                '\\begin{enumerate}[leftmargin=!,labelindent=5pt,itemindent=-35pt]\n')
            
            for Task in CurrentCategory:
                file.write(self.StringFixer(Task) + '\n')
        
        
            file.write('\\end{enumerate}\\vspace{.5cm}\n')
    
    def ReportGenerator(self):
        with open('../GeneratedReports/Sprint {} GTPS Task Report {}.tex'.format(
                self.TitleSprint, self.TitleDate),'w') as file:
            
            file.write('''\\documentclass[letterpaper, 12pt]{article}\n
        \\usepackage[utf8]{inputenc}\n
        \\usepackage[margin=1in,letterpaper]{geometry}\n
        \\usepackage[stretch=10]{microtype}\n
        \\usepackage[table,xcdraw]{xcolor}\n
        \\usepackage{listings}\n
        \\usepackage{color}\n
        \\usepackage{xcolor, soul}\n
        \\usepackage{enumitem}\n
        \\usepackage[en-GB,showseconds=false, showzone=false]{datetime2}\n
        \\definecolor{navy}{rgb}{245,156,74}\n
        \\definecolor{codegreen}{rgb}{0,0.6,0}\n
        \\definecolor{codegray}{rgb}{0.5,0.5,0.5}\n
        \\definecolor{codepurple}{rgb}{0.58,0,0.82}\n
        \\definecolor{backcolour}{rgb}{0.95,0.95,0.92}\n
        \\DeclareRobustCommand{\\hlcyan}[1]{{\\sethlcolor{cyan}\\hl{#1}}}\n
        \\DeclareRobustCommand{\\hlyellow}[1]{{\\sethlcolor{yellow}\\hl{#1}}}\n
        \\DeclareRobustCommand{\\hlgreen}[1]{{\\sethlcolor{green}\\hl{#1}}}\n
        \\DeclareRobustCommand{\\hlpurple}[1]{{\\sethlcolor{codepurple}\\hl{#1}}}\n''')
            
            file.write('''\\begin{{document}}\n
        \\begin{{center}}\n
        \\Large\n
        \\textsc{{GTPS Task Report for Sprint {}}}\\\n
        \\normalsize \\DTMnow\n
        \\end{{center}}\\vspace{{1.5cm}}\n'''.format(self.Sprint))
        
        
        
            file.write('''\\large\n
        \\textsc{{Top Priority Tasks}}\n
        \\normalsize\n''')
        
            CurrentCategory = self.PriorityTasks
            self.SectionMaker(file, CurrentCategory)
        
            file.write('''\\large\n
        \\textsc{{Tasks Created in the Last {}hrs}}\n
        \\normalsize\n'''.format(str(self.DaysSinceLastReport*24)))
        
            CurrentCategory = self.NewTasks
            self.SectionMaker(file, CurrentCategory)
        
            file.write('''\\large\n
        \\textsc{{Previous Tasks}}\n
        \\normalsize\n''')
        
            CurrentCategory = self.PreviousTasks
            self.SectionMaker(file, CurrentCategory)
                        
        
        
            file.write('\\end{document}')
