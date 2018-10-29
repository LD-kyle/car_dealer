#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 15:22:57 2018

@author: lk
"""

import json
import time
import requests
import csv
from bs4  import BeautifulSoup


headers={'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0)'
                     ' Gecko/20100101 Firefox/62.0'}

def get_province_index():
    pros, done=[], True
    url='https://www.lynkco.com.cn/api/geely/lynk/region/GetAllProvince'
    s = requests.Session()
    while done:
        try:
            r=s.get(url, headers=headers, timeout=10)
            time.sleep(1)
            done=False
            if r.status_code!=200:
                done=True
        except Exception as e:
            print(e)
    details=r.json()['data']
    for x in details:
        pros.append((x['regionName'], x['regionId'], x['regionCode']))
        
    return pros

def get_city_index(city):
    citys, done=[], True
    while done:
        try:
            r=requests.get('https://www.lynkco.com.cn/api/geely/lynk/region/'
                   'GetCitiesByPro?regionId={}'.format(city),
                   headers=headers, timeout=10)
            time.sleep(1)
            done=False
            if r.status_code!=200:
                done=True
        except Exception as e:
            print(e)
    details=r.json()['data']
    for x in details:
        citys.append((x['regionName'], x['regionCode'])) 
    return citys


def get_sale_company(pro, city):
    companys, done=[], True
    s = requests.Session()
    while done:
        try:
            r=s.get('https://www.lynkco.com.cn/api/geely/lynk/dealer'
                    '/get?provinceCode={}&cityCode='
                    '{}'.format(pro, city), 
                    headers=headers, timeout=10)
            time.sleep(1)
            done=False
            if r.status_code!=200:
                done=True
        except Exception as e:
            print(e)
    details=r.json()['data']
    for x in details:
        companys.append(x['dealerName']) 
    return companys
    
        
    
def crawl():
    columns=['车系', '省', '城市', '销售公司']
    pros=get_province_index()
    #print(pros)
    with open('lynkco.csv', 'w', newline='') as csvfile:
         detail_wirter = csv.writer(csvfile, dialect=csv.excel())
         detail_wirter.writerow(columns)
         for pro in pros: 
             citys=get_city_index(pro[1])
             #print(citys)
             for city in citys:
                 companys=get_sale_company(pro[2], city[1])
                 #print(companys)
                 for company in companys:
                     try:
                         print(company)
                         detail_wirter.writerow(['lynkco', pro[0], city[0],
                                                 company])
                     except Exception as e:
                         print(e, company)


if __name__=='__main__':
    crawl()