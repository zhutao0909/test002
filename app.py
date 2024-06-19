import streamlit as st
import pandas as pd
from draw import set_chinese_font, word_frequency_analysis, word_cloud, score_proportion, \
    plot_comment_frequency_by_month, TSNE_show, word_fre_draw
from utils import chinese_word_cut, vectorization_comment, KmeansAlgorithm

# 读取csv文件中的评论数据，这里简化为直接从上传的文件中读取
def read_comments_from_csv(uploaded_file):
    return pd.read_csv(uploaded_file)['comment'].tolist()

def main():
    st.title('MOOC在线课程评论分析')

    # 移除爬虫设置相关的全局变量初始化
    # ...

    # 选择页面
    page = st.sidebar.selectbox('选择页面', ['配置', '评论数据分析结果展示'])

    if page == '配置':
        st.header('KMeans算法模块设置')
        # 用户输入配置参数
        min_df = st.number_input('min_df数据大小', min_value=1, value=5)
        true_k = st.number_input('true_k数据大小', min_value=1, value=5)
        max_iter = st.number_input('max_iter数据大小', min_value=1, value=100)
        n_init = st.number_input('n_init数据大小', min_value=1, value=1)
        # 将用户配置保存到session_state，以便在分析页面使用
        st.session_state.min_df = min_df
        st.session_state.true_k = true_k
        st.session_state.max_iter = max_iter
        st.session_state.n_init = n_init

    elif page == '评论数据分析结果展示':
        st.header('评论数据分析结果展示')
        # 使用Streamlit的文件上传功能
        uploaded_file = st.file_uploader("请上传您的评论数据CSV文件", accept_multiple_files=False)
        if uploaded_file is not None:
            # 读取上传的CSV文件
            df = pd.read_csv(uploaded_file)
            st.session_state.data = df

            # 数据预处理
            st.session_state.data['split'] = st.session_state.data['Comment'].apply(chinese_word_cut)
            set_chinese_font()  # 设置中文展示字体

            # 数据分析和可视化
            # ...

            # 聚类分析
            # ...

            # 展示分析结果
            # ...

            # 例如，展示词汇频率分析和词云
            words = word_frequency_analysis(st.session_state.data)
            st.write(word_fre_draw(words, 'All'))
            st.write(word_cloud(words))

            # 展示评分占比情况和发布时间统计
            st.write(score_proportion(st.session_state.data))
            st.write(plot_comment_frequency_by_month(st.session_state.data))

            # 向量化和聚类分析
            vectorizer, tfidf_weight = vectorization_comment(st.session_state.min_df, st.session_state.data)
            model = KmeansAlgorithm(st.session_state.data, tfidf_weight, st.session_state.max_iter, st.session_state.n_init)
            # 使用T-SNE算法展示聚类结果
            st.write(TSNE_show(tfidf_weight, model))

            # 输出每个簇的元素
            print_terms_perCluster(st.session_state.true_k, model, st.session_state.data)

if __name__ == '__main__':
    main()
