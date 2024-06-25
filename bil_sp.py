from bs4 import BeautifulSoup
import re
import xlwt
import urllib.request,urllib.error
import json
import os
import xlrd
from xlutils.copy import copy

#程序入口
def main():
    #URL网址
    baseurl = "https://api.bilibili.com/pgc/season/index/result?st=1&order=3&season_version=-1&spoken_language_type=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&sort=0&page=1&season_type=1&pagesize=20&type=1"
    #1. 爬取网页
    datalist = GetData(baseurl)
    savepath = "5.21/bili追番人数排行.xls"#Excel路径
   

    #3. 保存数据
    SavaData(datalist,savepath)


#解析URL数据
def GetData(baseurl):
    datalist = []
    # 1. 爬取网页
    for i in range(0,30):#获取30个页面信息
        str_temp = "page=" + str(i+1)
        url = baseurl.replace("page=1",str_temp)#替换URL网址
        jsonbili = AskUrl(url)#保存获取的网页源码(源码为json数据）
        print(f"第{i+1}页已开始")
       

    #2. 数据解析
        # print(soup.prettify())#使HTML标准化输出;HTML文件中排版：ctrl+alt+l
        datafind = re.findall(r"\"list\":(.+?),\"num\"",str(jsonbili))#返回列表
        jsondata = json.loads(datafind[0])#将已编码的 json字符串解码为 python 对象，转换为字典
        for item in jsondata:
            data = []

            title = item["title"]  # 番剧名称
            data.append(title.strip())
            num = item["order"]  # 追番人数
            data.append(num.strip())
            status = item["index_show"]  # 更新状态
            data.append(status.strip())
            image = item["cover"]#封面链接
            data.append(image.strip())
            link = item["link"]#番剧链接
            data.append(link.strip())
            score = item["score"]#番剧评分
            data.append(score.strip())

         # 进入番剧链接爬取更多信息
            html = AskUrl(item["link"])  # 保存获取的网页源码
            soup = BeautifulSoup(html, "lxml")  # 解析
            
           
            #提取动画标签
            for div_tag in soup.find_all('div', class_='mediainfo_mediaDesc__jjRiB'):
            # 获取div标签内的所有span标签
                span = div_tag.find('span')
        
                if span:
                # 如果span标签有文本内容，
                    text = span.get_text().strip()
                    break  # 找到并打印第一个非空span后退出循环    

            data.append(text)
                   
        

            # 提取 <p> 标签中的文本内容,简介
            for item1 in soup.find("p", class_="mediainfo_content_placeholder__Tgx67"):
            
                item2 = item1.get_text()
                item2 = str(item2)  # 转换为字符串用于正则表达式搜索
                item3= item2.replace("\n", " ")
                introduction = re.split(r'[。· ， ？]', item3)[:2] 
                # stri = "".join(str(item) for item in introduction)
                data.append(introduction)

                datalist.append(data)#追加每页信息 注意缩进
        #print(datalist)
    return  datalist



#获取指定的URL网页内容
def AskUrl(url):
    head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}#通过Uaer-Agent伪装为谷歌浏览器
    request = urllib.request.Request(url,headers=head)#封装请求
    html = ""
    try:
        response = urllib.request.urlopen(request)#发送请求
        html = response.read().decode("utf-8")#解码为utf-8
    except urllib.error.URLError as e:
        if hasattr(e, "code"):  # 出错代码
            print(e.code)
        if hasattr(e, "reason"):  # 出错原因
            print(e.reason)

    return html#返回网页数据


#自适应列宽设置
def Auto_Type(datalist,sheet):
    col_width = []

    for i in range(len(datalist[0])):# 每列
        for j in range(len(datalist)):# 每行
            number1 = number2 = 0#统计字符宽度
            for char in datalist[j][i]:
                try:
                    if 0x4e00 <= ord(char) <= 0x9fff or ord(char) == 0x0020:#unicode字符集（utf-8解码）
                        number1 += 2
                    else:
                        number2 += 1
                except Exception as e:
                    if hasattr(e, "code"):  # 出错代码
                        print(e.code)
                    if hasattr(e, "reason"):  # 出错原因
                        print(e.reason)
            number = number1 + number2
            if j == 0:
                col_width.append(number)# 数组增加一个元素
            else:
                if col_width[i] < number:# 获得每列中的内容的最大宽度
                    col_width[i] = number
        width = 256*(col_width[i]+1)
        if width >= 65535:
            width = 65535
        sheet.col(i).width = width#设置列宽


#保存数据到Excel
def SavaData(datalist,savepath):
    if not(os.path.isfile(savepath)):
        book = xlwt.Workbook(encoding="utf-8")#创建文件
        sheet = book.add_sheet("bili")#创建表单
        Auto_Type(datalist, sheet)#自适应列宽
        print("表格创建成功\n")
    else:
        rb = xlrd.open_workbook(savepath,formatting_info=True)#打开文件
        book = copy(rb)
        sheet = book.get_sheet(0)#打开表单
        print("表格打开成功\n")
    col = ["番剧名称","追番人数","更新状态","封面链接","番剧链接","评分","漫画标签","番剧简介"]         
    for i in range(len(datalist[0])):
        sheet.write(0,i,col[i])#写入第一行
    for i in range(len(datalist)):#存入数据
        print("正在写入第%s条"%(i+1))
        data = datalist[i]
        for j in range(len(datalist[0])):
            sheet.write(i+1,j,data[j])

    book.save(savepath)#保存数据




#程序执行入口
if __name__ == "__main__":
    #调用函数
    main()
    print("爬取完毕")
