#! /usr/bin/python3
# -*- coding:utf-8 -*-
# Copyright: 2019/4/24. All Rights Reserved.
# File: GetWeatherInfos.py 2019/4/24 20:08
# Author: Hu Jingbo
# Email: hujingbo16@163.com

import requests
from datetime import datetime
from bs4 import BeautifulSoup
import itchat
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import city_dict
import yaml
import re

class getWeather:

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    dict_channel_name = {1:'one一个',2:'词霸(每日英语)'}

    def __init__(self):
        self.girlfriend_list,self.alarm_hour,self.alarm_minute,self.dict_channel = self.get_init_data()

    def get_init_data(self):
        '''
        初始化基础数据
        :return:
        '''
        with open('_config','r',encoding='utf-8') as f:
            config = yaml.safe_load(f)

        alarm_time = config.get('alarm_time').strip()
        init_msg = f"每天定时发送时间：{alarm_time}\n"

        dict_channel = config.get('dict_channel',1)
        init_msg += f"格言获取渠道：{self.dict_channel_name.get(dict_channel,'无')}\n"

        girlfriend_list = []
        girlfriend_infos = config.get('girlfriend_infos')

        for girlfriend in girlfriend_infos:
            girlfriend.get('wechat_name').strip()
            # 根据城市名称获取城市编号，用于查询天气。
            # 查看支持的城市为; http://cdn.sojson.com/_city.json
            city_name = girlfriend.get('city_name').strip()
            city_code = city_dict.city_dict.get(city_name)

            if not city_code:
                print('您输入的城市无法获取到天气信息')
                break

            girlfriend['city_code'] = city_code
            girlfriend_list.append(girlfriend)

            print_msg = f"女朋友的微信昵称：{girlfriend.get('wechat_name')}\n\t女友所在城市名称：{girlfriend.get('city_name')}\n\t" \
                f"在一起的第一天日期：{girlfriend.get('start_date_together')}\n\t最后一句为：{girlfriend.get('sweet_words')}\n"

            init_msg += print_msg

        print(u"*" * 50)
        print(init_msg)

        hour,minute = [int(x) for x in alarm_time.split(':')]
        return girlfriend_list,hour,minute,dict_channel

    def is_online(self,auto_login=False):
        '''
        判断是否还在线,
        :param auto_login:True,如果掉线了则自动登录。
        :return: True ，还在线，False 不在线了
        '''

        def online():
            '''
            通过获取好友信息，判断用户是否还在线
            :return: True,还在线，False 不在线了
            '''
            try:
                if itchat.search_friends():
                    return True
            except:
                return False
            return True

        if online():
            return True

        # 仅仅判断是否在线
        if not auto_login:
            return online()

        # 登陆，尝试 5 次
        for _ in range(5):
            # 命令行显示登录二维码
            # itchat.auto_login(enableCmdQR=True)
            itchat.auto_login(True)
            if online():
                print('登录成功')
                return True
        else:
            print('登录成功')
            return False

    def run(self):
        '''
        主运行入口
        :return:
        '''
        # 自动登录
        if not self.is_online(auto_login=True):
            return
        for girlfriend in self.girlfriend_list:
            wechat_name = girlfriend.get('wechat_name')
            friends = itchat.search_friends(name=wechat_name)
            if not friends:
                print('昵称错误')
            name_uuid = friends[0].get('UserName')
            girlfriend['name_uuid'] = name_uuid

        # 定时任务
        scheduler = BlockingScheduler()
        # 每天7点左右给对象发送每日一句
        scheduler.add_job(self.start_today_info,'cron',hour=self.alarm_hour,minute=self.alarm_minute)
        # 每隔两分钟发送一条数据用于测试
        # scheduler.add_job(self.start_today_info,'intervial',seconds=30)
        scheduler.start()

        itchat.run(True)

    def start_today_info(self,is_test=False):
        '''
        每日定时开始处理
        :param is_test: 测试标志，当为True时，不发生微信消息，仅仅获取数据
        :return:
        '''
        print("*" * 50)
        print('获取相关信息...')

        if self.dict_channel == 1:
            dict_msg = self.get_dict_info()
        elif self.dict_channel == 2:
            dict_msg = self.get_ciba_info()
        else:
            dict_msg = ''

        for girlfriend in self.girlfriend_list:
            city_code = girlfriend.get('city_code')
            start_date_together = girlfriend.get('start_date_together')
            sweet_words = girlfriend.get('sweet_words')

            today_msg = self.get_today_weather_info(dict_msg,city_code=city_code,start_date_together=start_date_together,sweet_words=sweet_words)

            name_uuid = girlfriend.get('name_uuid')
            wechat_name = girlfriend.get('wechat_name')

            print(f'给{wechat_name}发送的内容是:\n{today_msg}')

            if not is_test:
                if self.is_online(auto_login=True):
                    itchat.send(today_msg,toUserName=name_uuid)
                    print('发送成功...\n')
                # 防止信息过快
                time.sleep(5)

        print('发送完成...\n')
        itchat.run(True)

    def isJson(self,resp):
        '''
        判断数据是否能被 Json 化。 True 能，False 否。
        :param resp:
        :return:
        '''
        try:
            resp.json()
            return True
        except:
            return False

    def get_dict_info(self):
        '''
        获取格言信息（从『一个。one』获取信息 http://wufazhuce.com/）
        :return: str 一句格言或者短语
        '''
        print('获取格言信息...')
        user_url = 'http://wufazhuce.com/'
        resp = requests.get(user_url,headers=self.headers)
        soup_texts = BeautifulSoup(resp.text,'lxml')
        # [one 一个] 中的每日一句
        every_msg = soup_texts.find_all('div',class_ = 'fp-one-cita')[0].find('a').text
        return every_msg + '\n'

    def get_ciba_info(self):
        '''
        从词霸中获取每日一句，带英文。
        :return:
        '''
        resp = requests.get('http://open.iciba.com/dsapi')
        if resp.status_code == 200 and self.isJson(resp):
            contentJson = resp.json()
            content = contentJson.get('content')
            note = contentJson.get('note')
            # print(f"{content}\n{note})
            return f"{content}\n{note}"
        else:
            print('没有获取到数据')
            return None

    def get_seven_day_weather_info(self):
        # future_seven_day_weather_url = f'http://www.nmc.cn/publish/forecast/ASH/shanghai.html'
        future_seven_day_weather_url = 'http://www.nmc.cn/publish/forecast/AHB/wuhan.html'
        html = requests.get(future_seven_day_weather_url, headers=self.headers)

        if html.status_code == 200:
            html = html.content.decode('utf-8')
            patt = '<div class="date">(.*?)</div>.*?<div class="week">(.*?)</div>.*?<div class="wdesc">(.*?)</div>.*?<div class="temp">(.*?)</div>.*?<div class="direct">(.*?)</div>.*?<div class="wind">(.*?)</div>'
            pattern = re.compile(patt, re.S)
            results = re.findall(pattern, html)
            weather_information_lists = []
            for result in results:
                weather_information_lists.append(
                    result[0].replace('\n', '').strip() + ':\n' + result[1].replace('\n', '').strip() + ' ' + result[
                    2].replace('\n', '').strip() + ' ' + result[3].replace('\n', '').strip() + ' ' + result[4].replace(
                    '\n', '').strip() + ' ' + result[5].replace('\n', '').strip())

            future_seven_day_weather_information = '\n'.join(weather_information_lists)

        send_seven_day_weather_messages = f"你要说的话" + future_seven_day_weather_information

        return  send_seven_day_weather_messages

    def get_today_weather_info(self,dict_msg='',city_code='101200101', start_date_together = '2017-06-12',sweet_words='your sweet words'):
        '''
        获取天气信息。网址：https://www.sojson.com/blog/305.html
        :param dict_msg: 发送给朋友的信息
        :param city_code: 城市对应编码
        :param start_date: 恋爱第一天日期
        :param sweet_words: 来自谁的留言
        :return: 需要发送的话。
        '''
        print('获取天气信息...')

        weather_url = f'http://t.weather.sojson.com/api/weather/city/{city_code}'
        resp = requests.get(url=weather_url)
        if resp.status_code == 200 and self.isJson(resp) and resp.json().get('status') == 200:
            weatherJson = resp.json()
            # 今日天气
            today_weather = weatherJson.get('data').get('forecast')[1]
            # 今日日期
            today_date = datetime.now().strftime('%Y{y}%m{m}%d{d} %H:%M:%S').format(y='年', m='月', d='日')
            # 今日天气注意事项
            notice = today_weather.get('notice')
            # 温度
            high = today_weather.get('high')
            high_c = high[high.find(' ') + 1:]

            low = today_weather.get('low')
            low_c = low[low.find(' ') + 1:]

            temperature = f"温度: {low_c}/{high_c}"

            # 风
            fx = today_weather.get('fx')
            fl = today_weather.get('fl')
            wind = f"{fx} : {fl}"

            # 空气指数
            aqi = today_weather.get('aqi')
            aqi = f"空气：{aqi}"

            # 在一起，一共多少天了，如果没有设置初始日期，则不用处理
            if start_date_together:
                start_datetime = datetime.strptime(start_date_together,"%Y-%m-%d")
                day_delta = (datetime.now() - start_datetime).days
                delta_msg = f"xxx，这是我们在一起的第{day_delta}天。"
            else:
                delta_msg = ''

            today_notice = f"今天注意事项："
            sweet_words = f"your sweet words"

            send_seven_day_weather_messages = self.get_seven_day_weather_info()
            today_msg = f"{today_date}\n{delta_msg}\n\n{send_seven_day_weather_messages}\n\n{today_notice}\n{notice}。\n{temperature}\n{wind}\n{aqi}\n\n{dict_msg}\n\n{sweet_words if sweet_words else ''}\n"

            # today_msg = f"{today_date}\n{delta_msg}\\n{today_notice}\n{notice}。\n{temperature}\n{wind}\n{aqi}\n\n{dict_msg}\n\n{sweet_words if sweet_words else ''}\n"
            return today_msg

if __name__ == '__main__':
    # 只查看获取数据
    # getWeather().start_today_info(True)

    # 直接运行
    getWeather().run()
