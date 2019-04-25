#!/usr/bin/python env
# -*- coding: utf-8 -*-
# 一个小爬虫，抓取猫眼电影排行旁，获取排名、海报地质、片名、演员、上映时间、评分
import  requests
import re
import time

import codecs,sys
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def get_one_page(url):
    headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    response = requests.get(url, headers=headers, timeout=3)
    if response.status_code == 200:
        return response.text
    return None
def parse_one_page(html):
    patten = re.compile('<dd.*?>(\d+)</i>.*?data-src="(.*?)".*?title="(.*?)".*?"star">(.*?)<.*?"releasetime">(.*?)</p>.*?"integer">(.*?)</i>.*?"fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(patten, html)
    for i in items:                                           #使用生成器节约内存
        yield {
            'index': i[0],
            'image': i[1],
            'title': i[2].strip(),
            'actor': i[3].strip()[3:],
            'time': i[4].strip()[5:],
            'sorce': i[5].strip() + i[6].strip()
        }


def main(offset):
    url = 'http://maoyan.com/board/4?offset={}'.format(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)

if __name__ == '__main__':
    for i in range(10):
        main(offset=i*10)
        time.sleep(1)
