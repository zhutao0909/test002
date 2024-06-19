import streamlit as st
import pandas as pd
import os

# 导入其他必要的模块和函数
from utils import chinese_word_cut, vectorization_comment, KmeansAlgorithm
from draw import set_chinese_font, word_frequency_analysis, word_cloud, score_proportion, \
    plot_comment_frequency_by_month, TSNE_show

# 读取csv文件中的评论数据
def read_comments_from_csv(uploaded_file):
    # 读取上传文件中的评论数据
    return pd.read_csv(uploaded_file)

# 主函数
def main():
    st.title('MOOC在线课程评论分析')

    # 页面设置
    page = st.sidebar.selectbox('选择页面', ['评论数据分析结果展示'])

    if page == '评论数据分析结果展示':
        st.header('评论数据分析结果展示')

        # 用户上传CSV文件
        uploaded_file = st.file_uploader("请上传你的CSV文件", type=["csv"])
        if uploaded_file is not None:
            commentPath = uploaded_file.name
            data = read_comments_from_csv(uploaded_file)
            
            # 数据预处理
            data['split'] = data['Comment'].apply(chinese_word_cut)
            st.session_state.data = data

            # 数据可视化
            set_chinese_font()  # 设置中文展示字体

            # 词汇频率分析
            words_space_split = word_frequency_analysis(data)
            st.write('词汇频率分析:')
            word_fre_draw(words_space_split.split(), 'All')

            # 词云制作
            st.write('词云:')
            word_cloud(words_space_split)

            # 评分占比情况分析
            st.write('评分占比情况:')
            score_proportion(data)

            # 发布时间统计
            st.write('发布时间统计:')
            plot_comment_frequency_by_month(data)

            # 评论向量化
            vectorizer, tfidf_weight = vectorization_comment(st.session_state.min_df, data)

            # 使用K-means聚类算法对评论数据进行情感分类
            model = KmeansAlgorithm(data, tfidf_weight, st.session_state.max_iter, st.session_state.n_init)

            # T-SNE降维展示
            st.write('T-SNE降维展示:')
            TSNE_show(tfidf_weight, model)

            # 输出每个簇的元素
            print_terms_perCluster(model, data)

if __name__ == '__main__':
    main()
