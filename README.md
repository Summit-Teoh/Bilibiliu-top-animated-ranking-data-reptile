# -
有关获取哔哩哔哩热门动画排行榜数据的爬虫

程序要点总结

程序入口和主流程

主函数main()定义了程序的入口，主要执行以下步骤：
定义基准URL地址。
调用GetData()函数爬取数据。
调用SaveData()函数保存数据到Excel文件。
爬取网页数据

GetData(baseurl)函数负责获取并解析网页数据：
定义一个空列表datalist用于存储爬取的数据。
循环获取30个页面的数据，通过替换URL中的页码实现分页抓取。
调用AskUrl(url)函数获取每个页面的源码（JSON数据）。
使用正则表达式和json库解析JSON数据，提取番剧信息。
通过BeautifulSoup解析番剧详情页，提取更多详细信息如标签和简介。
将每个番剧的信息存入列表，并追加到datalist中。
发送网络请求

AskUrl(url)函数负责发送HTTP请求获取网页内容：
使用urllib.request模块构建请求，并伪装成浏览器发送请求。
处理请求异常，捕获错误信息。
返回获取的网页数据（HTML或JSON格式）。
解析网页和提取数据

使用BeautifulSoup解析HTML内容，提取特定标签中的文本信息。
使用正则表达式提取并处理字符串内容。
保存数据到Excel

SaveData(datalist, savepath)函数负责将数据保存到Excel文件：
检查文件是否存在，存在则打开文件，不存在则创建新文件。
调用Auto_Type(datalist, sheet)函数设置自适应列宽。
写入表头和数据到Excel文件中。
保存Excel文件。
自适应列宽设置

Auto_Type(datalist, sheet)函数负责根据数据内容设置Excel列宽：
计算每列的最大宽度，根据字符类型（中文或英文）设置合适的宽度。
设置每列的宽度，使数据在Excel中显示时不被截断。
总结
核心功能：该程序从指定的Bilibili API获取番剧数据，通过解析页面详情获取更多信息，并将数据保存到Excel文件中。
技术要点：
使用urllib.request模块发送HTTP请求。
使用BeautifulSoup解析HTML内容。
使用正则表达式和json库处理数据。
通过xlwt和xlrd库操作Excel文件。
实现数据的自动化抓取和存储，并处理网络请求的异常和错误。
