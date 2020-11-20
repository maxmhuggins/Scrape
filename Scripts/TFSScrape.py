#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 19:06:22 2020

@author: ***REMOVED***
This is an attempt to scrape info from tfs to automate the task report.
"""
#============================================================================#
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import subprocess
import Scraper       
#============================================================================#
Username = '***REMOVED***'
Password = 'uCfE2ahPM8C89CZ'
Sprint = input('Please input the Sprint number:')
URL = 'http://conw-mstf-01-pv.snaponglobal.com:8080/tfs/Embedded%20Engineering%20Collection/Agile%20Sanctuary/_backlogs/TaskBoard/2020/Sprint%20{}?_a=requirements'.format(Sprint)
DaysSinceLastReport = 5
SecondsSinceLastReport = DaysSinceLastReport * 60 * 60 * 24
N = 1000
elements = range(0,N)
ToDoCounter = 0
NewTasks = []
PreviousTasks = []
Names = {"David Palos":"PALOS", "Babb, David A":"BABB", "Huggins, Max":"MAX", "Patton, Matthew":"MATTHEW", "Sharma, Kuldeep":"KULDEEP", "Brown, Adam C.":"ADAM", "Pulapa, Rajani K.":"RAJANI", "Bansal, Aman":"AMAN", "Khurana, Simran":"SIMRAN", "Pandey, Sampurnanand":"SAMPURNANAND", "Singh, Upasana":"UPASANA", }


S = Scraper.Scrape(Username, Password, URL)    
wait = S.wait
URL = S.ModifiedURL
#============================================================================#
options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
#============================================================================#
driver.get(URL)
time.sleep(wait*2)
QueriesButton = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/table[2]/tbody/tr/td/div[1]/div/table/tbody/tr/td[1]/div[2]/div/ul/li[2]/a')
QueriesButton.click()
time.sleep(wait)
#============================================================================#
WorkInTest = driver.find_element_by_xpath('//*[@id="tfs_tnli17"]')
WorkInTest.click()
time.sleep(wait)


ColumnOptionsButton = driver.find_element_by_xpath('''//*[@id=
                                                   "mi_71_column-options"]''')
ColumnOptionsButton.click()
time.sleep(wait)


CreatedDate = driver.find_element_by_xpath('//*[contains(text(), "Created Date")]')
CreatedDate.click()
time.sleep(wait)


ArrowButton = driver.find_element_by_xpath('//button[@class="add ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only"]')
ArrowButton.click()
time.sleep(wait)

OK = driver.find_element_by_xpath('//*[@id="ok"]')
OK.click()
time.sleep(wait)


try:
    for element in elements:
        ScrollDown = driver.find_element_by_xpath('//*[@id="vss_11"]/div[2]')
        ScrollDown.send_keys(Keys.ARROW_DOWN)

        new_page_element = driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]'.format(element))
        
        TaskNumber = driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]/div[1]'.format(element))
        
        TaskDescription = driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]/div[3]'.format(element))
        
        TaskPerson = driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]/div[4]'.format(element))
        
        TaskTime = driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]/div[7]'.format(element))
        Person = Names[TaskPerson.text]
        TaskTime = time.strptime(TaskTime.text, "%m/%d/%Y %I:%M %p")
        TaskTimeSec = time.mktime(TaskTime)
        Today = time.gmtime()
        TodaySec = time.mktime(Today)
        Task = '\\item \\hlcyan{{{}}} {}: {}\n'.format(
        TaskNumber.text, Person, TaskDescription.text)
        
        if TodaySec > TaskTimeSec + SecondsSinceLastReport:
            PreviousTasks.append(Task)
        else:
            NewTasks.append(Task)

except NoSuchElementException:
    print('There are {} tasks in Test'.format(element + 1))
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

try:
    for element in elements:
        ScrollDown = driver.find_element_by_xpath('//*[@id="vss_11"]/div[2]')
        ScrollDown.send_keys(Keys.ARROW_DOWN)
        
        new_page_element = driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]'.format(element))
        
        TaskNumber = driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]/div[1]'.format(element))
        
        TaskDescription = driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]/div[3]'.format(element))
        
        TaskPerson = driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]/div[4]'.format(element))
        
        TaskTime = driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]/div[7]'.format(element))
        Person = Names[TaskPerson.text]
        TaskTime = time.strptime(TaskTime.text, "%m/%d/%Y %I:%M %p")
        TaskTimeSec = time.mktime(TaskTime)
        Today = time.gmtime()
        TodaySec = time.mktime(Today)
        
        
        Task = '\\item \\hlyellow{{{}}} {}: {}\n'.format(
        TaskNumber.text, Person, TaskDescription.text)
        if TodaySec > TaskTimeSec + SecondsSinceLastReport:
            PreviousTasks.append(Task)
        else:
            NewTasks.append(Task)
        
        ToDoCounter += 1
except NoSuchElementException:
    pass     
#============================================================================#
WorkInProgress = driver.find_element_by_xpath('//*[@id="tfs_tnli16"]')
WorkInProgress.click()

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

try:
    for element in elements:
        ScrollDown = driver.find_element_by_xpath('//*[@id="vss_11"]/div[2]')
        ScrollDown.send_keys(Keys.ARROW_DOWN)
        
        new_page_element = driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]'.format(element))
        
        TaskNumber = driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]/div[1]'.format(element))
        
        TaskDescription = driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]/div[3]'.format(element))
        
        TaskPerson = driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]/div[4]'.format(element))
        
        TaskTime = driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]/div[7]'.format(element))
        Person = Names[TaskPerson.text]
        TaskTime = time.strptime(TaskTime.text, "%m/%d/%Y %I:%M %p")
        TaskTimeSec = time.mktime(TaskTime)
        Today = time.gmtime()
        TodaySec = time.mktime(Today)
        
        
        Task = '\\item \\hlyellow{{{}}} {}: {}\n'.format(
        TaskNumber.text, Person, TaskDescription.text)
        if TodaySec > TaskTimeSec + SecondsSinceLastReport:
            PreviousTasks.append(Task)
        else:
            NewTasks.append(Task)
        
        ToDoCounter += 1
except NoSuchElementException:
    print('There are {} tasks in To Do'.format(ToDoCounter))
#============================================================================#
WorkInCompleted = driver.find_element_by_xpath('//*[@id="tfs_tnli9"]')
WorkInCompleted.click()
time.sleep(wait)


ColumnOptionsButton = driver.find_element_by_xpath('''//*[@id=
                                                   "mi_71_column-options"]''')
ColumnOptionsButton.click()
time.sleep(wait)


CreatedDate = driver.find_element_by_xpath('//*[contains(text(), "Created Date")]')
CreatedDate.click()
time.sleep(wait)


ArrowButton = driver.find_element_by_xpath('//button[@class="add ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only"]')
ArrowButton.click()
time.sleep(wait)

OK = driver.find_element_by_xpath('//*[@id="ok"]')
OK.click()
time.sleep(wait)

try:
    for element in elements:
        ScrollDown = driver.find_element_by_xpath('//*[@id="vss_11"]/div[2]')
        ScrollDown.send_keys(Keys.ARROW_DOWN)

        new_page_element = driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]'.format(element))
        
        TaskNumber = driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]/div[1]'.format(element))
        
        TaskDescription = driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]/div[3]'.format(element))
        
        TaskPerson = driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]/div[4]'.format(element))
        
        TaskTime = driver.find_element_by_xpath(
            '//*[@id="row_vss_11_{}"]/div[7]'.format(element))
        Person = Names[TaskPerson.text]
        TaskTime = time.strptime(TaskTime.text, "%m/%d/%Y %I:%M %p")
        TaskTimeSec = time.mktime(TaskTime)
        Today = time.gmtime()
        TodaySec = time.mktime(Today)
        Task = '\\item \\hlgreen{{{}}} {}: {}\n'.format(
        TaskNumber.text, Person, TaskDescription.text)
        
        if TodaySec > TaskTimeSec + SecondsSinceLastReport:
            PreviousTasks.append(Task)
        else:
            NewTasks.append(Task)

except NoSuchElementException:
    print('There are {} tasks in Completed'.format(element + 1))
#============================================================================#
with open('../Latex/TFSTesting.tex','w') as file:
    
    file.write('\\input{./Sections/Top}\n')
    
    file.write('''\\begin{{document}}\n
\\begin{{center}}\n
\\Large\n
\\textsc{{GTPS Task Report for Sprint {}}}\\\n
\\normalsize \\today\n
\\end{{center}}\\vspace{{1.5cm}}\n'''.format(Sprint))
    
    file.write('''\\large\n
\\textsc{{New Tasks}}\n
\\normalsize\n''')

    file.write('\\begin{enumerate}\n')
    
    for Task in NewTasks:
        file.write(Task)


    file.write('\\end{enumerate}\\vspace{.5cm}\n')

    file.write('''\\large\n
\\textsc{{Previous Tasks}}\n
\\normalsize\n''')

    file.write('\\begin{enumerate}\n')
    
    for Task in PreviousTasks:
        file.write(Task)


    file.write('\\end{enumerate}\\vspace{.5cm}\n')

    file.write('\\end{document}')
#============================================================================#



"""
Need to clean up some of the hard code. No need for there to be so many
repeated lines. Also, comments of course. More importantly though I need
some method of handling weird characters like &'s and what not. The latex
compiler is unhappy with that and just leaves it out.

In the end, I will need some method of storing old tasks so that the task 
report has older tasks on it. Possibly just use a .txt file to store the
old strings and just append them at the end of the tex file.

Lastly, need to have user input UN and PASS for security purposes
    
"""

time.sleep(wait)


driver.close()

subprocess.Popen(['rubber', '-d', 'TFSTesting.tex'],  cwd="../Latex")
time.sleep(2)
subprocess.Popen(['rubber', '--clean', 'TFSTesting.tex'],  cwd="../Latex")
time.sleep(3)
print('Opening document')
subprocess.Popen(['okular', 'TFSTesting.pdf'],  cwd="../Latex")
