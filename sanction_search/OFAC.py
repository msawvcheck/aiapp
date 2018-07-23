#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 05:46:14 2018

@author: monishasaw
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 14:29:34 2018

@author: monishasaw
"""


#Automating OFAC Sanction search

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import numpy as np
#from selenium.webdriver.common.keys import Keys
#import pandas as pd
#from bs4 import BeautifulSoup
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.support.wait import WebDriverWait
#import pyautogui
#import time
#import shutil
#import pathlib
#from requests import get
import docx2txt
import us
import os
#import re


def ofac_search1():
    
    path = "/Users/monishasaw/Desktop/accurint"
    f=os.listdir(path)[0]
    if(f == '.DS_Store'):
     file = "/Users/monishasaw/Desktop/accurint/"+ os.listdir(path)[1]
    else:
     file = "/Users/monishasaw/Desktop/accurint/"+ os.listdir(path)[0]

    
    #first_name= 'ADAM'
    #last_name= 'SMITH'
    
    #profile the person
    
    #imoprt accurint doc
    my_text = docx2txt.process(file)
    
    
    
    # profile a person
    
    #creat elist of the paragraphs
    par = my_text.split('\n\n\n')
    
    #keep only those elements having aka, subject information and address summary
    title = ['AKAs','Subject Information','Address Summary']
    
    profile_para = []
    
    for words in title:
      l = [k for k in par if words in k]
      profile_para.extend(l)
      
    profile_para[:] = (value for value in profile_para if value != '')
    
    
    
    #fetching akas
    p=profile_para[0].split("\n")
    arr = np.array(p)
    aka_words = ['AKAs','Names Associated','Age','SSN', 'Utility']
    aka = []
    
    for i in arr:
     if any(word in i for word in aka_words):
        pass
     else:
         l=i.upper()
         aka.append(l)
    
    aka[:] = (value for value in aka if value != '')
    
    
    
    # fetching basic info
    p1=profile_para[1].split("\n")
    arr1 = np.array(p1)
    bi_words = ['Name:','Date of Birth:','Age:','SSN:']
    bi = []
    
    
    for i in arr1:
     if any(word in i for word in bi_words):
         l=i.upper()
         bi.append(l)
     else:
         pass
        
    
    bi[:] = (value for value in bi if value != '')
    bi[:] = (value.split(":") for value in bi)
    aka.append(bi[0][1].strip())
    aka[:] = (value.strip() for value in aka)
    
    
    #fetching unique county
    p2=profile_para[2].split("\n")
    add_words = ['Address Summary','Utility']
    add = []
    
    for i in p2:
     if any(word in i for word in add_words):
          pass
     else:
         l=i.upper()
         add.append(l)
         
    add[:] = (value for value in add if value != '')
    add[:] = (value.split(",") for value in add )
    
    county_list = []
    county_list[:] = (value[3] for value in add)
    county_list[:] = (value.split("(") for value in county_list)
    county_list[:] = (value[0].split(" ")[1] for value in county_list)
    
    
    #fetching unique states
    state= []
    state[:] = (value[2] for value in add)
    state[:] = (value.split(" ") for value in state)
    state[:] = (value[1] for value in state)
    
    state_name = []
    state_name[:] = (us.states.lookup(value).name for value in state)
    
    
    def unique(list1):
         
        unique_list = []
        # traverse for all elements   
        for x in list1:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)
        return unique_list  
    
    county_list = unique(county_list)
    state_name = unique(state_name)
    aka = unique(aka)
    #aka1 = (value.replace("\xa0"," ") for value in aka)
    #table = pd.DataFrame(columns=['url','name in article', 'age','place'])
    #table = pd.DataFrame(columns=range(0,6), index = [0]) # I know the size 
    table =[]

    k1=0

    for m in aka:
        
        nm=m.replace("\xa0"," ")
        #first_name = nm.split(" ",1)[0]
        #last_name = nm.split(" ",1)[1]
        
        
        #table.iloc[k1,] = [nm,' ',' ',' ']
        table.extend([[nm,' ',' ',' ',' ', ' ']])
        k1=k1+1
        
        options = Options()
        options.set_headless(headless=True)
        #driver = webdriver.Firefox(firefox_options=options, executable_path=r'C:\Utility\BrowserDrivers\geckodriver.exe')
        # create a new Firefox session
        #driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
        driver = webdriver.Firefox(firefox_options=options,executable_path='/usr/local/bin/geckodriver')
        #driver = webdriver.PhantomJS(executable_path= '/usr/local/bin/phantomjs')
        #driver = webdriver.Ie(executable_path='/usr/local/bin/IEDriverServer')
        driver.implicitly_wait(30)
        #driver.maximize_window()
    
        #access the website
        driver.get("https://sanctionssearch.ofac.treas.gov")
        
        
    
        #get the name text box to fill in data
        search_field = driver.find_element_by_id('ctl00_MainContent_txtLastName')
        search_field.clear()
        search_field.send_keys(nm)
    
        #click submit button
        driver.find_element_by_name("ctl00$MainContent$btnSearch").click()
        driver.implicitly_wait(30)
        htm= driver.page_source
        
        dfs = pd.read_html(htm)
    
        
        print(dfs[5])
        if (dfs[5].shape[1] > 1):
            df = dfs[5].values.tolist()
            table.extend(df)
        else:
            table.extend([['No reuslts',' No reuslts',' No reuslts',' No reuslts',' No reuslts', ' No reuslts']])

            
    dff=pd.DataFrame(table)

    return {'name':dff[0].tolist(),'address':dff[1].tolist(), 'type':dff[2].tolist(), 'program':dff[3].tolist(),'list':dff[4].tolist(), 'score':dff[5].tolist() }



