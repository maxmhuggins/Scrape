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
Sprint=19

# Sprint = input('Please input the Sprint number\n >')
# Username = input('Please input your username\n >')
# Password = input('Please input your password\n >')
URL = '''http://conw-mstf-01-pv.snaponglobal.com:8080/tfs/Embedded%20
Engineering%20Collection/Agile%20Sanctuary/_backlogs/TaskBoard/2020/
Sprint%20{}?_a=requirements'''.format(Sprint)
#============================================================================#
S = Scraper.Scrape(Username, Password, URL)    
URL = S.ModifiedURL
#============================================================================#
S.driver.get(URL)
QueriesButton = '/html/body/div[2]/div/div[1]/table[2]/tbody/tr/td/div[1]/div/table/tbody/tr/td[1]/div[2]/div/ul/li[2]/a'
S.Clicker(QueriesButton)
#============================================================================#
WorkInToDo = '//*[@id="tfs_tnli18"]'
S.Clicker(WorkInToDo)

S.Handler()

try:
    for element in S.elements:
        
        
        S.TaskExtractor(element)        
            
        Task = '\\item \\hlyellow{{{}}} {}: {}\n'.format(
        S.TaskNumber.text, S.Person, S.TaskDescription.text)
        
        if S.TodaySec > S.TaskTimeSec + S.SecondsSinceLastReport:
            if S.TaskPriority == 3:
                S.PriorityTasks.append(Task)
            else:
                S.PreviousTasks.append(Task)
        else:
            if S.TaskPriority == 3:
                S.PriorityTasks.append(Task)
            else:
                S.NewTasks.append(Task)
                
        S.ToDoCounter += 1
except NoSuchElementException:
    print('where is it')
    pass
#============================================================================#
WorkInProgress = S.driver.find_element_by_xpath('//*[@id="tfs_tnli16"]')
WorkInProgress.click()

S.Handler()

try:
    for element in S.elements:
        
        S.TaskExtractor(element)        
        
        Task = '\\item \\hlyellow{{{}}} {}: {}\n'.format(
        S.TaskNumber.text, S.Person, S.TaskDescription.text)
        
        if S.TodaySec > S.TaskTimeSec + S.SecondsSinceLastReport:
            if S.TaskPriority == 3:
                S.PriorityTasks.append(Task)
            else:
                S.PreviousTasks.append(Task)
        else:
            if S.TaskPriority == 3:
                S.PriorityTasks.append(Task)
            else:
                S.NewTasks.append(Task)
        
        S.ToDoCounter += 1
except NoSuchElementException:
    print('There are {} tasks in To Do'.format(S.ToDoCounter))
#============================================================================#
WorkInTest = S.driver.find_element_by_xpath('//*[@id="tfs_tnli17"]')
WorkInTest.click()

S.Handler()

try:
    for element in S.elements:
        
        S.TaskExtractor(element)        
        
        Task = '\\item \\hlcyan{{{}}} {}: {}\n'.format(
        S.TaskNumber.text, S.Person, S.TaskDescription.text)
        
        if S.TodaySec > S.TaskTimeSec + S.SecondsSinceLastReport:
            if S.TaskPriority == 3:
                S.PriorityTasks.append(Task)
            else:
                S.PreviousTasks.append(Task)
        else:
            if S.TaskPriority == 3:
                S.PriorityTasks.append(Task)
            else:
                S.NewTasks.append(Task)

except NoSuchElementException:
    print('There are {} tasks in Test'.format(element))
#============================================================================#
WorkInCompleted = S.driver.find_element_by_xpath('//*[@id="tfs_tnli9"]')
WorkInCompleted.click()

S.Handler()

try:
    for element in S.elements:
        
        S.TaskExtractor(element)        
        
        Task = '\\item \\hlgreen{{{}}} {}: {}\n'.format(
        S.TaskNumber.text, S.Person, S.TaskDescription.text)
        
        if S.TodaySec > S.TaskTimeSec + S.SecondsSinceLastReport:
            if S.TaskPriority == 3:
                S.PriorityTasks.append(Task)
            else:
                S.PreviousTasks.append(Task)
        else:
            if S.TaskPriority == 3:
                S.PriorityTasks.append(Task)
            else:
                S.NewTasks.append(Task)

except NoSuchElementException:
    print('There are {} tasks in Completed'.format(element))
