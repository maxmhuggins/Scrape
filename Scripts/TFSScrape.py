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
# Sprint = input('Please input the Sprint number:')
Sprint=17
URL = '''http://conw-mstf-01-pv.snaponglobal.com:8080/tfs/Embedded%20
Engineering%20Collection/Agile%20Sanctuary/_backlogs/TaskBoard/2020/
Sprint%20{}?_a=requirements'''.format(Sprint)
#============================================================================#
S = Scraper.Scrape(Username, Password, URL)    
wait = S.wait
URL = S.ModifiedURL
#============================================================================#
S.driver.get(URL)
time.sleep(wait*2)
QueriesButton = S.driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/table[2]/tbody/tr/td/div[1]/div/table/tbody/tr/td[1]/div[2]/div/ul/li[2]/a')
QueriesButton.click()
time.sleep(wait)
#============================================================================#
WorkInToDo = S.driver.find_element_by_xpath('//*[@id="tfs_tnli18"]')
WorkInToDo.click()

S.Handler()

try:
    for element in S.elements:
        
        S.TaskExtractor(element)        
        
        Task = '\\item \\hlyellow{{{}}} {}: {}\n'.format(
        S.TaskNumber.text, S.Person, S.TaskDescription.text)
        
        if S.TodaySec > S.TaskTimeSec + S.SecondsSinceLastReport:
            S.PreviousTasks.append(Task)
        else:
            S.NewTasks.append(Task)
                
        S.ToDoCounter += 1
except NoSuchElementException:
    pass     
#============================================================================#
WorkInTest = S.driver.find_element_by_xpath('//*[@id="tfs_tnli17"]')
WorkInTest.click()
time.sleep(wait)

S.Handler()

try:
    for element in S.elements:
        
        S.TaskExtractor(element)        
        
        Task = '\\item \\hlcyan{{{}}} {}: {}\n'.format(
        S.TaskNumber.text, S.Person, S.TaskDescription.text)
        
        if S.TodaySec > S.TaskTimeSec + S.SecondsSinceLastReport:
            S.PreviousTasks.append(Task)
        else:
            S.NewTasks.append(Task)

except NoSuchElementException:
    print('There are {} tasks in Test'.format(element + 1))
#============================================================================#
WorkInProgress = S.driver.find_element_by_xpath('//*[@id="tfs_tnli16"]')
WorkInProgress.click()
time.sleep(wait)

S.Handler()

try:
    for element in S.elements:
        
        S.TaskExtractor(element)        
        
        Task = '\\item \\hlyellow{{{}}} {}: {}\n'.format(
        S.TaskNumber.text, S.Person, S.TaskDescription.text)
        
        if S.TodaySec > S.TaskTimeSec + S.SecondsSinceLastReport:
            S.PreviousTasks.append(Task)
        else:
            S.NewTasks.append(Task)
        
        S.ToDoCounter += 1
except NoSuchElementException:
    print('There are {} tasks in To Do'.format(S.ToDoCounter))
#============================================================================#
WorkInCompleted = S.driver.find_element_by_xpath('//*[@id="tfs_tnli9"]')
WorkInCompleted.click()
time.sleep(wait)

S.Handler()

try:
    for element in S.elements:
        
        S.TaskExtractor(element)        
        
        Task = '\\item \\hlgreen{{{}}} {}: {}\n'.format(
        S.TaskNumber.text, S.Person, S.TaskDescription.text)
        
        if S.TodaySec > S.TaskTimeSec + S.SecondsSinceLastReport:
            S.PreviousTasks.append(Task)
        else:
            S.NewTasks.append(Task)

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
    
    for Task in S.NewTasks:
        Task = list(Task)
        for i in range(0,len(Task)):
            if Task[i] == '&':
                Task[i] = '\&'
            else:
                pass
        Task = ''.join(Task)
        file.write(Task)


    file.write('\\end{enumerate}\\vspace{.5cm}\n')

    file.write('''\\large\n
\\textsc{{Previous Tasks}}\n
\\normalsize\n''')

    file.write('\\begin{enumerate}\n')
    
    for Task in S.PreviousTasks:
        Task = list(Task)
        for i in range(0,len(Task)):
            if Task[i] == '&':
                Task[i] = '\&'
            else:
                pass
        Task = ''.join(Task)
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

need to replace wait time with an exception handler...

Lastly, need to have user input UN and PASS for security purposes
    
"""

time.sleep(wait)


S.driver.close()

subprocess.Popen(['rubber', '-d', 'TFSTesting.tex'],  cwd="../Latex")
time.sleep(2)
subprocess.Popen(['rubber', '--clean', 'TFSTesting.tex'],  cwd="../Latex")
time.sleep(3)
print('Opening document')
subprocess.Popen(['okular', 'TFSTesting.pdf'],  cwd="../Latex")
