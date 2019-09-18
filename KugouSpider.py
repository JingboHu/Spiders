# -*- coding:utf-8 -*-

"""
爬取内容：酷狗排行榜前500的歌曲
具体为：排名情况、歌手、歌曲名、歌曲时长
"""
# 导入第三方库
import requests
import time
from bs4 import BeautifulSoup

# 请求头，伪装成浏览器，这里用的谷歌浏览器
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

# 定义一个获取信息函数
def get_info(url):
    data = requests.get(url,headers = headers)
    soup = BeautifulSoup(data.text,'lxml')

    # 解析排名
    ranks = soup.select('span.pc_temp_num')

    # 解析歌曲名和歌手名字,这两个信息是在一起的
    titles = soup.select('div.pc_temp_songlist > ul > li > a')

    # 解析歌曲时长
    timespans = soup.select('span.pc_temp_tips_r > span')

    for rank, title, timespan in zip(ranks,titles, timespans):
        # 如果歌手名字和歌曲名是以 - 分割的话，运行try下面的程序，否则运行except下面的程序
        # 这样写的目的是出现爬取错误时不至于程序停止
        # 在对结果进行时发现，有的地方歌手名字较多，且以‘、’分割
        try:
            data = {
                'rank':rank.get_text().strip(),
               # 'singer-song':title.get_text().strip(),
                'singer':title.get_text().split('-')[0],
                'song':title.get_text().split('-')[1],
                'timespan':timespan.get_text().strip()
            }
        except:
            data = {
                'rank': rank.get_text().strip(),
                'singer': title.get_text().split('、')[0:-1],
                'song': title.get_text().split('、')[-1],
                'timespan': timespan.get_text().strip()
            }
        # 获取信息并按字典格式打印出来
        print(data)

# 主函数
def main():
    # 构造要爬取的网页，字符串的格式化
    urls = ['https://www.kugou.com/yy/rank/home/{}-8888.html'.format(str(i)) for i in range(1,24)]

    # 利用get_info()函数，获取每一页网页的信息
    for url in urls:
        get_info(url)
        # 爬取完一页后等待1秒，防止爬取过快
        time.sleep(1)

# 程序主入口
if __name__ == '__main__':
    main()