#============================================================================#
TitleSprint = str(Sprint)
TitleDate = time.strftime('%m-%d-%y Hr-%H',time.localtime())

with open('../Latex/Sprint {} GTPS Task Report {}.tex'.format(TitleSprint,TitleDate),'w') as file:
    
    file.write('\\input{./Sections/Top}\n')
    
    file.write('''\\begin{{document}}\n
\\begin{{center}}\n
\\Large\n
\\textsc{{GTPS Task Report for Sprint {}}}\\\n
\\normalsize \\DTMnow\n
\\end{{center}}\\vspace{{1.5cm}}\n'''.format(Sprint))



#     file.write('''\\large\n
# \\textsc{{Top Priority Tasks}}\n
# \\normalsize\n''')
#     if len(S.PriorityTasks) == 0:
#         file.write('\\textit{No top priority tasks to display.}\\vspace{.5cm}\n')
#     else:
#         file.write('\\begin{enumerate}[leftmargin=!,labelindent=5pt,itemindent=-35pt]\n')
        
#         for Task in S.PriorityTasks:
#             Task = list(Task)
#             for i in range(0,len(Task)):
#                 if Task[i] == '&':
#                     Task[i] = '\&'
#                 else:
#                     pass
#             Task = ''.join(Task)
#             file.write(Task)
    
    
#         file.write('\\end{enumerate}\\vspace{.5cm}\n')




    file.write('''\\large\n
\\textsc{{Tasks Created in the Last {}hrs}}\n
\\normalsize\n'''.format(str(S.DaysSinceLastReport*24)))
    if len(S.NewTasks) == 0:
        file.write('\\textit{No new tasks to display.}\\vspace{.5cm}\n')
    else:
        file.write('\\begin{enumerate}[leftmargin=!,labelindent=5pt,itemindent=-35pt]\n')
        
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

    if len(S.PreviousTasks) == 0:
        file.write('\\textit{No previous tasks to display.}\\vspace{.5cm}\n')
    else:
        file.write('\\begin{enumerate}[leftmargin=!,labelindent=5pt,itemindent=-35pt]\n')
        
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
test
Need to comment it out.

In the end, I will need some method of storing old tasks so that the task 
report has older tasks on it. Possibly just use a .txt file to store the
old strings and just append them at the end of the tex file.   - Or maybe, I 
dont...? I mean no one is looking at the old tasks so who gives.  

See about selenium waiting for a refreshed page

Arrange Tasks by date in their respective sections

Figure out how we want to do priorities

Wrap up in pretty bow so others can use.
    To do this: creaete setup.py file
                Maybe use py2exe to make an exe file
                
Should use something like this for handling tasks in order to sort them by
date created. From here: https://www.programiz.com/python-programming/methods/list/sort               
# sorting using custom key
employees = [
    {'Name': 'Alan Turing', 'age': 25, 'salary': 10000},
    {'Name': 'Sharon Lin', 'age': 30, 'salary': 8000},
    {'Name': 'John Hopkins', 'age': 18, 'salary': 1000},
    {'Name': 'Mikhail Tal', 'age': 40, 'salary': 15000},
]

# custom functions to get employee info
def get_name(employee):
    return employee.get('Name')


def get_age(employee):
    return employee.get('age')


def get_salary(employee):
    return employee.get('salary')


# sort by name (Ascending order)
employees.sort(key=get_name)
print(employees, end='\n\n')

# sort by Age (Ascending order)
employees.sort(key=get_age)
print(employees, end='\n\n')

# sort by salary (Descending order)
employees.sort(key=get_salary, reverse=True)
print(employees, end='\n\n')    




Something like... this:

Tasks = []
Tasks.append({'TaskTime':S.TaskTimeSec,'TaskNumber':S.TaskNumber.text, 
              'Person':S.Person, 'Description':S.TaskDescription.text})
            
                
                
"""

S.driver.close()

subprocess.Popen(['rubber', '-d', 'Sprint {} GTPS Task Report {}.tex'.format(TitleSprint,TitleDate)],  cwd="../Latex")
time.sleep(2)
subprocess.Popen(['rubber', '--clean', 'Sprint {} GTPS Task Report {}.tex'.format(TitleSprint,TitleDate)],  cwd="../Latex")
time.sleep(2)
print('Opening document')
subprocess.Popen(['okular', 'Sprint {} GTPS Task Report {}.pdf'.format(TitleSprint,TitleDate)],  cwd="../Latex")
