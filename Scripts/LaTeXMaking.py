#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 08:19:05 2020

@author: ***REMOVED***

This is a script to get started using LaTeX with python to eventually create
the task report from scraped data.
"""

import subprocess, os
import time

with open('../Latex/main.tex','w') as file:
    file.write('\\input{./Sections/Top}\n')
    file.write('This should work with no errors at all!\n')
    file.write('\\end{document}\n')

subprocess.Popen(['rubber', '-d', 'main.tex'],  cwd="../Latex")
time.sleep(2)
subprocess.Popen(['rubber', '--clean', 'main.tex'],  cwd="../Latex")
time.sleep(2)
subprocess.Popen(['okular', 'main.pdf'],  cwd="../Latex")
