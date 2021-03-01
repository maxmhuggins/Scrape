#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 18:10:31 2020

@author: maxmhuggins

This is an example of scraping a webpage that requries a login. I've taken the
cookies and headers from web developer tools in my browser and copied the cURL
then used the tool here: https://curl.trillworks.com/ to get the following
code.
"""
from bs4 import BeautifulSoup
import requests

cookies = {
    '_octo': 'GH1.1.465994550.1602105249',
    'logged_in': 'yes',
    '_ga': 'GA1.2.1358488333.1602105251',
    '_device_id': '0509b85cf1c3ff7b00fe8cc6d8e548d6',
    'tz': 'America%2FChicago',
    '_gh_sess': '6rcvH7eC4dJYIcHwdHZ4GR0jVArRRdIWUO1rOpoTq7%2F94FUy43zf6LwiQwtEidsnTVMGu4cKSgZ9h91KS8gqT%2BtGpYsluRYh%2BTDlDIiCO7R7IepHL%2FVhaqab1aRDr8kRK71915XDfbNYr7wAl4qZH8TupZyErzhjdqNWcSeRMrokx1fVPpq7TdjAV2lArrcUTABCdpifFcOMh0SWR7OAMQT4KTPC3aCs2Q2lKLFOV4jI3bSp79ujHXjtAGwXf8oOqN%2Bcy9dT6EOhHLelpgQU4gTv1VRybn6PKndqDZJCIpkZrezTPSQ7k1aiWUAOmvCE2SQ4aJpaCCYblziNO2pqOkehXy%2FnUEFwsgVE6T650sl1HN9ZKcAqSVWmrNZpa5Cm9TB%2FZ%2Fh%2F4CtYMCEyXvWRcjuraZ8YJxtsvM2AFIJOpKKDrsx5%2BLoM0HRwE4RJh9hq9JG8SaQjhK5B8HBUzcqMx648iTtPdV4anksWPDq2Fk7ptQS8W02CJn6d2i6yyabev4OWxtg0MTkTYf%2FtQO9Mk5TEDUzwpSmerW5n6ywFx57uzA%2FA9yDHKz7B0TRAsb3H%2Be5KtVuahnY%2BE0y40Y6LNEJFTB1kX%2BE1PMg%2FQeXTQ%2BbsnNeJtv74XUAcP09GZ9SZ5SnnI%2B4uBk603%2BwynT5SEdhh7byIGJvTFz6CUr2SlWISLg5TuXTpJkxnkRix8lnT%2FKNILfeewFhQS8ulIDvZrRzlwRdsBk5Jhja4obmBXf2AUKFlu2585R6uUawoEmt5mnQeog%3D%3D--ROB7otQ1eE0e09Uw--thHoC3uUVniKEEf2Dwr3Fg%3D%3D',
    'has_recent_activity': '1',
    'user_session': 'CN26SHWJIvUynDqIDWGJBjAEE4Cx5q9Y5lRQint-iZki2TFV',
    '__Host-user_session_same_site': 'CN26SHWJIvUynDqIDWGJBjAEE4Cx5q9Y5lRQint-iZki2TFV',
    'dotcom_user': 'maxmhuggins',
    '_gat': '1',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://github.com/',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

response = requests.get('https://github.com/maxmhuggins/Scrape', headers=headers, cookies=cookies)


soup = BeautifulSoup(response.content, 'html.parser')
results = soup.find('div', class_='plain')
print(results.text)

print('========== Another method... that doesnt seem to be working==========')

from bs4 import BeautifulSoup
import requests

# Start the session
session = requests.Session()

# Create the payload
payload = {'login':'maxmhuggins', 
          'password':'Huggies192*!'
         }

# Post the payload to the site to log in
s = session.post("https://github.com/login", data=payload)
print('login', s.status_code)

# Navigate to the next page and scrape the data
s = session.get('https://github.com/maxmhuggins/Scrape')

soup = BeautifulSoup(s.content, 'html.parser')

results = soup.find('div', class_='plain')
print('scrape', s.status_code)
# print(results.text)
