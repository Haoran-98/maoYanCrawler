from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
from datetime import timedelta
import json
import visualization


# 获取数据
def get_data(url):
    # requests失败无法爬到数据
    # headers = {
    #     "User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
    #                           Chrome/101.0.4951.54 Safari/537.36"
    # }
    # response = requests.get(url, headers=headers)
    # if response.status_code == 200:
    #     print(response.text)
    #     return response.text
    
    browser_options = Options()
    browser = webdriver.Chrome(options=browser_options, executable_path='chromedriver')
    # headers = {"User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    #                          "Chrome/101.0.4951.54 Safari/537.36"}
    print("浏览器已创建")
    browser.get(url)
    text = browser.find_element_by_tag_name('pre').text
    time.sleep(1)
    browser.close()
    return text


# 处理数据
def parse_data(html):
    data = json.loads(html)['cmts']  # 将str转换为json
    comments = []
    for item in data:
        comment = {
            'id': item['id'],
            'nickName': item['nickName'],
            'cityName': item['cityName'] if 'cityName' in item else '',  # 处理cityName不存在的情况
            'content': item['content'].replace('\n', ' ', 10),  # 处理评论内容换行的情况
            'score': item['score'],
            'startTime': item['startTime']
        }
        comments.append(comment)
    return comments


# 存储数据，存储到文本文件
def save_to_txt():
    # 获取当前时间，从当前时间向前获取
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start_time = '2018-05-11 00:00:00'
    # while start_time > end_time:
    # 因为是演示，所以只爬取前10页的数据
    for i in range(10):
        url = 'https://m.maoyan.com/mmdb/comments/movie/248170.json?_v_=yes&offset=' + str(
            15 * i) + '&startTime=' + start_time.replace(' ', '%20')
        try:
            html = get_data(url)
            time.sleep(1)
        except Exception as e:
            time.sleep(3)
            html = get_data(url)
        else:
            time.sleep(1)
        comments = parse_data(html)
        print(comments)
        print("抓取第" + str(i + 1) + "页成功")
        start_time = comments[14]['startTime']  # 获得末尾评论的时间
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(
            seconds=-1)  # 转换为datetime类型，减1秒，避免获取到重复数据p
        start_time = datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S')  # 转换为str
        
        for item in comments:
            with open('comments.txt', 'a', encoding='utf-8') as f:
                f.write(str(item['id']) + ',' + item['nickName'] + ',' + item['cityName'] + ',' + item[
                    'content'] + ',' + str(item['score']) + ',' + item['startTime'] + '\n')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    save_to_txt()  # 爬虫
    name = 'comments.txt'
    visualization.word_cloud(name)  # 可视化词云
    visualization.funsloctions(name)  # 可视化地图和柱状图
    visualization.pie_chart(name)  # 可视化饼状图

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
