#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 08:19:05 2020

@author: ***REMOVED***

This is a script to get started using LaTeX with python to eventually create
the task report from scraped data.
"""

import subprocess, os

with open('../Latex/main.tex','w') as file:
    file.write('\\input{../Latex/Sections/Packages}\n')
    file.write('\\begin{document}\n')
    file.write('Hello World!\n')
    file.write('\\end{document}\n')
    
os.system('rubber -d ../Latex/main.tex')
os.system('rubber --clean ../Latex/main.pdf')
os.system('okular ../Latex/main.pdf')

"""
Need to fix os.system running in the script directory rather than the working 
directory!
"""