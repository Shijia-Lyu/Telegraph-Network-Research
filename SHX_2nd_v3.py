# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 00:44:41 2024

@author: 11786
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 21:57:39 2024

@author: 11786
"""

# Import packages
import os
import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
from selenium.webdriver.chrome.options import Options
import re
import random

# Web driver
options = Options()

# Change User-Agent
user_agents =  [ "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"]
user_agent = random.choice(user_agents)
options.add_argument(f'user-agent={user_agent}')

# Set directory
os.chdir(r"C:\Users\11786\sxh")
os.getcwd()
#os.remove("SHX_2ndlayer0.csv")
csvname = ["URL","Title", "Sender",'Receiver','Subject','Time','Year','Edition','Quantity','Size','Archive Number']
with open("SHX_2ndlayer0.csv", "a+", newline = '', encoding = 'GB18030') as data_file:
    output = csv.writer(data_file)
    output.writerow([s for s in csvname])

# read CSV
csv_file = 'SHX_1st _v2.csv'
df = pd.read_csv(csv_file, encoding='gb18030')
href_column = 'HREF'  
j = df[href_column]

# find all the HREF in the CSV    
for j in df[href_column]:
    url = "http://data.library.sh.cn/sd/resource/work/"+ j +"&dataType=2"
    s = Service(r'C:\Users\11786\sxh\chromedriver130.exe')
    driver = webdriver.Chrome(service=s)
    #driver.set_window_size(1920, 1080)
    driver.get(url)
    time.sleep(random.uniform(5, 7))
    
    soup = BeautifulSoup(driver.page_source, features="lxml")
        
    li = soup.find_all('li', {'style':"line-height: 30px;"})
    p = li[0].find_all("p")

    result = {}

        #Crawling title, sender
    result["URL"] = url
    result["Title"] = p[0].get_text().strip().split("\xa0")[-1]
    result["Sender"] = p[1].find('a').get_text().strip()
           
        #Crawling for receiver:
    my_liist = []
    for i in range (0,len(p)):
        pi = "".join(p[i].get_text().strip().split("\xa0"))
        my_liist.append(pi)

    receiver_lines = []
    for line in my_liist:
        if '【收件人】' in line:
            receiver_lines.append(line.strip().split("】")[-1].strip())
        else:
            pass
    result['Receiver'] = receiver_lines[0] if receiver_lines else ''

    quantity_lines = []    
    for line in my_liist:
        if '【数量】' in line:
            quantity_lines.append(line.split("】")[-1])
        else:
            pass
    result['Quantity'] = quantity_lines[0] if quantity_lines else ''

    subject_lines = []    
    for line in my_liist:
        if '【主题】' in line:
            su =  re.sub(r'\s+', ' ', line.strip().split("】")[-1])
            subject_lines.append(su)
        else:
            pass
        result['Subject'] = subject_lines[0] if subject_lines else ''

    edition_lines = []    
    for line in my_liist:
        if '【版本类型】' in line:
            edition_lines.append(line.strip().split("】")[-1])
        else:
            pass
    result['Edition'] = edition_lines[0] if edition_lines else ''

    year_lines = []    
    for line in my_liist:
        if '【年号】' in line:
            year_lines.append(line.split("】")[-1])
        else:
            pass
    result['Year'] = year_lines[0] if year_lines else ''  
            
    time_lines = []    
    for line in my_liist:
        if '【时间】' in line:
            time_lines.append(line.split("】")[-1])
        else:
            pass
    result['Time'] = time_lines[0] if time_lines else ''

    size_lines = []    
    for line in my_liist:
        if '【尺寸】' in line:
            size_lines.append(line.split("】")[-1])
        else:
            pass
    result['Size'] = size_lines[0] if size_lines else ''
            
    result["Archive Number"] = p[-2].get_text().strip().split("\xa0")[-1]

# Write to output file
    with open("SHX_2ndlayer0.csv", "a+", newline = '', encoding = 'GB18030') as file:
        output = csv.writer(file)
        output.writerow([result[s] for s in csvname]) 
 
    
driver.quit()  