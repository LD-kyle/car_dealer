#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 19:18:36 2018

@author: lk
"""

import json
import time
import requests
import csv
from bs4  import BeautifulSoup


headers0={'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0)'
                     ' Gecko/20100101 Firefox/62.0'}

headers={'Accept':'application/json, text/javascript, */*; q=0.01',
          'Accept-Encoding'	:'gzip, deflate',
          'Connection':'keep-alive',
          'Accept-Language':'en-US,en;q=0.5',
          'Content-Length':'23',
          'Host':'mall.haval.com.cn',
          'X-Requested-With	':'XMLHttpRequest',
          'X-CSRF-TOKEN':'fe61d8447243ba04b10db4c05bc9aacd;CqzTzA',
          'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0)'
                     ' Gecko/20100101 Firefox/62.0',
          'Cookie':'_gscu_293425980=40287929zji01p87; Hm_lvt_503e901520f86'
                   '9597c8cba6f4c3efa32=1540287930,1540386410; userSelecte'
                   'dlocation=%7B%22provinceName%22%3A%22%E5%90%89%E6%9E%9'
                   '7%E7%9C%81%22%2C%22cityName%22%3A%22%E9%95%BF%E6%98%A5'
                   '%E5%B8%82%22%7D; userLocationId=%7B%22provinceId%22%3A'
                   '8%2C%22cityId%22%3A85%7D; TC_EV_DIR=0d1c06a0806ac9c68f'
                   '4ff8ca82256160; JSESSIONID=F88E6DE1ABD7B2EC088657E0231'
                   '23114; SERVERID=6f00e9cc68b4d71efd2f6baa6003356d|15406'
                   '54168|1540654167; Hm_lpvt_503e901520f869597c8cba6f4c3e'
                   'fa32=1540791964; _gscbrs_293425980=1; _gscs_293425980='
                   't40791881msd3lr13|pv:2',
          'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
          'Referer':'http://mall.haval.com.cn/dealer.html'}



def get_city_index():    
    detail=[]
    url='http://mall.haval.com.cn/dealer.html'
    s = requests.Session()
    done=True
    while done:
        try:
            r=s.get(url, headers=headers0, timeout=10)
            time.sleep(1)
            done=False
            if r.status_code!=200:
                done=True
        except Exception as e:
            print(e)    

    soup=BeautifulSoup(r.text, 'html.parser')
    div=soup.find('div', {'id':'header_areaContainer'})
    a=div.find_all('a')
    for x in a:
        detail.append(tuple(x['onclick'][14:-2].split("','")))
    return detail



def get_company(citys):
    columns=['车系', '省', '城市', '销售公司']
    s = requests.Session()
    url='http://mall.haval.com.cn/cars/getDealerByType.html'
    with open('haval.csv', 'w', newline='') as csvfile:
         detail_wirter = csv.writer(csvfile, dialect=csv.excel())
         detail_wirter.writerow(columns)
         for city in citys:
            done=True
            while done:
                try:
                    r=s.post(url,data={'city':city[1]}, headers=headers, 
                                       timeout=10)
                    time.sleep(1)
                    done=False
                    if r.status_code!=200:
                         done=True
                except Exception as e:
                    print(e)
            data=r.json()['list']
            print(city)
            for x in data:
                cars=x['carModel'].split(',')
                company=x['storeName']
                for car in cars:
                     detail_wirter.writerow([car, city[0], city[1], company])


if __name__=='__main__':
    citys=get_city_index()
    get_company(citys)
         
                    
































