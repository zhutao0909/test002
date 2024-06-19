import streamlit as st
import pandas as pd
from utils import chinese_word_cut, vectorization_comment, KmeansAlgorithm
from draw import set_chinese_font, word_frequency_analysis, word_cloud, score_proportion, \
    plot_comment_frequency_by_month, TSNE_show

# 确保 utils 和 draw 文件在同一个目录下，或者在 Python 的搜索路径中

def main():
    st.title('MOOC在线课程评论分析及可视化')

    # 让用户上传文件
    uploaded_file = st.file_uploader("请上传本地爬取的评论数据CSV文件", accept_multiple_files=False)
    
    if uploaded_file is not None:
        # 读取CSV文件
        data = pd.read_csv(uploaded_file)
        
        # 设置中文字体
        set_chinese_font()

        # 数据预处理
        data['split'] = data['Comment'].apply(chinese_word_cut)

        # 数据分析和可视化
        st.header('词汇频率分析')
        words_space_split = word_frequency_analysis(data)
        st.write(words_space_split)

        st.header('词云展示')
        word_cloud_image = word_cloud(words_space_split)
        st.image(word_cloud_image, caption='词云', use_column_width=True)

        st.header('评分占比情况分析')
        score_proportion_image = score_proportion(data)
        st.pyplot(score_proportion_image)

        st.header('评论发布时间统计')
        comment_frequency_image = plot_comment_frequency_by_month(data)
        st.pyplot(comment_frequency_image)

        # 向量化和聚类分析
        st.header('K-means聚类分析')
        vectorizer, tfidf_weight = vectorization_comment(min_df=5, data=data['split'])
        model = KmeansAlgorithm(data=data, tfidf_weight=tfidf_weight)

        # 展示聚类结果
        st.header('T-SNE降维展示')
        tsne_image = TSNE_show(tfidf_weight, model)
        st.pyplot(tsne_image)

if __name__ == '__main__':
    main()
