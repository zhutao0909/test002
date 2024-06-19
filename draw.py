import re
from collections import Counter
import streamlit as st
import pandas as pd
from sklearn.manifold import TSNE
from wordcloud import WordCloud
import jieba
from matplotlib import pyplot as plt


def set_chinese_font():
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

def word_fre_draw(a, str):
    a_counts = Counter(a)
    top_30_a = a_counts.most_common(30)
    words, frequencies = zip(*top_30_a)

    # 绘制水平柱状图
    # plt.figure(figsize=(10, 15))  # 设置宽、高
    fig = plt.figure(figsize=(15, 10))  # 设置宽、高
    plt.barh(words, frequencies, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title('Top 30 Words in Comment Messages for {0}'.format(str))
    # plt.show()
    st.pyplot(fig)  # 使用Streamlit的绘图功能显示图像

def is_chinese_word(word):
    for char in word:
        if not re.match(r'[\u4e00-\u9fff]', char):
            return False
    return True

def correct(a, stop_words):
    b = []
    for word in a:
        if len(word) > 1 and is_chinese_word(word) and word not in stop_words:
            b.append(word)
    return b



# 词汇频率分析
def word_frequency_analysis(df):
    all_text = ' '.join(df['Comment'].astype(str))

    words = list(jieba.cut(all_text, cut_all=False))

    with open(r'cn_stopwords.txt', encoding='utf-8') as f:  # 添加屏蔽词汇
        con = f.readlines()
        stop_words = set()  # 集合可以去重
        for i in con:
            i = i.replace("\n", "")  # 去掉读取每一行数据的\n
            stop_words.add(i)

    Words = correct(words, stop_words)
    words_space_split = ' '.join(Words)

    # word_fre_draw(Words, 'All')   # 词汇频率分析还是通过其他函数进行间接调用

    return words_space_split



def word_cloud(words_space_split):
    wordcloud = WordCloud(font_path='‪C:\Windows\Fonts\STCAIYUN.TTF',
                          width=800, height=600,
                          background_color='white',
                          max_words=200,
                          max_font_size=100,
                          ).generate(words_space_split)

    # plt.figure(figsize=(10, 8))
    fig = plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    # plt.show()
    st.pyplot(fig)  # 使用Streamlit的绘图功能显示图像

# 爬取课程评论评分的占比情况分析
def score_proportion(df):
    # 统计各个分数的数量
    score_counts = df['score'].value_counts()
    # 绘制饼状图
    # plt.figure(figsize=(8, 6))
    fig = plt.figure(figsize=(8, 6))
    plt.pie(score_counts, labels=score_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Score Distribution')
    plt.axis('equal')  # 使饼状图为正圆形
    # plt.show()
    st.pyplot(fig)  # 使用Streamlit的绘图功能显示图像


def plot_comment_frequency_by_month(df):
    '''
    评论发布时间频率柱状图
    :param df:
    :return:
    '''
    # 提取年份和月份并合并为新的列
    df['year_month'] = pd.to_datetime(df['time_data']).dt.to_period('M')

    # 按月份统计评论数量
    chat_frequency = df['year_month'].value_counts().sort_index()

    # 设置图形大小
    # plt.figure(figsize=(10, 10))
    fig = plt.figure(figsize=(14, 6))  # 设置图形宽度为12英寸，高度为6英寸

    # 绘制柱状图
    chat_frequency.plot(kind='bar', color='#DF9F9B')

    # 添加文本说明
    total_messages = len(df)
    start_month = df['year_month'].min()
    end_month = df['year_month'].max()
    plt.text(0.5, 0.95, '消息总数：{0}条'.format(total_messages), transform=plt.gca().transAxes, ha='left', va='top',
             fontsize=10, color='black')
    plt.text(0.5, 0.9, '起止时间：{0} --- {1}'.format(start_month, end_month), transform=plt.gca().transAxes, ha='left',
             va='top', fontsize=10, color='black')

    # 设置图表标题和坐标轴标签
    plt.xlabel('Year-Month')
    plt.ylabel('Frequency')
    plt.title('Comment Frequency by Month')

    # 显示图例
    plt.legend(['Frequency'], loc='upper right')

    # 显示图形
    plt.xticks(rotation=45, fontsize=8)  # 旋转日期标签，使其更易读[调整字体大小]
    plt.tight_layout()  # 调整布局以避免标签重叠
    # plt.show()
    st.pyplot(fig)  # 使用Streamlit的绘图功能显示图像



def TSNE_show(tfidf_weight,model):
    # 使用T-SNE算法，对权重进行降维，准确度比PCA算法高，但是耗时长
    tsne = TSNE(n_components=2)
    decomposition_data = tsne.fit_transform(tfidf_weight)

    x = []
    y = []

    for i in decomposition_data:
        x.append(i[0])
        y.append(i[1])

    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes()
    plt.scatter(x, y, c=model.labels_, marker="x")
    plt.xticks(())
    plt.yticks(())
    st.pyplot(fig)  # 使用Streamlit的绘图功能显示图像
    # plt.show()
