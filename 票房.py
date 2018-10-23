#coding = utf-8
import requests as r
from bs4 import BeautifulSoup
import re
import time as t





URL = "http://www.cbooo.cn/BoxOffice/getMonthBox?sdate={}-{}-01"

def get_soup(url):
    res = r.get(url)
    res.raise_for_status()
    res.encoding = "utf-8"
    #soup = BeautifulSoup(res.text,"html.parser")
    return res.text

def main():
    file = open("movieRank.csv","w+")
    file.write("name,type,value,date\n")
    
    for year in range(2008,2019):
        for month in range(1,13):
            print(str(year)+"-"+str(month))
            try:
                for rank in eval(get_soup(URL.format(year,month)))["data1"][:-1]:
                    file.write(rank["MovieName"]+", ,")
                    file.write(rank["boxoffice"]+",")
                    file.write(str(year)+"-"+str(month)+"\n")              
            except:
                print("这个月的出错了")
                continue
    

main()
