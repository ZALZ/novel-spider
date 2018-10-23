import requests
from bs4 import BeautifulSoup
from io import BytesIO
import re
import time


WORD_MAP={"period":".","zero":"0","one":"1","two":"2","three":"3","four":"4","five":"5","six":"6","seven":"7","eight":"8","nine":"9"}


def get_ttf(span):
    res = re.search("https://qidian.gtimg.com/qd_anti_spider/[a-zA-Z]*.ttf",span)
    url = res.group(0)
    ttf = url.split("/")[-1].split(".")[0]
    con = requests.get(url).content
    return con,ttf

def get_html(url,file,date):
    info = []
    hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    r = requests.get(url,headers = hea , timeout = 30)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text,'html.parser')
    
    for i in soup.select('.book-img-text'):#使用ccs的select方法,返回所有属性book-mid-info下的a标签,排名榜单
        con,ttf = get_ttf(str(i))   #获取ttf的content和名字，网络字体反爬
        font = TTFont(BytesIO(con))
        cmap = font.getBestCmap()
        font.close()
        count = re.findall('<span class=\"'+ttf+'\">[&#0-9;]*</span>' , r.text,re.S) #找到所有月票数字所在
        lists = []   #月票列表
        for j in count:   #获取月票列表
            total = ""
            totallist = j.split(">")[1].split("<")[0].split(";")[:-1]
            for each in totallist:   #更新数字
                ch = cmap.get(eval(each[2:]))
                total += WORD_MAP.get(ch,"")
            lists.append(total)

        title = []  #标题列表
        for j in i.select("h4"):
            title.append(j.string)

        author = [] #作者列表
        noveltype = []  #小说类型列表
        for j in i.select(".author"):
            k = j.find_all("a")
            author.append(k[0].string)
            noveltype.append(k[1].string)
        for i in range(len(lists)):
            file.write("《"+title[i]+"》"+","+author[i]+","+lists[i]+","+date+"\n")
            print("写入成功")

def main():
    url = 'https://www.qidian.com/mm/rank/yuepiao?style=1&chn=-1&month={}&year={}&page={}'
    monthdict = {1:"01",2:"02",3:"03",4:"04",5:"05",6:"06",7:"07",8:"08",9:"09",10:"10",11:"11",12:"12"}
    file = open("qidianGirlRank.csv","w+")
    file.write("name,type,value,date\n")
    for year in range(2015,2019):
        for month in range(1,13):
            if year == 2018 and month > 7:
                break
            for page in range(1,4):
                print(year,"-",month,page)
                get_html(url.format(monthdict[month],year,page),file,str(year)+"-"+str(month))
                #time.sleep(1)


main()
