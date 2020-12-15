#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 19:06:22 2020

@author: ***REMOVED***
This is an attempt to scrape info from tfs to automate the task report.
"""
#============================================================================#
import time
import subprocess
import Scraper       
#============================================================================#
Username = '***REMOVED***'
Password = 'uCfE2ahPM8C89CZ'
Sprint=20

# Sprint = input('Please input the Sprint number\n >')
# Username = input('Please input your username\n >')
# Password = input('Please input your password\n >')
URL = '''http://conw-mstf-01-pv.snaponglobal.com:8080/tfs/Embedded%20
Engineering%20Collection/Agile%20Sanctuary/_backlogs/TaskBoard/2020/
Sprint%20{}?_a=requirements'''.format(Sprint)
TitleSprint = str(Sprint)
TitleDate = time.strftime('%m-%d-%y Hr-%H',time.localtime())
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

S.TaskExtractor('To Do')        
#============================================================================#
WorkInProgress = S.driver.find_element_by_xpath('//*[@id="tfs_tnli16"]')
WorkInProgress.click()

S.Handler()

S.TaskExtractor('To Do')        
#============================================================================#
WorkInTest = S.driver.find_element_by_xpath('//*[@id="tfs_tnli17"]')
WorkInTest.click()

S.Handler()

S.TaskExtractor('Test')        
#============================================================================#
WorkInCompleted = S.driver.find_element_by_xpath('//*[@id="tfs_tnli9"]')
WorkInCompleted.click()

S.Handler()

S.TaskExtractor('Completed')
#============================================================================#
S.StringMaker()

with open('../GeneratedReports/Sprint {} GTPS Task Report {}.tex'.format(TitleSprint,TitleDate),'w') as file:
    
    file.write('\\input{../Latex/Sections/Top}\n')
    
    file.write('''\\begin{{document}}\n
\\begin{{center}}\n
\\Large\n
\\textsc{{GTPS Task Report for Sprint {}}}\\\n
\\normalsize \\DTMnow\n
\\end{{center}}\\vspace{{1.5cm}}\n'''.format(Sprint))



    file.write('''\\large\n
\\textsc{{Top Priority Tasks}}\n
\\normalsize\n''')
    if len(S.PriorityTasks) == 0:
        file.write('\\textit{No top priority tasks to display.}\\vspace{.5cm}\n')
    else:
        file.write('\\begin{enumerate}[leftmargin=!,labelindent=5pt,itemindent=-35pt]\n')
        
        for Task in S.PriorityTasks:
            Task = Task['String']
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
\\textsc{{Tasks Created in the Last {}hrs}}\n
\\normalsize\n'''.format(str(S.DaysSinceLastReport*24)))
    if len(S.NewTasks) == 0:
        file.write('\\textit{No new tasks to display.}\\vspace{.5cm}\n')
    else:
        file.write('\\begin{enumerate}[leftmargin=!,labelindent=5pt,itemindent=-35pt]\n')
        
        for l in range(0,len(S.NewTasks)):
            Task = list(S.NewTasks[l])
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
Need to comment it out.

In the end, I will need some method of storing old tasks so that the task 
report has older tasks on it. Possibly just use a .txt file to store the
old strings and just append them at the end of the tex file.   - Or maybe, I 
dont...? I mean no one is looking at the old tasks so who gives.  


Wrap up in pretty bow so others can use.
    To do this: creaete setup.py file
                Maybe use py2exe to make an exe file
"""

S.driver.close()

subprocess.Popen(['rubber', '-d', 'Sprint {} GTPS Task Report {}.tex'.format(TitleSprint,TitleDate)],  cwd="../GeneratedReports")
time.sleep(5)
subprocess.Popen(['rubber', '--clean', 'Sprint {} GTPS Task Report {}.tex'.format(TitleSprint,TitleDate)],  cwd="../GeneratedReports")
time.sleep(5)
print('Opening document')
subprocess.Popen(['okular', 'Sprint {} GTPS Task Report {}.pdf'.format(TitleSprint,TitleDate)],  cwd="../GeneratedReports")