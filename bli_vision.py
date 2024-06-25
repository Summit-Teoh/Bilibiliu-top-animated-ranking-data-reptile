import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from matplotlib.font_manager import FontProperties

# 设置中文字体
font = FontProperties(fname='C:/Windows/Fonts/SimHei.ttf')   # 请将路径替换为您本地的中文字体路径

# 定义一个函数来提取数字并转换为追番人数
def extract_followers(follower_str):
    # 使用正则表达式提取数字部分
    match = re.search(r'([\d.]+)', follower_str) 
    if match:
        # 提取到的数值部分乘以10000
        return float(match.group(1)) * 10000
    return 0

# 读取数据
df = pd.read_excel('bili追番人数排行.xls')

# 数据处理
df['追番人数'] = df['追番人数'].apply(extract_followers)
df['评分'] = df['评分'].astype(float)

# 条形图：按追番人数显示番剧排名（显示排名前10的番剧）
top_n = 30   # 指定显示排名前10的番剧
# 首先对DataFrame进行排序和切片
df_top_n = df.sort_values(by='追番人数', ascending=False).head(top_n)
# 然后将排序和切片后的DataFrame传递给sns.barplot
plt.figure(figsize=(12, 8))
sns.barplot(x='追番人数', y='番剧名称', data=df_top_n)
plt.xlabel('追番人数', fontproperties=font)
plt.ylabel('番剧名称', fontproperties=font)
plt.title('按追番人数排名的番剧(排名前{})'.format(top_n), fontproperties=font)
plt.xticks(fontproperties=font)
plt.yticks(fontproperties=font)
plt.show()

# 使用散点图代替折线图：不同番剧的评分分布
top_n = 30
df_top_n = df.loc[:top_n-1, ['番剧名称',  '评分']]
plt.figure(figsize=(15, 7))
sns.scatterplot(x='评分', y='番剧名称', data=df_top_n)
plt.xlabel('评分', fontproperties=font)
plt.ylabel('番剧名称', fontproperties=font)
plt.title('不同番剧的评分分布(排名前{})'.format(top_n), fontproperties=font)
plt.xticks(fontproperties=font)
plt.yticks(fontproperties=font)
plt.show()

# 散点图：追番人数与评分的关系
df_top_n = df.loc[:top_n-1, ['追番人数','评分','漫画标签']]
plt.figure(figsize=(12, 8))
sns.scatterplot(x='评分', y='追番人数', hue='漫画标签', data=df_top_n)
plt.xlabel('评分', fontproperties=font)
plt.ylabel('追番人数', fontproperties=font)
plt.title('追番人数与漫画标签的关系(排名前{})'.format(top_n), fontproperties=font)
plt.legend(loc='best', prop=font)
plt.xticks(fontproperties=font)
plt.yticks(fontproperties=font)
plt.show()



# 饼状图：不同漫画标签的分布（显示排名前top_n的标签）
top_n = 10  # 指定显示排名前10的标签
# 首先对漫画标签进行分组统计，并获取排名前top_n的标签
label_counts = df['漫画标签'].value_counts().head(top_n)
plt.figure(figsize=(10, 10))
plt.pie(label_counts, labels=label_counts.index, autopct='%1.1f%%', startangle=140, textprops={'fontproperties': font})
plt.title('不同漫画标签的分布(排名前{})'.format(top_n), fontproperties=font)
plt.show()