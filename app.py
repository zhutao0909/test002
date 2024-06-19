import streamlit as st
import pandas as pd
from draw import set_chinese_font, word_frequency_analysis, word_cloud, score_proportion, \
    plot_comment_frequency_by_month, TSNE_show
from utils import chinese_word_cut, vectorization_comment, KmeansAlgorithm

# 注意：假设 draw 和 utils 模块中的函数已经调整为可以通过Streamlit上传的文件进行操作

# 主函数
def main():
    st.title('MOOC在线课程评论分析')

    # 移除爬虫设置相关的全局变量
    # st.session_state.url, st.session_state.num_pages, st.session_state.browser ...

    # 系统过程参数设置
    st.session_state.filenamePath = None  # 操作文件地址
    st.session_state.data = None  # 文件对象
    st.session_state.model = None  # 模型对象
    st.session_state.vectorizer = None  # 向量化对象

    # 移除爬虫按钮和相关逻辑
    # if st.button('确认'):
    #     st.session_state.filenamePath = get_MOOC(...)

    # 选择页面
    page = st.sidebar.selectbox('选择页面', ['配置', '评论数据分析结果展示'])

    if page == '配置':
        st.header('KMeans算法模块设置')
        # 配置min_df, true_k, max_iter, n_init等参数
        # 这部分代码与您原始代码中的配置页面类似，但不需要爬虫设置

    elif page == '评论数据分析结果展示':
        st.header('评论数据分析结果展示')
        # 使用Streamlit的文件上传功能
        uploaded_file = st.file_uploader("请上传您的评论数据CSV文件", accept_multiple_files=False)
        if uploaded_file is not None:
            # 读取上传的CSV文件
            df = pd.read_csv(uploaded_file)
            st.session_state.filenamePath = uploaded_file.name  # 更新文件名
            st.session_state.data = df

            # 以下代码与您原始代码中的分析页面类似
            # 对评论数据进行预处理
            st.session_state.data['split'] = st.session_state.data['Comment'].apply(chinese_word_cut)
            set_chinese_font()  # 设置中文展示字体

            # 数据可视化统计分析
            # ...

            # 评论向量化
            # ...
            # 使用K-means聚类算法
            # ...

            # 展示结果
            # ...

if __name__ == '__main__':
    main()
