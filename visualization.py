# coding=utf-8
# 导入jieba模块，用于中文分词
import jieba
# 导入matplotlib，用于生成2D图形
import matplotlib.pyplot as plt
# 导入wordcount，用于制作词云图
from wordcloud import WordCloud
import os


def word_cloud(name):
    # 获取所有评论
    comments = []
    with open(name, mode='r', encoding='utf-8') as f:
        rows = f.readlines()
        for row in rows:
            comment = row.split(',')[3]
            if comment != '':
                comments.append(comment)
    
    # 设置分词
    comment_after_split = jieba.cut(str(comments), cut_all=False)  # 非全模式分词，cut_all=false
    words = " ".join(comment_after_split)  # 以空格进行拼接
    # 设置词云参数，参数分别表示：画布宽高、背景颜色、字体、最大词的字体大小
    wc = WordCloud(width=1024, height=768, background_color='white', font_path='STKAITI.TTF', max_font_size=400,
                   random_state=50)
    # 将分词后数据传入云图
    wc.generate_from_text(words)
    plt.imshow(wc)
    plt.axis('off')  # 不显示坐标轴
    plt.show()
    # 保存结果到本地
    wc.to_file('wc.jpg')


# 导入Style类，用于定义样式风格
# from pyecharts import Style
# 导入Geo组件，用于生成地理坐标类图
from pyecharts.charts import Geo
import json
# 导入Geo组件，用于生成柱状图
from pyecharts.charts import Bar
# 导入Counter类，用于统计值出现的次数
from collections import Counter
from pyecharts.globals import ChartType, ThemeType, CurrentConfig, GeoType


# 处理地名数据，解决坐标文件中找不到地名的问题
def handle(cities):
    # print(len(cities), len(set(cities)))
    
    # 获取坐标文件中所有地名
    data = None
    project_path = os.path.abspath(os.path.dirname(__file__))
    with open(r'C:\Users\77481\.conda\envs\pytorch\Lib\site-packages\pyecharts\datasets\city_coordinates.json',
              mode='r', encoding='utf-8') as f:
        data = json.loads(f.read())  # 将str转换为json
    
    # 循环判断处理
    data_new = data.copy()  # 拷贝所有地名数据
    for city in set(cities):  # 使用set去重
        # 处理地名为空的数据
        if city == '':
            while city in cities:
                cities.remove(city)
        count = 0
        for k in data.keys():
            count += 1
            if k == city:
                break
            if k.startswith(city):  # 处理简写的地名，如 达州市 简写为 达州
                # print(k, city)
                data_new[city] = data[k]
                break
            if k.startswith(city[0:-1]) and len(city) >= 3:  # 处理行政变更的地名，如县改区 或 县改市等
                data_new[city] = data[k]
                break
        # 处理不存在的地名
        if count == len(data):
            while city in cities:
                cities.remove(city)
    
    # 写入覆盖坐标文件
    with open(r'C:\Users\77481\.conda\envs\pytorch\Lib\site-packages\pyecharts\datasets\city_coordinates.json',
              mode='w',
              encoding='utf-8') as f:
        f.write(json.dumps(data_new, ensure_ascii=False))  # 将json转换为str


