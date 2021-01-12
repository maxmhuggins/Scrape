#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 19:06:22 2020

@author: ***REMOVED***

This is an automated task report generator. It uses selenium to access TFS
and collect data from there. It compiles it into a LaTeX document for which
rubber is used to compile it into a pdf to be sent out. This is for the SQA 
intern team.
"""
#============================================================================#
import time
import subprocess
import Scraper       
#============================================================================#
"""Either input name here, or uncomment the input commands and do it on 
startup. The latter is more secure."""

Username = '***REMOVED***'
Password = '***REMOVED***'
Sprint=1

# Sprint = input('Please input the Sprint number\n >')
# Username = input('Please input your username\n >')
# Password = input('Please input your password\n >')
#============================================================================#
"""This URL leads to TFS, on its own it is useless for scraping, but it is
passed to the Scraper class which uses a method to format it so selenium can
authenticate on the website."""

URL = '''http://conw-mstf-01-pv.snaponglobal.com:8080/tfs/Embedded%20
Engineering%20Collection/Agile%20Sanctuary/_backlogs/TaskBoard/2020/
requirements'''
TitleSprint = str(Sprint)
TitleDate = time.strftime('%m-%d-%y Hr-%H',time.localtime())
#============================================================================#
"""Instantiate a Scraper object with the given URL, pass, user."""
S = Scraper.Scrape(Username, Password, URL)    
URL = S.ModifiedURL
#============================================================================#
"""The driver gets the URL"""
S.driver.get(URL)
QueriesButton = """/html/body/div[2]/div/div[1]/table[2]/tbody/tr/td/div[1]/
div/table/tbody/tr/td[1]/div[2]/div/ul/li[2]/a"""
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

with open('../GeneratedReports/Sprint {} GTPS Task Report {}.tex'.format(
        TitleSprint,TitleDate),'w') as file:
    
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
\\end{{center}}\\vspace{{1.5cm}}\n'''.format(Sprint))



    file.write('''\\large\n
\\textsc{{Top Priority Tasks}}\n
\\normalsize\n''')


    if len(S.PriorityTasks) == 0:
        file.write('\\textit{No top priority tasks to display.}\\vspace{.5cm}\n')
    else:
        file.write(
            '\\begin{enumerate}[leftmargin=!,labelindent=5pt,itemindent=-35pt]\n')
        
        for Task in S.PriorityTasks:
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
            file.write(Task + '\n')
    
    
        file.write('\\end{enumerate}\\vspace{.5cm}\n')


    file.write('''\\large\n
\\textsc{{Tasks Created in the Last {}hrs}}\n
\\normalsize\n'''.format(str(S.DaysSinceLastReport*24)))
    if len(S.NewTasks) == 0:
        file.write('\\textit{No new tasks to display.}\\vspace{.5cm}\n')
    else:
        file.write(
            '\\begin{enumerate}[leftmargin=!,labelindent=5pt,itemindent=-35pt]\n')
        
        for l in range(0,len(S.NewTasks)):
            Task = list(S.NewTasks[l])
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
            
            file.write(Task + '\n')
    
    
        file.write('\\end{enumerate}\\vspace{.5cm}\n')

    file.write('''\\large\n
\\textsc{{Previous Tasks}}\n
\\normalsize\n''')

    if len(S.PreviousTasks) == 0:
        file.write('\\textit{No previous tasks to display.}\\vspace{.5cm}\n')
    else:
        file.write(
            '\\begin{enumerate}[leftmargin=!,labelindent=5pt,itemindent=-35pt]\n')
        
        for Task in S.PreviousTasks:
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
            file.write(Task + '\n')
    
    
        file.write('\\end{enumerate}\\vspace{.5cm}\n')
                


    file.write('\\end{document}')
#============================================================================#


"""
Need to comment it out.

In the end, I will need some method of storing old tasks so that the task 
report has older tasks on it. Possibly just use a .txt file to store the
old strings and just append them at the end of the tex file.   - Or maybe, I 
dont...? I mean no one is looking at the old tasks so who gives.  

If top priority task is in done category then it shouldn't be a priority task

Wrap up in pretty bow so others can use.
    To do this: creaete setup.py file
                Maybe use py2exe to make an exe file
                
It would be really snazzy if it saw that a tester's name is assigned to a to-do
or in progress task that it would move that task to test.
"""

S.driver.close()

subprocess.Popen(['rubber', '-d', 'Sprint {} GTPS Task Report {}.tex'.format(
    TitleSprint,TitleDate)],  cwd="../GeneratedReports")
time.sleep(5)
subprocess.Popen(['rubber', '--clean', 'Sprint {} GTPS Task Report {}.tex'.format(
    TitleSprint,TitleDate)],  cwd="../GeneratedReports")
time.sleep(5)
print('Opening document')
subprocess.Popen(['okular', 'Sprint {} GTPS Task Report {}.pdf'.format(
    TitleSprint,TitleDate)],  cwd="../GeneratedReports")