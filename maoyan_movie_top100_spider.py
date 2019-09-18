# -*- coding:utf-8 -*-
import requests
import re
import json
from requests.exceptions import RequestException

# get one url page
def get_one_page(url):
    try:
        headers = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

# parse html's content, get information we want to get
def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)'
                         + '</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',
                         re.S)
    items = re.findall(pattern,html)

    for item in items:
        # print(item)
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score': item[5].strip() + item[6].strip()
        }

# write our content into a txt file
def write_to_file(content):
    with open('maoyan_movie_top100_result.txt','a', encoding='utf-8') as f:
        # print type of json.dumps()
        print(type(json.dumps(content)))
        # json.dumps(): turn dict to str
        f.write(json.dumps(content,ensure_ascii=False) + '\n')

# main function
def main():
    base_url = 'https://maoyan.com/board/4?offset='
    urls = []

    for i in range(10):
        url = base_url + str(i * 10)
        print('url %d '% (i + 1),url)
        urls.append(url)
    for url in urls:
        print(url)
        html = get_one_page(url)
        # print(html)

        for item in parse_one_page(html):
            print('item:\n',item)
            write_to_file(item)

if __name__ == '__main__':
    main()

