#!/usr/bin/env python
# _*_ coding:utf-8 _*_
'''
 ____       _     _     _ _   __  __           _
|  _ \ __ _| |__ | |__ (_) |_|  \/  | __ _ ___| | __
| |_) / _` | '_ \| '_ \| | __| |\/| |/ _` / __| |/ /
|  _ < (_| | |_) | |_) | | |_| |  | | (_| \__ \   <
|_| \_\__,_|_.__/|_.__/|_|\__|_|  |_|\__,_|___/_|\_\

'''

import requests
import re
import time
import random

headers = {
    'Host': 'www.butian.net',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://www.butian.net/Loo',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cookie':'PHPSESSID=5dd3sthc5apjagdnr4o2491602; __guid=66782632.1664862250244665600.1557796022581.058; __DC_sid=66782632.169128837010834560.1557802913718.1436; btlc_ab7a660c7e054d9e446e06f4571ebe41=a8ba629076f379d3f25f1755143e7ef7b51f320b73921a1df0abc56acba54af8; __q__=1557803853434; _currentUrl_=%2FLoo%2Findex%2Fp%2F2.html; __DC_monitor_count=21; __DC_gid=66782632.922877208.1557796022582.1557803854280.38',
    'Connection': 'close'}

def run(url):
    time.sleep(random.randint(1,5))
    try:
        r = requests.get(url,headers=headers,timeout=5)
        res1 = re.findall('<a href="/Company/u/.*?">(.*?)</a>', r.text)
        res2 = re.findall(u'<span>\u7684\u4e00\u4e2a(.*?)</span>', r.text)
        res3 = re.findall('<em>.*?class="loopHigh">(.*?)</strong>', r.text)

        for i in range(len(res1)):
            f = open("result.txt", "a")
            st=res1[i] +' '+ res2[i] +' '+ res3[i]+'\n'
            f.write(st.encode('gb2312'))
            f.close()
    except:
        pass


if __name__ == '__main__':
    for i in range(6102):
        print (u'当前页数：{}'.format(i+1))
        run('https://butian.360.net/Loo/index/p/' + str(i) + '.html')