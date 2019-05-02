import requests
import re
import itchat
# import time

# def get_weather_informations():

url = 'http://www.nmc.cn/publish/forecast/ASH/shanghai.html'
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}
html = requests.get(url,headers=headers)
html=html.content.decode('utf-8')
# print(html)

# the weather of future 7 days
patt = '<div class="date">(.*?)</div>.*?<div class="week">(.*?)</div>.*?<div class="wdesc">(.*?)</div>.*?<div class="temp">(.*?)</div>.*?<div class="direct">(.*?)</div>.*?<div class="wind">(.*?)</div>'
# patt = '<div class="date">(.*?)</div>.*?<div class="wdesc">(.*?)</div>'
pattern = re.compile(patt,re.S)
results = re.findall(pattern,html)

itchat.auto_login(True)
author = itchat.search_friends(name='小美女')[0]
# for author in authors:
# print(author)
# author.send('小美女呀，未来7天的天气分别是：')
weather_information_lists=[]
for result in results:
    # print(result[0].replace('\n','').strip()+'\n'+result[1].replace('\n','').strip()+' \t '+result[2].replace('\n','').strip()+' \t '+result[3].replace('\n','').strip()+' \t '+result[4].replace('\n','').strip()+' \t '+result[5].replace('\n','').strip())
    # author.send(result[0].replace('\n','').strip()+' \t '+result[1].replace('\n','').strip()+' \t '+result[2].replace('\n','').strip()+' \t '+result[3].replace('\n','').strip()+' \t '+result[4].replace('\n','').strip()+' \t '+result[5].replace('\n','').strip())
    weather_information_lists.append(result[0].replace('\n','').strip()+':\n'+result[1].replace('\n','').strip()+' '+result[2].replace('\n','').strip()+' '+result[3].replace('\n','').strip()+' '+result[4].replace('\n','').strip()+' '+result[5].replace('\n','').strip())
# print(weather_information_lists)

weather_information = '\n'.join(weather_information_lists)

# obtain tm_year,tm_mon,tm_mday,tm_hour,tm_min,tm_sec
# current_time = time.localtime()

# print(weather_information)
send_messages = '小美女呀，未来7天的天气分别是：\n'+weather_information + '\n注意天气变化哦~\n'+'爱你的小哥，嘿嘿'
print(send_messages)
author.send(send_messages)

# return results

# tomorrow = results[1] # tomorrow weather
# the_day_after_tomorrow = results[2]
# for result in tomorrow:
#     print(result.replace('\n','').strip())
# for result in the_day_after_tomorrow:
#     print(result.replace('\n', '').strip())

# def itchat_auto_send_messages():
    # author = itchat.search_friends(wechatAccount='yjy13387561456')
    # author = itchat.search_friends(name='filehelper')

    # weather_information = get_weather_informations()
    # for result in weather_information:

        # print(result[0].replace('\n','').strip()+'\n'+result[1].replace('\n','').strip()+' \t '+result[2].replace('\n','').strip()+' \t '+result[3].replace('\n','').strip()+' \t '+result[4].replace('\n','').strip()+' \t '+result[5].replace('\n','').strip())

        # send_messages = result[0].replace('\n','').strip()+'\n'+result[1].replace('\n','').strip()+' \t '+result[2].replace('\n','').strip()+' \t '+result[3].replace('\n','').strip()+' \t '+result[4].replace('\n','').strip()+' \t '+result[5].replace('\n','').strip()
        # author.send('%s'%send_messages)
itchat.run(True)

# def main():
    # itchat_auto_send_messages()
    # get_weather_informations()


# if '__name__' == '__main__':
#     main()


