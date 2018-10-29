#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 15:27:16 2018

@author: lk
"""

import json
import time
import requests
import csv
from bs4  import BeautifulSoup


headers={'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0)'
                     ' Gecko/20100101 Firefox/62.0'}

headers1={'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0)'
                     ' Gecko/20100101 Firefox/62.0',
          'Cookie':'TC_EV_DIR=1a8b985533bc99005fb978adbbf3cd5e; JSESSIONID=87'
                    '484DD05BD0168A37C9A90CBAA727C5; SERVERID=6f00e9cc68b4'
                    'd71efd2f6baa6003356d|1540046462|1540046461; _gscu_293'
                    '425980=40287929zji01p87; _gscbrs_293425980=1; Hm_lvt_'
                    '503e901520f869597c8cba6f4c3efa32=1540287930; Hm_lpvt_'
                    '503e901520f869597c8cba6f4c3efa32=1540304198; userSele'
                    'ctedlocation=%7B%22provinceName%22%3A%22%E5%90%89%E6%'
                    '9E%97%E7%9C%81%22%2C%22cityName%22%3A%22%E9%95%BF%E6%'
                    '98%A5%E5%B8%82%22%7D; userLocationId=%7B%22provinceId'
                    '%22%3A8%2C%22cityId%22%3A85%7D; _gscs_293425980=t4030'
                    '4188gtcqro87|pv:1',
          'content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
          'Referer':'http://mall.haval.com.cn/dealer.html'}
          
def get_car_pro_index():
    cars, pros=[], []
    url='http://www.bydauto.com.cn/counter-sellpoint.html'
    s = requests.Session()
    done=True
    while done:
        try:
            r=s.get(url, headers=headers, timeout=10)
            time.sleep(1)
            done=False
            if r.status_code!=200:
                done=True
        except Exception as e:
            print(e)    
    soup=BeautifulSoup(r.text, 'html.parser')
    div=soup.find('div', {'class':'content1'})
    spans=div.find_all('span')
    options=spans[1].find_all('option')
    for option in options[1:]:
        cars.append((option.text, option['value']))
    options=spans[3].find_all('option')
    for option in options[1:]:
        pros.append((option.text, option['value']))
    return cars, pros


def get_province_index(car):
    pros, done=[], True
    url='http://www.bydauto.com.cn/ajax.php?act=getpro&inajax=1'
    s = requests.Session()
    while done:
        try:
            r=s.post(url, data={'carid':car}, headers=headers)
            time.sleep(1)
            done=False
            if r.status_code!=200:
                done=True
        except Exception as e:
            print(e)
   
    soup=BeautifulSoup(r.text, 'html.parser')
    options=soup.find_all('option')
    for option in options:
        pros.append(option['value'])
    return pros

def get_city_index(car, pro):
    citys=[]
    s = requests.Session()
    url='http://www.bydauto.com.cn/ajax.php?act=getcity&inajax=1'
    done=True
    while done:
        try:
            r=s.post(url, data={'carid':car, 'pid': pro}, 
                     headers=headers, timeout=10)
            time.sleep(1)
            done=False
            if r.status_code!=200:
                done=True
        except Exception as e:
            print(e)
    soup=BeautifulSoup(r.text, 'html.parser')
    options=soup.find_all('option')
    for option in options:
        citys.append(option['value'])
    return citys


def get_sale_company(car, city):
    detail=[]
    s = requests.Session()
    url='http://www.bydauto.com.cn/ajax.php?act=getsellpoint&inajax=1'
    done=True
    while done:
        try:
            r=s.post(url, data={'carid':car, 'showtype':'json', 'cid':city},
                    headers=headers)
            time.sleep(1)
            done=False
            if r.status_code!=200:
                done=True
        except Exception as e:
            print(e)
    data=r.json()
    for x in data:
        detail.append(x['sjname'])
    return detail
    


def crawl():
    columns=['车系', '省', '城市', '销售公司']
    cars=get_car_pro_index()[0]
    with open('byd.csv', 'w', newline='') as csvfile:
         detail_wirter = csv.writer(csvfile, dialect=csv.excel())
         detail_wirter.writerow(columns)
         for x in cars: 
             car=x[1]
             pros=get_province_index(car)
             for pro in pros:
                 citys=get_city_index(car, pro)
                 for city in  citys:
                     companys=get_sale_company(car, city)
                     for i in companys:
                         try:
                             print(i)
                             detail_wirter.writerow([x[0], pro, city, i])
                         except Exception as e:
                             print(e, i)
if __name__=='__main__':
    crawl()





