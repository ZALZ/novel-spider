#coding:utf-8

import requests
from bs4 import BeautifulSoup
import pandas as pd
from fontTools.ttLib import TTFont
from io import BytesIO
import re
import time

URL = "http://book.zongheng.com/rank/male/r1/c0/q{}{}01/{}.html"
monthdict = {1:"01",2:"02",3:"03",4:"04",5:"05",6:"06",7:"07",8:"08",9:"09",10:"10",11:"11",12:"12",}
total_yp_dic = {}
name_au = {}



def get_soup(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text,'html.parser')
    return soup

def gx_yp(name,yuepiao):    #更新total_yp_dic
    if name in total_yp_dic:
        total_yp_dic[name] += yuepiao
    else:
        total_yp_dic[name] = yuepiao

    
def get_all(url,date,file):
    soup = get_soup(url)
    for info in soup.find_all("ul",attrs = {'class': 'main_con'})[0].find_all("li"):
        allinfo = info.find_all("span")
        try:
            wtype = allinfo[1].a.string
        except:
            continue
        if wtype == "[]":
            continue
        name = allinfo[2].find("a").string
        yuepiao = allinfo[3].string
        author = allinfo[4].a.string
        gx_yp(name,int(yuepiao))
        name_au[name] = author
        file.write(name+","+author+","+yuepiao+","+date[0:4]+"-"+date[4:]+'\n')


def main():
    file = open("ZHRank.csv","w+")
    file.write("name,type,value,date\n")
    allRank = open("ZHAllRank.csv","w+")
    allRank.write("name,type,value,date\n")
    for page in range(1,5):
        print("2013-12",page)
        get_all("http://book.zongheng.com/rank/male/r1/c0/q20131201/{}.html".format(page),"201312",file)
    for keys in total_yp_dic.keys():
        allRank.write(keys+","+name_au[keys]+","+str(total_yp_dic[keys])+",2013-12\n")
    for year in range(2014,2019):
        for month in range(1,13):
            if year == 2018 and month > 7:
                break
            for page in range(1,5):
                print(year,"-",month,page)
                get_all(URL.format(year,monthdict[month],page),str(year)+str(month),file)
            for keys in total_yp_dic.keys():
                allRank.write(keys+","+name_au[keys]+","+str(total_yp_dic[keys])+","+str(year)+"-"+str(month)+"\n")
                


main()
