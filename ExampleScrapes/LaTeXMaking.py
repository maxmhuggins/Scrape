#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 08:19:05 2020

@author: maxmhuggins

This is a script to get started using LaTeX with python to eventually create
the task report from scraped data.
"""

import subprocess, os
import time

strings = []
N = 10

for i in range(0,N):
    package = ['NUMBER{}'.format(i), 'NAME{}'.format(i), 'DESCRIPTION{}'.format(i)]
    strings.append(package)
        
with open('../Latex/main.tex','w') as file:
    
    file.write('\\input{./Sections/Top}\n')
    
    file.write('''\\large
                \\textsc{{Top Priority}}
                \\normalsize''')
                
    file.write('\\begin{enumerate}')
    for string in strings:
        file.write('\\item \\hlcyan{{{}}} {}: {}'.format(string[0], string[1], string[2]))
    file.write('\\end{enumerate}\\vspace{.5cm}')
    
    
    file.write('''\\large
                \\textsc{{New Tasks}}
                \\normalsize''')

    file.write('\\begin{enumerate}')
    for string in strings:
        file.write('\\item \\hlyellow{{{}}} {}: {}'.format(string[0], string[1], string[2]))
    file.write('\\end{enumerate}\\clearpage')


    file.write('''\\large
                \\textsc{{Previous Tasks}}
                \\normalsize''')

    file.write('\\begin{enumerate}')
    for string in strings:
        file.write('\\item \\hlgreen{{{}}} {}: {}'.format(string[0], string[1], string[2]))
    file.write('\\end{enumerate}\\vspace{.5cm}')
    
    file.write('\\end{document}')
    file.close()

subprocess.Popen(['rubber', '-d', 'main.tex'],  cwd="../Latex")
time.sleep(2)
subprocess.Popen(['rubber', '--clean', 'main.tex'],  cwd="../Latex")
time.sleep(3)
print('Opening document')
subprocess.Popen(['okular', 'main.pdf'],  cwd="../Latex")
