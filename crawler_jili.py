# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import json
import requests
import csv


headers={'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0)'
                     ' Gecko/20100101 Firefox/62.0'}



def get_car_index():
    detail=[]
    url='http://www.geely.com/api/geely/official/get/getAllSeries'
    s = requests.Session()
    r=s.get(url, headers=headers, timeout=10)
    data=r.json()
    for x in data:
        detail.append((x['seriesName'], x['seriesCode']))
    return detail


def get_province_index():
    detail=[]
    url='http://www.geely.com/api/geely/official/get/getprovincelist'
    s = requests.Session()
    r=s.get(url, headers=headers, timeout=10)
    data=r.json()
    for x in data:
        detail.append((x['regionName'], x['regionId']))
    return detail

def get_city_index(pro):
    detail=[]
    s = requests.Session()
    r=s.get('http://www.geely.com/api/geely/'
            'official/get/getcitylist?provinceid={}'.format(pro),
            headers=headers, timeout=10)
    data=r.json()
    for x in data:
        detail.append((x['regionName'], x['regionId']))
    return detail


def get_sale_company(car, pro, city):
    detail=[]
    s = requests.Session()
    r=s.get('http://www.geely.com/api/geely/'
            'official/get/GetDealer?'
            'seriesCode={}&province={}&'
            'city={}&keyword='.format(car, pro, city), 
            headers=headers, timeout=10)
    data=r.json()
    for x in data:
        detail.append(x['dealerName'])
    return detail
    


def crawl():
    columns=['车系', '省', '城市', '销售公司']
    list0=get_car_index()
    list1=get_province_index()
    with open('jili.csv', 'w', newline='') as csvfile:
         detail_wirter = csv.writer(csvfile, dialect=csv.excel())
         detail_wirter.writerow(columns)
         for y in list1: 
             list2=get_city_index(y[1])
             for z in list2:
                 for x in  list0:
                     list3=get_sale_company(x[1], y[1], z[1])
                     for i in list3:
                         try:
                             print(i)
                             detail_wirter.writerow([x[0], y[0], z[0], i])
                         except Exception as e
                             print(e, i)
if __name__=='__main__':
    crawl()











































