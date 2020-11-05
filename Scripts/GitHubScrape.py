#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 18:10:31 2020

@author: ***REMOVED***

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
    'user_session': 'VtbtJtqiKeciY730a85xk7No3UnfXClGqzw9yuX8LMeJX-Cl',
    '__Host-user_session_same_site': 'VtbtJtqiKeciY730a85xk7No3UnfXClGqzw9yuX8LMeJX-Cl',
    'dotcom_user': '***REMOVED***',
    'has_recent_activity': '1',
    '_gat': '1',
    'tz': 'America%2FChicago',
    '_gh_sess': 'VmP0noDHBMv8SOgs6utZKKiQChYxIoHz4Vzr3xBftOevXQkYyOyYlyIGkvotCPKJB8ECOnF6%2Bj6L0elbokSx7TOq6hAR0wZwAiJADxfZzermatF53X1jOhXPSCFdELthYAUxX8EspdQEjD97PBjASBVlVt3TXJXWv0JGvirx5%2BVWQXvhmYlIMmdzj5CxtfkDZC%2F3QcIbMiRiTIprGAhM%2BgeCDZ%2BXVnI1QfvMaP8OzQL0V2BC9GoVNycD%2BeIcTeNxAtqoW%2F7%2Bk7PZf7hs1G4BLbz%2BFydyRLaVyJ8A00QbvBCc6ITN%2FCgMJSScoD21xILw7WIJynHUAiGrA0%2FQ4I4Do6v2QI6mYtjTMKz3r1mLj8uFMrWHOATnwr9oRkwASPp1qHujcOcUaKTqD1LFTSiqqbUOnr18oIVj55PR1WJGCFs%2B1JScLJm2XAqlXHc6AvRdR2RTEWK8ojmMAWi0ujy33Zes213cGsCS%2FFAv7S2F4bqUNKSiaVYc%2FF%2FvsrgvhNBg2oKCwFTxvCn3AARaS0AxUJkbgYKjAWzy9EKQWwn%2ByVZwqbzfCJfrV%2FbfgzEUbhvmfmgL70IFOqRpCutO7QrM1E4UHlik7Wna9SfGFoqeQal%2BrcSpOd78u9esI6KARPkkVrnNuO1CEE2EiQSxeVHgPj%2BpTOSBaBHFLCmbWQ0ehF4A0D9miS1btULsmQTpMR%2BozaHBtCH%2BLIDpHAQDB1yQJ6Z8Mpd5aC5SUMQu7IKv5VywD0OpTDmt6lBzb8Q5fl5h7g5F%2BIIFAzz%2BcgCGiMRFzpbndv%2B1UZ%2BuqdlNT4b8Mi3k9MhIMnl%2BlmQBQNXjoHsdxixPiw%3D%3D--ebEs3BzXgXrwVBUd--PwMd%2BybIteOA6JRcOyFH%2FA%3D%3D',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://github.com/new',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'If-None-Match': 'W/"404e7e0e42ecfe926bed70da5c92cf4c"',
    'Cache-Control': 'max-age=0',
}

response = requests.get('https://github.com/***REMOVED***/Scrape', headers=headers, cookies=cookies)


soup = BeautifulSoup(response.content, 'html.parser')
results = soup.find('div', class_='plain')
print(results.text)