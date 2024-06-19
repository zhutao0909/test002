import codecs
import re
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.cluster import KMeans

# 对评论数据进行预处理
def chinese_word_cut(mytext):
    # 文本预处理 ：去除一些无用的字符只提取出中文出来
    new_data = re.findall('[\u4e00-\u9fa5]+', mytext, re.S)
    new_data = " ".join(new_data)

    # 文本分词
    seg_list_exact = jieba.cut(new_data, cut_all=True)
    result_list = []
    # 加载停用词库
    with open(r'cn_stopwords.txt', encoding='utf-8') as f:  # 可根据需要打开停用词库，然后加上不想显示的词语
        stop_words = set()
        for i in f.readlines():
            stop_words.add(i.replace("\n", ""))  # 去掉读取每一行数据的\n
    # 去除停用词
    for word in seg_list_exact:
        if word not in stop_words and len(word) > 1:
            result_list.append(word)
    return " ".join(result_list)

def print_FeatureVector_textContent(word,tfidf_weight):
    # 打印特征向量文本内容
    resName = "Tfidf_Result.txt"
    result = codecs.open(resName, 'w', 'utf-8')
    for j in range(len(word)):
        result.write(word[j] + ' ')
    result.write('\r\n\r\n')
    #每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    for i in range(len(tfidf_weight)):
        for j in range(len(word)):
            result.write(str(tfidf_weight[i][j]) + ' ')
        result.write('\r\n\r\n')
    result.close()

def KmeansAlgorithm(data,tfidf_weight,max_iter_value=100,n_init_value=1):
    '''
    :param data:
    :param tfidf_weight:
    :param max_iter_value: 算法的最大迭代次数 ,默认值100
    :param n_init_value: 初始化簇中心的次数,默认值1
    :return:
    '''
    # 使用K-means聚类算法对评论数据进行情感分类
    print( 'Start Kmeans:')
    true_k = 5  # 假设我们有五个情感类别
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=max_iter_value, n_init=n_init_value) # init：指定了初始化簇中心的方法（一种智能的初始化方法，有助于避免陷入局部最小值）、max_iter：算法的最大迭代次数、n_init：初始化簇中心的次数
    model.fit(tfidf_weight) # 使用TF-IDF权重作为特征，对K均值模型进行训练。模型将会对这些特征进行聚类，将文档划分到不同的簇中

    # 打印出各个簇的中心点
    print("中心点坐标：")
    print(model.cluster_centers_) # 打印出各个簇的中心点坐标
    for index, label in enumerate(model.labels_, 1): # 对于每个样本，打印其索引以及所属的簇的标签
        print("index: {}, label: {}".format(index, label))
    # 样本距其最近的聚类中心的平方距离之和，用来评判分类的准确度，值越小越好
    # k-means的超参数n_clusters可以通过该值来评估
    print("效果评估值：")
    print("inertia: {}".format(model.inertia_)) # 打印出样本距其最近的聚类中心的平方距离之和

    # 将聚类的结果保存为excel文件
    data['label'] = model.labels_
    return model


def print_terms_perCluster(model,data):
    # 输出每个簇的元素
    true_k = 5  # 假设我们有五个情感类别
    print("Top terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = model.labels_
    # terms = vectorizer.get_feature_names_out()
    list = []
    for i in range(true_k):
        print("Cluster %d:" % i)
        #for ind in order_centroids[i, :10]:
        for ind in order_centroids[i]:
            # print(' %s' % terms[ind])
            # list.append(terms[ind])
            list.append(data['split'][ind])
        print(list)
        list = []



def vectorization_comment(min_df_value,data):
    '''
    # 利用TF-IDF对评论数据进行向量化
    :param min_df_value:
    :param data:
    :return:
    '''
    # -----评论向量化------------
    # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频(忽略在文档中出现次数低于 5 次的词语)
    vectorizer = CountVectorizer(min_df= min_df_value)
    # 该类会统计每个词语的tf-idf权值
    transformer = TfidfTransformer()
    # 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(data['split']))
    # 获取词袋模型中的所有词语
    word = vectorizer.get_feature_names_out()  # get_feature_names
    # 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
    tfidf_weight = tfidf.toarray()  # 特征矩阵，每一行代表一个文档，每一列代表一个特征

    return [vectorizer,tfidf_weight]




