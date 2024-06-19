import csv
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import xml.dom.minidom  # 处理包含浏览器版本信息的xml文件
import re


def del_and_create_dir(filename):
    # 判断文件是否存在，如果存在则删除文件
    filenamePath = os.path.join(os.getcwd(), "result", "comment", filename)
    # filenamePath = os.path.join("D:\study-code\spider\paper", "result", "comment",filename)  # 【bug:streamlit运行的过程中，其当前路径是工程路径，而不是该文件所在的路径。导致这里os.getcwd()获取定位失败】
    # 确保目录存在，如果不存在则创建
    os.makedirs(os.path.dirname(filenamePath), exist_ok=True)
    return filenamePath

def extract_time(comment_time):
    '''
    接受一个字符串comment_time作为输入，并返回提取到的时间数据
    :param comment_time:
    :return:
    '''
    pattern = r'\d{4}-\d{2}-\d{2}'
    matches = re.findall(pattern, comment_time)
    if matches:
        return matches[0]
    else:
        return None



def open_broswer(broswerType):
    """
    根据传入的浏览器类型参数来确定要打开的浏览器驱动路径
    """
    # 加载浏览器驱动
    firefor_driver = "geckodriver.exe"
    chrome_driver = "chromedriver.exe"
    edge_driver = "msedgedriver.exe"
    if broswerType == "Firefox" or broswerType == "FireFox" or broswerType == "firefox" or broswerType == "huohu" or broswerType == "火狐":
        path = os.getcwd() + "\\" + firefor_driver
    elif broswerType == "Chrome" or broswerType == "chrome" or broswerType == "guge" or broswerType == "谷歌":
        path = os.getcwd() + "\\" + chrome_driver
    else:
        path = os.getcwd() + "\\" + edge_driver
    return path


def get_MOOC(broswer, url, sum_page):
    # 设置超时时间为60秒
    timeout = 60

    # 创建Edge浏览器选项对象
    edge_options = Options()
    chrome_options = Options()
    # 启用无痕模式
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--ignore-ssl-errors=yes') # 添加参数以忽略SSL错误

    # 加载自动化测试驱动，让浏览器自动执行某些操作
    path = open_broswer(broswer)
    if path.endswith("geckodriver.exe"):
        driver = webdriver.Firefox(executable_path=path)  # 设置Firefox浏览器驱动路径
    elif path.endswith("chromedriver.exe"):
        service = Service(executable_path=path)  # selenium4 使用services设置chromedriver路径
        driver = webdriver.Chrome(options=chrome_options, service=service)
    else:
        driver = webdriver.Edge(options=edge_options)
    driver.maximize_window()
    driver.get(url)

    time.sleep(3)
    # 模仿点击查看课程评价的行为
    element = driver.find_element(By.ID, "review-tag-button")
    element.click()
    # print("********************************************************")
    '''
        模仿点击下一页功能，类名是ux-pager_btn ux-pager_btn__next，
        类名中的空格表示该元素属于多个类别，任意取其中一个就行，但是要保证其唯一性
    '''
    next_element = driver.find_element(By.CLASS_NAME, value="ux-pager_btn__next")
    time_flag = str(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))
    filename = time_flag + ".csv"
    filenamePath = del_and_create_dir(filename) # 返回的文件路径

    # 等待页面加载完成
    wait = WebDriverWait(driver, 10)

    with open(filenamePath, "a", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Comment', 'score', 'time_data'])  # 写入 CSV 文件的标题行
        for index in range(int(sum_page)):  # 循环遍历每一页的内容
            # 找到 class="ux-mooc-comment-course-comment_comment-list_item_body" 的 div 元素
            div_lists = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located(
                (By.CLASS_NAME, 'ux-mooc-comment-course-comment_comment-list_item_body')))

            for div_list in div_lists:
                # 获取div_list下的评论内容
                comment_text = div_list.find_element(By.CLASS_NAME,
                                                     "ux-mooc-comment-course-comment_comment-list_item_body_content").find_element(
                    By.TAG_NAME, "span").text
                # ==获取div_list下的打分内容==
                # 找到用户信息下的 <div class="star-point"> 标签
                star_point_div = div_list.find_element(By.CLASS_NAME, "star-point")
                # 找到该标签下的所有 <i> 标签
                star_icons = star_point_div.find_elements(By.TAG_NAME, "i")
                # 获取 <i> 标签的数量 ==评论得分
                comment_score = len(star_icons)
                # comment_score = div_list.find_element(By.CLASS_NAME,"ux-mooc-comment-course-comment_comment-list_item_body_user-info").find_element(By.TAG_NAME, "span").find_element(By.TAG_NAME, "div").find_element(By.CLASS_NAME,"star-point")
                # ==获取div_list下的打分时间==
                comment_time = div_list.find_element(By.CLASS_NAME,
                                                     "ux-mooc-comment-course-comment_comment-list_item_body_comment-info_time").text
                time_data = extract_time(comment_time)
                print("当前爬取到的数据：{}-{}-{}".format(comment_text, comment_score, time_data))
                writer.writerow([comment_text, comment_score, time_data])  # 将评论内容写入 CSV 文件
            next_element.click()  # 模拟点击下一页按钮，加载下一页的评价内容
            # time.sleep(3)  # 等待页面加载完成
    csvfile.close()  # 关闭文件
    driver.quit()  # 关闭浏览器驱动

    return filenamePath






