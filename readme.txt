This repository houses the code for an automated task report generator for the software quality assurance team at Snap-on.

The project uses selenium to scrape relevant project information from Team Foundation Server, and then compiles the information into a PDF document using LaTeX

You will need to install dependencies and make yourself a password file. Name it passwords.py and have something in it like:
username = 'pa6519'
password = 'supersecretpassword'
this should be saved in the supporters directory
