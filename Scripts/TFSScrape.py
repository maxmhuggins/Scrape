#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 19:06:22 2020

@author: maxmhuggins

This is an automated task report generator. It uses selenium to access TFS
and collect data from there. It compiles it into a LaTeX document for which
rubber is used to compile it into a pdf to be sent out. Made for the SQA
intern team to make their lives easier.
"""
# ========================================================================== #
import time
import subprocess
import Scraper
import supporters.passwords as passwords
# ========================================================================== #
Username = passwords.username
Password = passwords.password
Sprint = 11
SoftwareVersion = '1.3.0'
ReportType = 'Tru-Point'

# Sprint = input('Please input the Sprint number\n >')
# Username = input('Please input your username\n >')
# Password = input('Please input your password\n >')
# SoftwareVersion = input('Please input the software version being released ' +
#                         'next\n >')
# ReportType = input('Please input the report type (f.e. Tru-Point)\n >')
# ========================================================================== #
"""This URL leads to TFS, on its own it is useless for scraping, but it is
passed to the Scraper class which uses a method to format it so selenium can
authenticate on the website."""

URL = '''http://conw-mstf-01-pv.snaponglobal.com:8080/tfs/Embedded%20
Engineering%20Collection/Agile%20Sanctuary/_backlogs/TaskBoard/2020/
requirements'''
# ========================================================================== #
"""Instantiate a Scraper object with the given URL, pass, user."""
S = Scraper.Scrape(Username, Password, Sprint, URL, SoftwareVersion,
                   ReportType)
URL = S.ModifiedURL
# ========================================================================== #
"""The driver gets the URL"""
S.driver.get(URL)
QueriesButton = """/html/body/div[2]/div/div[1]/table[2]/tbody/tr/td/div[1]/
div/table/tbody/tr/td[1]/div[2]/div/ul/li[2]/a"""
S.Clicker(QueriesButton)
# ========================================================================== #
WorkInToDo = '//*[@id="tfs_tnli18"]'
S.Clicker(WorkInToDo)

S.Handler()

S.TaskExtractor('To Do')
# ========================================================================== #
WorkInProgress = S.driver.find_element_by_xpath('//*[@id="tfs_tnli16"]')
WorkInProgress.click()

S.Handler()

S.TaskExtractor('To Do')
# ========================================================================== #
WorkInTest = S.driver.find_element_by_xpath('//*[@id="tfs_tnli17"]')
WorkInTest.click()

S.Handler()

S.TaskExtractor('Test')
# ========================================================================== #
WorkInCompleted = S.driver.find_element_by_xpath('//*[@id="tfs_tnli9"]')
WorkInCompleted.click()

S.Handler()

S.TaskExtractor('Completed')
# ========================================================================== #
S.StringMaker()
S.ReportGenerator()
# ========================================================================== #

S.driver.close()

print('Compiling document using Rubber')
subprocess.Popen(['rubber', '-d', S.DocumentTitle],
                 cwd="../GeneratedReports/")

time.sleep(5)
print('Cleaning directory using Rubber')
subprocess.Popen(['rubber', '--clean', S.DocumentTitle],
                 cwd="../GeneratedReports/")

time.sleep(5)
print('Opening document with Okular')
subprocess.Popen(['okular', 'Sprint {} {} Task Report {}.pdf'.format(
                S.TitleSprint, Scraper.AlignerModels[S.ReportType],
                S.TitleDate)],  cwd="../GeneratedReports/")
