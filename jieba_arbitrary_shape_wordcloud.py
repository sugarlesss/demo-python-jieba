import logging
import collections
import re
import math
from random import randint

import jieba
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator

from PIL import Image
import numpy as np

jieba.setLogLevel(logging.INFO)


# 创建停用词列表
def stopwordslist():
    # 按行读入
    stopwords = [line.strip() for line in open('chinsesstop.txt', encoding='UTF-8').readlines()]

    # 分割为单个字符（列表解析）
    stopwords = [k for s in stopwords for k in s]
    return stopwords


# 自定义颜色函数（在绘制词云图时发现有的字颜色为黄色导致看不清因此需要修改整个词云图的色调为冷色调 蓝绿色）
def random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None,
                      random_state=None):
    # what is HSL? https://baike.baidu.com/item/HSL/1443144?fr=aladdin
    H = randint(120, 250)
    S = int(100.0 * 255.0 / 255.0)
    L = int(100.0 * float(randint(60, 120)) / 255.0)
    return "hsl({}, {}%, {}%)".format(H, S, L)


# # 指定字符串方式
# text = "collections在python官方文档中的解释是High-performance container datatypes，直接的中文翻译解释高性能容量数据类型。它总共包含五种数据类型"

# 文件读取方式
f = open("./article.txt", "r", encoding="utf-8")
text = f.read()
f.close()

# 生成词云的词频限制，选取前30%
TopWordFrequencyPercentage = 30
TopWordFrequencyPercentage /= 100

# 词云图片生成路径（当前目录下的 wordcloud_arbitrary_shape.png 文件）
PicSavePath = "./wordcloud_arbitrary_shape.png"

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

# 词云形状
mask = np.array(Image.open("./background1.png"))
# 根据图片颜色设置词云颜色(如果背景图片是纯色背景会报 NotImplementedError: Gray-scale images TODO 错误)
bg_color_func = ImageColorGenerator(mask)

# 生成词云
wc = WordCloud(
    # 词云形状
    mask=mask,
    # 限制词数（根据词频限制，计算个数，向上取整）
    max_words=math.ceil(len(word_counts) * TopWordFrequencyPercentage),
    # 设置图片宽度（单位：像素）
    width=500,
    # 设置图片高度（单位：像素）
    height=350,
    # 最大字体
    max_font_size=50,
    # 最小字体
    min_font_size=10,
    # 字体文件路径，不指定就会出现乱码。（windows系统字体文件路径：C:\Windows\Fonts，可以从这里拷贝出来）
    font_path='./MSYH.TTC',
    # 设置背景色
    background_color='white',
    # 颜色模式（默认为RBG）当参数为“RGBA”并且background_color为None时，背景为黑色
    mode='RGBA',

    # 词语水平方向排版出现的频率，默认 0.9 （所以词语垂直方向排版出现频率为 0.1 ）
    prefer_horizontal=0.9,
    # 按照比例进行放大画布，如设置为1.5，则长和宽都是原来画布的1.5倍
    scale=1,
    # 词频和字体大小的关联性
    relative_scaling=0.5,
    # 生成新颜色的函数（默认为None）
    # color_func=None,
    color_func=bg_color_func,
    # color_func=random_color_func,
    # 给每个单词随机分配颜色，若指定color_func，则忽略该方法
    colormap=None,
    # colormap='pink',
)

# 根据词频产生词云
wc.generate_from_frequencies(word_counts)

# 生成词云图片文件
wc.to_file(PicSavePath)
