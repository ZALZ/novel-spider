# coding=utf-8
import requests
import time
import os
import bs4
import re

URLROOT = 'http://www.bx1k.com/funnyimg/find-cate-2-p-{}.html'
ROOT = "D://workspace//视频//福利沙雕GIF//PIC3//"

hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}

def gettext(url):
    try:

        r = requests.get(url,headers = hea)
        r.raise_for_status()
        r.encoding = "utf-8"
        return r.text
    except:
        print(r.status_code)



def getDirUrl(url):
    html = gettext(url)
    soup = bs4.BeautifulSoup(html,"html.parser")
    print("******"+soup.title.string+"******")
    dirpath = ROOT+soup.title.string+"//"
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    for li in soup.find_all('li'):
        if not getPicUrl(URLROOT+li.a['href'],dirpath):
            print("ÎÄ¼þ¼ÐÒÑ´æÔÚorÍ¼Æ¬µØÖ·´íÎó")
            return False
    return True

def getPicUrl(url):
    html = gettext(url)
    soup = bs4.BeautifulSoup(html,"html.parser")
    li = soup.find('ul',attrs={'class':'cf','id':'thumb-ul'}).find_all('li')
    for i in li[:-1]:
        name = i.a.img['data-intro']
        href = i.a.img['big_src']
        if not save(href,ROOT,name):
            print('失败')

        print('成功')
            
def getmaindir(url):
     try:
        html = gettext(url)
        soup = bs4.BeautifulSoup(html,"html.parser")
        pic = soup.find_all('ul',class_='plist cf')
        for li in pic[0].find_all('li'):
            getPicUrl(li.a['href'])
            
            '''name = p.a.img['alt']
            if 'data-gif' in p.a.img.attrs:
               if not save(p.a.img['data-gif'],ROOT,name):
                    print("失败")
                    continue
            else:
                print('保存JPG中\t', end=' ')
                if not save(p.a.img['src'],ROOT,name):
                    print('失败')
                    continue
            print("成功")'''
     except:
         return False


    
def save(url,dirpath,name):
    print("正在保存"+name,end='\t')
    path = dirpath + name + '.' + url.split('.')[-1]
    try:
        if not os.path.exists(path):
            r = requests.get(url,headers = hea)
            with open(path,'wb') as f:

                f.write(r.content)
        else:
            return False
        return True
    except:
        return False
        print("保存输出哦")
        
def main():
    start = time.perf_counter()
    for i in range(1,20):   #796
        print("正在保存第{}页".format(i))
        if not getmaindir(URLROOT.format(i)):
            continue

    end = time.perf_counter()
    print("total time:{:.2f}".format(end-start))

    
main()
