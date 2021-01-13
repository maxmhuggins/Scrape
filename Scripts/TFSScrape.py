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
Username = '***REMOVED***'
Password = '***REMOVED***'
Sprint = 1     
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
#============================================================================#
"""Instantiate a Scraper object with the given URL, pass, user."""
S = Scraper.Scrape(Username, Password, Sprint, URL)    
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
S.ReportGenerator()
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

If I get close to end of the document then clear page

Associate task with the PBI in the report?
"""

S.driver.close()

subprocess.Popen(['rubber', '-d', 'Sprint {} GTPS Task Report {}.tex'.format(
    S.TitleSprint,S.TitleDate)],  cwd="../GeneratedReports")
time.sleep(5)
subprocess.Popen(['rubber', '--clean', 'Sprint {} GTPS Task Report {}.tex'.format(
    S.TitleSprint,S.TitleDate)],  cwd="../GeneratedReports")
time.sleep(5)
print('Opening document')
subprocess.Popen(['okular', 'Sprint {} GTPS Task Report {}.pdf'.format(
    S.TitleSprint,S.TitleDate)],  cwd="../GeneratedReports")