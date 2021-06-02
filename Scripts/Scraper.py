#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 10:42:39 2020

@author: maxmhuggins
"""
# ========================================================================== #
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException)
import operator
# ========================================================================== #
"""
This is the names dictionary. It holds all of the TFS names and assigns them
nicknames to be displayed on the report.
"""
Names = {
    "David Palos": "PALOS", "Babb, David A": "BABB", "Huggins, Max": "MAX",
    "Patton, Matthew": "MATTHEW", "Sharma, Kuldeep": "KULDEEP",
    "Brown, Adam C.": "ADAM", "Pulapa, Rajani K.": "RAJANI",
    "Bansal, Aman": "AMAN", "Khurana, Simran": "SIMRAN",
    "Pandey, Sampurnanand": "SAM", "Singh, Upasana": "UPASANA",
    "Sellers, Eric R": "ERIC", "Sperry, Jonathan A": "JONATHAN",
    "LeCrone, Sean": "SEAN", "Robinson, Chance W": "CHANCE",
    "D'Agostino, Robert J": "BOB", "Verma, Anju": "ANJU",
    "Heaver, Annika": "ANNIKA", "Robbins, Lance": "LANCE",
    "Saxena, Kritika": "KRITIKA", "Gill, George M.": "MIKE",
    "Boehringer, Derreck B": "BO",
    "": "Unassigned"
    }

AlignerModels = {'All': 'Specs Testing', 'Tru-Point': 'GTPS',
                 'EZ-ADAS': 'EZ-ADAS', 'V1200': 'V-Series',
                 'V2000': 'V-Series', 'V2100': 'V-Series',
                 'V2280': 'V-Series', 'V2380': 'V-Series',
                 'V3300': 'V-Series', 'Pro32': 'Pro-Series',
                 'Pro42': 'Pro-Series', 'Dragon': 'Dragon',
                 'OEM': 'OEM', 'Truck': 'Truck'
                 }
# ========================================================================== #


class Scrape:

    """
    The Scrape class handles most of the scraping from TFS. It also includes
    some attributes for the report and handles task dictionaries.
    """

    def __init__(self, Username, Password, Sprint, URL, SoftwareVersion,
                 ReportType):
        """Either input name here, or uncomment the input commands and do it
        on startup. The latter is more secure."""
        self.Username = Username
        self.Password = Password
        self.Sprint = Sprint
        self.SoftwareVersion = SoftwareVersion
        self.URL = URL
        self.ReportType = ReportType
        self.TitleSprint = str(self.Sprint)
        self.TitleDate = time.strftime('%m-%d-%y Hr-%H', time.localtime())
        self.DocumentTitle = 'Sprint {} {} Task Report {}.tex'.format(
                self.TitleSprint, AlignerModels[self.ReportType],
                self.TitleDate)
        self.ModifiedURL = self.MakeURL(self.URL)
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(options=self.options)
        self.DaysSinceLastReport = 1
        self.SecondsSinceLastReport = self.DaysSinceLastReport * 60 * 60 * 24
        self.TodaySec = time.time()
        self.Delay = 0
        self.Columns = ['Created Date', 'Backlog Priority', 'Tags',
                        'Aligner Model']
        self.Tasks = []
        self.NewTasks = []
        self.PreviousTasks = []
        self.PriorityTasks = []

    def MakeURL(self, URL):
        """The MakeURL method will make an authentication URL so you can get
        into TFS without having to manually log in."""

        NoHTTPURL = ''
        for i in range(0, len(URL)):
            if i > 6:
                NoHTTPURL += URL[i]
            else:
                pass

        ModifiedURL = 'http://' + '{}:{}@'.format(self.Username,
                                                  self.Password) + NoHTTPURL
        return ModifiedURL

    def Clicker(self, xpath):
        """The Clicker method literally clicks on an xpath element. There
        is a try, except in place for unloaded elements."""

        time.sleep(self.Delay)
        result = None
        tried = 0
        while result is None:
            tried += 1
            try:
                Element = self.driver.find_element_by_xpath(xpath)
                Element.click()
                result = Element
            except (NoSuchElementException, StaleElementReferenceException):
                pass

            if tried >= 100:
                print("Couldn't find {}".format(xpath))
                break

    def Appender(self, Tasks, hl):
        """The Appender method will make a dictionary for each task that
        includes priority and the string that will get put into the latex
        document."""

        T = Tasks['Priority']
        if T != ' ':

            if Tasks['Type'] == 'Completed':
                if Tasks['Time'] + self.SecondsSinceLastReport > self.TodaySec:
                    self.NewTasks.append(
                            {
                                'String': '\\item \\hl{}{{{}}} {}: {}'.format(
                                    hl,
                                    Tasks['Number'],
                                    Tasks['Person'],
                                    Tasks['Description']),
                                'Priority': Tasks['Priority'],
                                'Aligner Model': Tasks['Aligner Model']
                                }
                            )

                else:
                    self.PreviousTasks.append(
                            {
                                'String': '\\item \\hl{}{{{}}} {}: {}'.format(
                                    hl,
                                    Tasks['Number'],
                                    Tasks['Person'],
                                    Tasks['Description']),
                                'Priority': None,
                                'Aligner Model': Tasks['Aligner Model']
                                }
                            )

            else:
                self.PriorityTasks.append(
                    {
                        'String': '\\item \\hl{}{{{}}} {}: {}'.format(
                            hl,
                            Tasks['Number'],
                            Tasks['Person'],
                            Tasks['Description']),
                        'Priority': Tasks['Priority'],
                        'Aligner Model': Tasks['Aligner Model']
                        }
                    )

        elif Tasks['Time'] + self.SecondsSinceLastReport > self.TodaySec:
            self.NewTasks.append(
                    {
                        'String': '\\item \\hl{}{{{}}} {}: {}'.format(
                            hl,
                            Tasks['Number'],
                            Tasks['Person'],
                            Tasks['Description']),
                        'Priority': Tasks['Priority'],
                        'Aligner Model': Tasks['Aligner Model']
                        }
                    )

        else:
            self.PreviousTasks.append(
                    {
                        'String': '\\item \\hl{}{{{}}} {}: {}'.format(
                            hl,
                            Tasks['Number'],
                            Tasks['Person'],
                            Tasks['Description']),
                        'Priority': None,
                        'Aligner Model': Tasks['Aligner Model']
                        }
                    )

    def Handler(self):
        """The Handler method makes a unique query that includes the date the
        task was created as well as the backlog priority."""

        ArrowButton = """/html/body/div[4]/div[2]/div/div[4]/div[1]/div[1]/
        div[3]/div[1]/button/span/span"""

        ColumnOptions = '//*[@id="mi_71_column-options"]'
        self.Clicker(ColumnOptions)

        time.sleep(self.Delay+.5)

        counter = 0
        ListOfOptions = self.driver.find_element_by_xpath(
            '/html/body/div[4]/div[2]/div/div[4]/div[1]/div[1]/div[2]/select')

        for option in ListOfOptions.find_elements_by_tag_name('option'):

            if option.text in self.Columns:
                option.click()
                time.sleep(self.Delay + .3)
                self.Clicker(ArrowButton)
                time.sleep(self.Delay)
                counter += 1

                if counter == len(self.Columns):
                    break

        OK = '//button[@id="ok"]'
        self.Clicker(OK)

        CreatedDateColumn = '//*[@id="vss_11"]/div[1]/div[1]/div[9]'
        self.Clicker(CreatedDateColumn)
        self.Clicker(CreatedDateColumn)
        time.sleep(1)

    def TaskExtractor(self, Section):
        """The TaskExtractor method grabs all of the relevant data from TFS
        regarding the task, stores it in a dictionary and appends it to a
        list."""

        elements = range(0, 1000)

        try:

            for element in elements:

                CurrentTask = '//*[@id="vss_11"]/div[2]'

                ScrollDown = self.driver.find_element_by_xpath(CurrentTask)
                ScrollDown.send_keys(Keys.ARROW_DOWN)

                AlignerModel = self.driver.find_element_by_xpath(
                    '//*[@id="row_vss_11_{}"]/div[7]'.format(element))

                Tag = self.driver.find_element_by_xpath(
                    '//*[@id="row_vss_11_{}"]/div[10]'.format(element))

                TaskNumber = self.driver.find_element_by_xpath(
                    '//*[@id="row_vss_11_{}"]/div[1]'.format(element))

                TaskDescription = self.driver.find_element_by_xpath(
                    '//*[@id="row_vss_11_{}"]/div[3]'.format(element))

                TaskPerson = self.driver.find_element_by_xpath(
                    '//*[@id="row_vss_11_{}"]/div[4]'.format(element))

                TaskTime = self.driver.find_element_by_xpath(
                    '//*[@id="row_vss_11_{}"]/div[9]'.format(element))

                Priority = self.driver.find_element_by_xpath(
                    '//*[@id="row_vss_11_{}"]/div[8]'.format(element))

                self.AlignerModel = AlignerModel.text
                self.Tag = Tag.text
                self.TaskPriority = Priority.text
                try:
                    self.Person = Names[TaskPerson.text]
                except KeyError:
                    self.Person = TaskPerson.text
                    print('Please add: ' +
                          '{} to the Names dictionary.'.format(self.Person))
                self.TaskTime = time.strptime(TaskTime.text,
                                              "%m/%d/%Y %I:%M %p")
                self.TaskTimeSec = time.mktime(self.TaskTime)
                self.TaskDescription = TaskDescription
                self.TaskNumber = TaskNumber

                if self.AlignerModel == self.ReportType and (
                        self.Tag == self.SoftwareVersion or self.Tag == ' '):

                    Task = {
                        'Time': self.TaskTimeSec, 'Type': Section,
                        'Priority': self.TaskPriority,
                        'Number': self.TaskNumber.text, 'Person': self.Person,
                        'Description':  self.TaskDescription.text,
                        'Aligner Model': self.AlignerModel, 'Tag': self.Tag
                        }

                    self.Tasks.append(Task)

                else:
                    pass

        except NoSuchElementException:
            pass

    def StringMaker(self):
        """The StringMaker method will sort the list of dictionaries by date,
        assign colors to the highlighter, then send the task to the Appender"""
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

        self.PriorityTasks.sort(key=operator.itemgetter('Priority'),
                                reverse=False)

    def StringFixer(self, Task):
        '''The StringFixer method can be used to correct strings with special
        characters in them, characters like & or forward slash '''
        Task = Task['String']
        Task = list(Task)
        for i in range(0, len(Task)):
            if Task[i] == '&':
                Task[i] = '\\&'
            if Task[i] == '$':
                Task[i] = '\\$'
            if Task[i] == '#':
                Task[i] = '\\#'
            if Task[i] == '_':
                Task[i] = '\\_'
            else:
                pass
        Task = ''.join(Task)
        return Task

    def SectionMaker(self, file, CurrentCategory):
        '''The SectionMaker method is used to make the sections of the report.
        It also handles if there are no tasks in a given categeory.'''
        if len(CurrentCategory) == 0:
            file.write(
                '\\textit{No top priority tasks to display.}\\vspace{.5cm}\n')
        else:
            file.write(
                '\\begin{enumerate}[leftmargin=!,labelindent=5pt,itemindent=-35pt]\n')

            for Task in CurrentCategory:
                file.write(self.StringFixer(Task) + '\n')

            file.write('\\end{enumerate}\\vspace{.5cm}\n')

    def ReportGenerator(self):
        '''The ReportGenerator method will make a LaTeX document from the
        information gathered throughout the program.'''

        with open('../GeneratedReports/' + self.DocumentTitle, 'w') as file:

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
        \\textsc{{{} Task Report for Sprint {} v{}}}\\\n
        \\normalsize \\DTMnow\n
        \\end{{center}}\\vspace{{1.5cm}}\n'''.format(AlignerModels[self.ReportType], self.Sprint, self.SoftwareVersion))

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
