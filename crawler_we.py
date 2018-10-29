#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 14:58:09 2018

@author: lk
"""

import json
import time
import requests
import csv
from bs4  import BeautifulSoup


headers={'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0)'
                     ' Gecko/20100101 Firefox/62.0'}

def get_pro_city():
    citys=[]
    url='https://www.wey.com/index.php?m=tiyan&c=index&a=province'
    r=requests.get(url,  headers=headers, timeout=10)
    data=r.json()
    for x in data:
        citys.append((x['province'], x['city']))
    return citys
        
    

def crawl(citys):
    columns=['车系', '省', '城市', '销售公司']
    s = requests.Session()
    with open('wey.csv', 'w', newline='') as csvfile:
         detail_wirter = csv.writer(csvfile, dialect=csv.excel())
         detail_wirter.writerow(columns)
         for city in citys:
             done=True
             while done:
                 try:
                     r=s.get('https://www.wey.com/index.php?m=tiyan&c=index&a='
                             'distributor&b={}&t=/经销商'.format(city[1]),
                             headers=headers, timeout=10)
                     time.sleep(1)
                     done=False
                     if r.status_code!=200:
                          done=True
                 except Exception as e:
                     print(e)
             print(city)
             data=r.json()
             if type(data) is list:
                 for x in data:
                     try:
                         detail_wirter.writerow(['WEY', city[0], city[1],
                                         x['sh_serviceStoreName']])
                     except Exception as e:
                         print(e, city)
             else:
                 print(data, city)

if __name__=='__main__':
    citys=get_pro_city()
    crawl(citys)
    
    
    