# 数据可视化
def funsloctions(name):
    # 获取评论中所有城市
    cities = []
    with open(name, mode='r', encoding='utf-8') as f:
        rows = f.readlines()
        for row in rows:
            city = row.split(',')[2]
            if city != '':  # 去掉城市名为空的值
                cities.append(city)
    # 对城市数据和坐标文件中的地名进行处理
    # handle(cities)
    # 统计每个城市出现的次数
    handle(cities)
    data = Counter(cities).most_common()  # 使用Counter类统计出现的次数，并转换为元组列表
    print(data)
    
    # 定义样式
    # style = Style(
    #     title_color='#fff',
    #     title_pos='center',
    #     width=1200,
    #     height=600,
    #     background_color='#404a59'
    # )
    
    # 根据城市数据生成地理坐标图
    # geo = Geo('《一出好戏》粉丝位置分布', '数据来源：猫眼电影数据')
    g = Geo(init_opts=opts.InitOpts(width="1200px",
                                    height="900px", theme=ThemeType.PURPLE_PASSION),
            is_ignore_nonexistent_coord=True)  # 地理初始化
    g.add_schema(maptype='china',
                 label_opts=opts.LabelOpts(is_show=True))
    g.add('门店数量',
          data_pair=data,
          type_=GeoType.EFFECT_SCATTER,
          symbol_size=8,
          )
    g.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    g.set_global_opts(title_opts=opts.TitleOpts(title='粉丝位置分布'),visualmap_opts=opts.VisualMapOpts(max_=10000,is_piecewise=True,pieces=[
                     {"max": 5, "min": 0, "label": "0-5", "color": "#708090"},
                     {"max": 10, "min": 6, "label": "5-10", "color": "#00FFFF"},
                     {"max": 20, "min": 11, "label": "10-20", "color": "#FF69B4"},
                     {"max": 40, "min": 21, "label": "20-40", "color": "#FFD700"},
                     {"max": 80, "min": 41, "label": "40-80", "color": "#FF0000"},]), legend_opts=opts.LegendOpts(is_show=False))
    # 分段  添加图例注释和颜色
    g.render('粉丝位置分布-地理坐标图.html')
    
    # 根据城市数据生成柱状图
    data_top10 = Counter(cities).most_common(10)  # 返回出现次数最多的20条
    bar = Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT,animation_opts=opts.AnimationOpts(animation_delay=2000, animation_easing="elasticOut")))
    cities_top10 = []
    fans_count = []
    for item in data_top10:
        cities_top10.append(item[0])
        dict_value = {"value": item[1]}
        fans_count.append(dict_value)
    print(cities_top10)
    bar.add_xaxis(cities_top10)
    bar.add_yaxis("粉丝数量", fans_count,stack="stack0", gap="0%",itemstyle_opts=opts.ItemStyleOpts(color="#00CD96"))
    bar.set_global_opts(xaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(rotate=-15)),toolbox_opts=opts.ToolboxOpts(), title_opts=opts.TitleOpts(title="《一出好戏》粉丝来源排行TOP20"))
    bar.render("粉丝来源排行-柱状图.html")


# coding=utf-8
# 导入Pie组件，用于生成饼图
from pyecharts.charts import Pie
from pyecharts import options as opts


def pie_chart(name):
    # 获取评论中所有评分
    rates = []
    with open(name, mode='r', encoding='utf-8') as f:
        rows = f.readlines()
        for row in rows:
            rates.append(row.split(',')[4])
    # 定义星级，并统计各星级评分数量
    data = {"五星": rates.count('5') + rates.count('4.5'), "四星": rates.count('4') + rates.count('3.5'),
            "三星": rates.count('3') + rates.count('2.5'), "二星": rates.count('2') + rates.count('1.5'),
            "一星": rates.count('1') + rates.count('0.5')}
    attr = ["五星", "四星", "三星", "二星", "一星"]
    value = [
        rates.count('5') + rates.count('4.5'),
        rates.count('4') + rates.count('3.5'),
        rates.count('3') + rates.count('2.5'),
        rates.count('2') + rates.count('1.5'),
        rates.count('1') + rates.count('0.5')
    ]
    pie = Pie(init_opts=opts.InitOpts(theme='light',
                                      width='1000px',
                                      height='600px'))
    # '评分星级比例', title_pos='center', width=900
    
    pie.add("", [list(z) for z in zip(attr, value)],
            radius=["40%", "75%"], rosetype='area')
    pie.set_global_opts(title_opts=opts.TitleOpts(title='评分星级比例',pos_left="center",
            pos_top="20",),tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
        ),legend_opts=opts.LegendOpts(type_="scroll", pos_left="90%", orient="vertical"),)
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    pie.render('评分.html')
