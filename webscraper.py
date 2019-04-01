# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 18:38:24 2018

@author: dhruvi.vadalia

web scraper for greatplacetowork.net
"""

"""importing all the necessary modules"""
from bs4 import BeautifulSoup as bs
#import pandas as pd
#import numpy as np
import urllib3
import re
from selenium import webdriver
#import sys
import time
import csv
""" getting the link"""
http = urllib3.PoolManager()
url = 'http://www.greatplacetowork.net/best-companies/browse-international-lists'
response  = http.request('GET',url)
soup = bs(response.data,"lxml")

new_table=[]        #list to store all the links
var = False    
"""find the table in the page"""
t = soup.find('table')
if t:
    table = t
else:
    print("No tables found in this page")
     #boolean to end the while loop

""" putting all links in a list using a function """
def add_links_to_list(t,var,table):
       v = False
       for row in table.find_all('tr'):
              column_marker = 0
              col=[]
              columns = row.find_all('td')
              for column in columns:
                  column_marker+=1
                  if(column_marker==2):
                      #print(type(column.find('a',href = True)))
                      temp  = re.findall(r'"([^"]*)"', str(column.find('a',href = True)))
                      col.append('http://www.greatplacetowork.net'+''.join(temp))
                  else:
                      col.append(column.get_text())
                  if(column_marker == 4):
                      print(column.get_text())
                      if(str(column.get_text())!='2018' and str(column.get_text())!='2017'):
                          v = True
                          print("about to break")
                          break
              t.append(col)
       return t,v

"""Selenium to click on the 'next' link in pagination"""
def Click_on_Next(new_table,var,url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.find_element_by_xpath("//*[@id='sectJsfSrchResNavPgr-content']/ul/li[14]/strong/a").click()
    time.sleep(10)
    url = driver.current_url
    response  = http.request('GET',url)
    soup = bs(response.data,"lxml")
    table = soup.find('table')
    (new_table,var) = add_links_to_list(new_table,var,table)

""" Getting all the links for years 2018 and 2017 by looping the get links function and the selenium click function"""
(new_table,var) = add_links_to_list(new_table,var,table)
driver = webdriver.Chrome()
driver.get(url)
driver.find_element_by_xpath("//*[@id='sectJsfSrchResNavPgr-content']/ul/li[14]/strong/a").click()
time.sleep(10)
url = driver.current_url
(new_table,var) = add_links_to_list(new_table,var,table)
while(var != True):
    Click_on_Next(new_table,var,url)

#print(var)
print()
print()
print()
for item in new_table:
       print(item)
print()

#for item in new_table:
#       link = item[1]
#       response = http.request('GET',link)
#       soup = bs(response.data,"lxml")

#Next = re.findall(r'"([^"]*)"', str(soup.find('a',{'title':'Next'})))[0]
#print('http://www.greatplacetowork.net'+''.join(Next))
#print(sys.prefix)


"""creating a csv and loading data into it"""
with open(data.csv,'w',newline = ' ') as f:
  thewriter = csv.writer(f)
  fieldnames = ['rank','company_name','something','no. of employees']
  thewriter.writeheader()

  thewriter.writerow("""pass the data you want to store""")