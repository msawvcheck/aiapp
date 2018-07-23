#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 10:24:04 2018

@author: monishasaw
"""

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
#import numpy as np
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
#import docx2txt
#import us
#import re


def ofac_search_name1(nm):
        
        table =[]
        #table.iloc[k1,] = [nm,' ',' ',' ']
        table.extend([[nm,' ',' ',' ',' ', ' ']])
        
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



