#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 14:29:34 2018

@author: monishasaw
"""


#Automating JUSTICE Sanction search

#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.support.wait import WebDriverWait
#import pyautogui
#import time
#import shutil
#import pathlib
from requests import get
import docx2txt
import us
import re
import os
#from astropy.table import Table, Column
#import str


def doj_search1():
    
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
    table=[]
    k1=0

    for m in aka:
       

        #nm=bi[0][1].strip()
        nm=m.replace("\xa0"," ")
        first_name = nm.split(" ",1)[0]
        last_name = nm.split(" ",1)[1]
        page=1
        urls = []
        
        #table.iloc[k1,] = [nm,' ',' ',' ']
        table.append([nm,' ',' ',' '])
        k1=k1+1
    
    
        #article url extraction
        
        while True:
          url = 'https://search.justice.gov/search?affiliate=justice&commit=Search&page='+"%s" % page+'&query="'+first_name+'+'+last_name+'"&utf8=%E2%9C%93'
          print(first_name + last_name)
          print(url)
          response = get(url, timeout = 10)
          html_soup = BeautifulSoup(response.text, 'html.parser')
          content = html_soup.find_all('div', class_ = 'content-block-item')
          if('Sorry, no results' not in content[0].text):
            links = html_soup.find_all('div', class_ = 'url')
            pagination=html_soup.find_all('div',class_='pagination')
            page=page+1
            for container in links:
              link = container.text
              print(link)
              urls.append(link)
          else:
               break
          if('next_page disabled' in  ("%s" % pagination[0])):
                break
            
        
        urls = unique(urls)
        
        if(len(urls)>=1):
        #article analysis
            
           l_url = len(urls)
           for i in range(l_url):
            
            #fetch one article
             if('.pdf' in urls[i]):
               url = 'https://'+urls[i]
               art_name = ''
               age = ''
             elif(urls[i] == "www.justice.gov/dag"):
               url = 'https://'+urls[i]
               art_name = ''
               age = ''
             else: 
              url = 'https://'+urls[i]
              response = get(url)
              html_soup1 = BeautifulSoup(response.text, 'html.parser')
              art = html_soup1.find('div', class_ = 'node__content').text
            
            
            #Figure out the name in article
              start= first_name
              stop = last_name
              art_name= []
              
              k=re.findall(start +' '+ stop ,art, re.IGNORECASE)
              k=unique(k)    
              #k[:] = (value for value in k if value != ' ')
              l1 = len(k)
              if(l1==1):
                  art_name = k[0]
              else: 
                 art_name = start+' '+stop+' not found in article'
                    
                 
            # Figuring out the age
              art1=art.split(".")
              art2=art.split()
              art_name_sen = []
              art_age = []
              #age = []
              
    
              for j in art1:
                 if(' age ' in j):
                     l=j.upper()
                     art_age.append(l)
                 else:
                     pass
              
              age = "||".join(art_age)
    
    
            
            #place match
              PLACE = []
              for j in art2:
                 if(us.states.lookup(j)):
                     #l=j.upper()
                     PLACE.append(j)
                 else:
                     pass
              
              PL = "||".join(PLACE)
        
            
            #add a row in the table      
             #table.loc[k1] = [urls[i], art_name, age, PL]
             table.append([urls[i], art_name, age, PL]) 
             k1=k1+1
             #print(table.loc[k])
            
        else:
            table.append(['No results found','no results found','No results found','No results found'])
            k1=k1+1
            #write to excel
        #fil='/Users/monishasaw/Documents/VCheck Global/Due Diligence AI/test-'+m+'-' + "%s" % len(urls)+'-results.xls'
        #table.to_excel(fil, sheet_name='sheet1', index=False)
        
    #lis=table.values.tolist()
    df=pd.DataFrame(table)
    
    return {'url':df[0].tolist(),'name':df[1].tolist(), 'age':df[2].tolist(), 'place':df[3].tolist()}



# figuring out the age
 # age = 
 



    #do a string search
    #look for the matches
    #give it score if match- makes it above 50
    #give nothing if no information availabke to filter out
    #give a zero score if it has different county and different or different age.
    #check for all the combinations-
    
















