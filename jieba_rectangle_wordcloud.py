import logging
import collections
import re
import math

import jieba
from wordcloud import WordCloud

jieba.setLogLevel(logging.INFO)


# 创建停用词列表
def stopwordslist():
    # 按行读入
    stopwords = [line.strip() for line in open('chinsesstop.txt', encoding='UTF-8').readlines()]

    # 分割为单个字符（列表解析）
    stopwords = [k for s in stopwords for k in s]
    return stopwords


# # 指定字符串方式
# text = "collections在python官方文档中的解释是High-performance container datatypes，直接的中文翻译解释高性能容量数据类型。它总共包含五种数据类型"

# 文件读取方式
f = open("./article.txt", "r", encoding="utf-8")
text = f.read()
f.close()

# 生成词云的词频限制，选取前30%
TopWordFrequencyPercentage = 30
TopWordFrequencyPercentage /= 100

# 词云图片生成路径（当前目录下的 wordcloud_rectangle.png 文件）
PicSavePath = "./wordcloud_rectangle.png"

# jieba分词
seg = jieba.cut(text)

seg = " ".join(seg)
seg = seg.strip()

# 去除标点符号
seg = re.sub(r"[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:：。？、~@#￥%……&*（）]+", " ", seg)
# 只取中文
# seg = re.sub(r'[^\u4e00-\u9fa5]', ' ', seg)

# 转换为list
seg = seg.split(" ")

# 过滤空字符和None
seg = list(filter(None, seg))
# print(seg)

# 创建一个停用词列表
stopwords = stopwordslist()
# print(stopwords)

# 过滤停用词（列表解析）
seg = [v for v in seg if v not in stopwords]
# print(seg)

# 统计词频
word_counts = collections.Counter(seg)
# print(word_counts)
# print(math.ceil(len(word_counts) * 0.3))

# # 获取词频降序排列的前30%
# word_counts_top_50_percent = word_counts.most_common(math.ceil(len(word_counts) * 0.3))
# print(word_counts_top_50_percent)

# 生成词云
wc = WordCloud(
    # 限制词数（根据词频限制，计算个数，向上取整）
    max_words=math.ceil(len(word_counts) * TopWordFrequencyPercentage),
    # 设置背景宽
    width=500,
    # 设置背景高
    height=350,
    # 最大字体
    max_font_size=50,
    # 最小字体
    min_font_size=10,
    # 设置字体文件路径，不指定就会出现乱码。
    font_path='./MSYH.TTC',
    # 设置背景色
    background_color='white',
)

# 根据词频产生词云
wc.generate_from_frequencies(word_counts)

# 生成词云图片文件
wc.to_file(PicSavePath)
