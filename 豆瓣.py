

import re       #正则表达式，进行文字匹配
from bs4 import BeautifulSoup    #网页解析，获取数据
import urllib.request,urllib.error      #指定URL，获取网页数据
import xlwt      #进行Excel操作






def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1.爬取网页
    datalist = getData(baseurl)

    savepath= ".//豆瓣电影top250.xls"
    # 3.保存数据
    saveData(datalist,savepath)
    # askURL('https://movie.douban.com/top250?start=')


#影片详情链接的规则
findLink = re.compile(r'<a href="(.*?)">')         #创建正则表达式对象，表示规则（字符串的模式）
# 影片图片
findImaSrc = re.compile(r'<img.*src="(.*?)"',re.S)   #re.S 让换行符包含在字符中
# 影片片名
findName = re.compile(r'<span class="title">(.*)</span>')
# 影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 找到影片相关内容
findDB = re.compile(r'<p class="">(.*?)</p>',re.S)


# 爬取网页
def getData(baseurl):
    datalist= []
    for i in range(0,10):        # 调用获取页面信息的函数，10次
        url = baseurl + str(i*25)
        html = askURL(url)          # 保存获取到的网页源码

        # 2.逐一解析数据
        soup = BeautifulSoup(html,'html.parser')
        for item in soup.find_all('div',class_="item"):     # 查找符合要求的字符串，形成列表
            # print(item)     #测试：查看电影item全部信息
            data = []       #保存一部电影的全部信息
            item = str(item)

            # 影片详情的链接
            link = re.findall(findLink,item)[0]         #re库用来通过正则表达式查找指定的字符串
            data.append(link)                           #添加链接

            imgSrc = re.findall(findImaSrc,item)[0]
            data.append(imgSrc)                         #添加图片

            name = re.findall(findName,item)
            if(len(name) == 2):
                cname = name[0]
                data.append(cname)                  #添加中国名
                uname = name[1].replace('/','')     #去掉无关符号
                data.append(uname)                  #添加外国名
            else:
                data.append(name[0])
                data.append(' ')                    #外国名留空

            Rating = re.findall(findRating,item)[0]
            data.append(Rating)

            Judge = re.findall(findJudge,item)[0]
            data.append(Judge)

            Inq = re.findall(findInq,item)
            if len(Inq) !=0:
                Inq = Inq[0].replace('。','')       #去掉句号
                data.append(Inq)
            else:
                data.append(' ')

            DB = re.findall(findDB,item)[0]
            DB =re.sub('<br(\s+)?/>(\s+)?',' ',DB)          #去掉br
            DB = re.sub('/',' ',DB)                     #去掉/
            data.append(DB.strip())                 #去掉前后空格

            datalist.append(data)                   #把处理好的一部电影信息放入datalist中
    print(datalist)
    return datalist


# 得到一个指定的URL的网页内容
def askURL(url):
    head ={      # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 86.0.4240.111Safari / 537.36"
    }               # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器---浏览器
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)

    return html

# 保存数据
def saveData(datalist,savepath):
    book = xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet = book.add_sheet('豆瓣电影top250',cell_overwrite_ok=True)
    col = ("电影详情链接","图片链接","影片中文名","影片外国名","评分","评价数","概况","相关信息","")
    for i in range(0,8):
        sheet.write(0,i,col[i])     #列名
    for i in range(0,250):
        print('第%d条'%(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])      #数据
    book.save(savepath)                 #保存





if __name__ == '__main__':
    main()
    print('爬取完毕')