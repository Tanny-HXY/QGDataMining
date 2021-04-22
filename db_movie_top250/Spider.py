import random
import pymysql
import requests
from lxml import etree
import time

# 简单的规避反爬虫
headers = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.39"}


def getmovie_urls(index):
    # 分析网页后发现每一页只有start后面的数字改变
    initialurl = "https://movie.douban.com/top250?start="
    url = initialurl + str(index * 25)
    html = requests.get(url, headers=headers).text
    # 选取每部电影的URL才能爬到剧情简介
    selector = etree.HTML(html)
    urls = selector.xpath('//li/div/div/a/@href')
    return urls


def getdata(url):
    html = requests.get(url=url, headers=headers).text
    selector = etree.HTML(html)
    # 排名
    ranking = selector.xpath("//span[@class='top250-no']/text()")
    # 电影名
    name = selector.xpath("//h1/span[1]/text()")
    # 上映年份
    year = selector.xpath("//h1/span[2]/text()")
    # 导演
    director = selector.xpath("//div[@id='info']/span[1]/span[@class='attrs']/a/text()")
    # 得分
    score = selector.xpath("//div[@class='rating_self clearfix']/strong/text()")
    # 参评人数
    number = selector.xpath("//span[@property='v:votes']/text()")
    # 剧情简介
    synopsis = selector.xpath("//span[@property='v:summary']/text()")
    synopsis = [x.strip() for x in synopsis]
    # 片长
    duration = selector.xpath("//span[@property='v:runtime']/text()")

    return zip(ranking, name, year, director, score, number, synopsis, duration)


def savedata(data):
    try:
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='LOVEHXY1228',
                             db='douban')
        cursor = db.cursor()

        # 创建表db_movie_top250
        # sql_create_table = """create table db_movie_top250 (
        #     Ranking char(10),
        #     Title varchar(255),
        #     Release_year char (8),
        #     Director TEXT (255),
        #     Score char (8),
        #     Raters_num varchar (40),
        #     Synopsis  text (255),
        #     Duration varchar (40)
        # )"""
        # cursor.execute(sql_create_table)
        sql_insert = """insert into db_movie_top250 (Ranking, 
        Title, Release_year, Director, Score, Raters_num, Synopsis,Duration)
        values (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql_insert, data)
        # 提交
        db.commit()
        db.close()
        print("insert success")
    except:
        # 如果发生错误则回滚数据
        print("error")
        db.rollback()


num = 0
for i in range(10):
    movie_urls = getmovie_urls(i)
    for movie_url in movie_urls:
        movie_datas = getdata(movie_url)
        for movie_data in movie_datas:
            num += 1
            savedata(movie_data)
            print('第' + str(num) + '条电影信息保存完毕！')
            # 加个随机时间间隔爬取
            time.sleep(random.random())
