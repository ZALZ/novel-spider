#coding:utf-8

import requests as r
from bs4 import BeautifulSoup as BS
import pandas as pd
import re
import time
import json

URL = "https://box.maoyan.com/promovie/api/box/second.json?beginDate={}"   #20180801

int_str = {1:"01",2:"02",3:"03",4:"04",5:"05",6:"06",7:"07",8:"08",9:"09"}
allcont = {}  #总票房


def get_json(url):
    res = r.get(url)
    resjson = json.loads(res.text)
    return resjson

def save_all(year,month,day,alldata):

    try:
        month = int_str[month]
    except:
        month = str(month)
    
    try:
        day = int_str[day]
    except:
        day = str(day)

    #info = sorted(record.items(), key=lambda x:x[1])
    for info in sorted(allcont.items(), key=lambda x:x[1],reverse=True)[:21]:
        alldata.write(info[0]+",,"+str(info[1])+","+str(year)+"-"+str(month)+"-"+str(day)+"\n")

def get_html(year,month,day,daydate):
    print(year,month,day)
    
    try:
        month = int_str[month]
    except:
        month = str(month)
    
    try:
        day = int_str[day]
    except:
        day = str(day)

    date = str(year)+month+day
    datas = get_json(URL.format(date))
    #file = open('alldata\\'+ date +".json",'w',encoding='utf-8')
    #json.dump(datas,file,ensure_ascii=False)
    #file.close()
    
    for info in datas["data"]['list']:
        name = info["movieName"].replace(",","，") #电影名
        daycount = info['boxInfo'] #单日票房
        sumcount = info['sumBoxInfo'] #总票房

        if daycount[-1] == "亿":
            daycount = eval(daycount[:-1])*10000
        else:
            daycount = eval(daycount[:-1])

        if sumcount[-1] == "亿":
            sumcount = eval(sumcount[:-1])*10000
        else:
            sumcount = eval(sumcount[:-1])

        daydate.write(name+", ,"+str(daycount)+","+str(year)+"-"+str(month)+"-"+str(day)+"\n")
        allcont[name] = sumcount
        
    
        file = open('alldata\\'+ date +".json",'w')
        json.dump(datas,file,ensure_ascii=False)
        file.close()


def js_data(datas):
    for info in datas["data"]['list']:
        print(info)
        

def main():
    daydate = open("daydate.csv",'w')
    daydate.write("name,type,value,date\n")
    alldata = open("alldate.csv",'w')
    alldata.write("name,type,value,date\n")
    err = open("err.csv",'w')
    
    
    for year in range(2011,2019):
        for month in range(1,13):

            if month in [1,3,5,7,8,10,12]:
                for day in range(1,32):
                    if year == 2018 and month == 8 and day== 19:
                        return
                    try:
                        get_html(year,month,day,daydate)
                        save_all(year,month,day,alldata)
                    except:
                        err.write(str(year)+str(month)+str(day))
                        continue
           

                        
            elif month in [4,6,9,11]:
                for day in range(1,31):
                    try:
                        get_html(year,month,day,daydate)
                        save_all(year,month,day,alldata)
                    except:
                        err.write(str(year)+str(month)+str(day))
                        continue
                    
            elif month == 2 and year in [2012,2016]:
                for day in range(1,30):
                    try:
                        get_html(year,month,day,daydate)
                        save_all(year,month,day,alldata)
                    except:
                        err.write(str(year)+str(month)+str(day))
                        continue
                    
            else:
                for day in range(1,29):
                    try:
                        get_html(year,month,day,daydate)
                        save_all(year,month,day,alldata)
                    except:
                        err.write(str(year)+str(month)+str(day))
                        continue
                    

    daydate.close()
    alldata.close()
                    

main()



