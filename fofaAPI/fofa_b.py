#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# 0 bug, 0 error, 0 warning

import re
from time import sleep
import requests
from multiprocessing import Pool, Manager
import base64
import sys


headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
    "Cookie":'[Your Cookie]',}


def getinfo(p,q,d):
    print('当前进度：第{}页'.format(p))
    response=requests.get("https://fofa.so/result?full=true&page="+ str(p) +"&qbase64="+str(q),headers=headers)
    r1= re.compile(r'<a target="_blank" href="(.*?)">.*?<i class')
    r = r1.findall(response.text)
    d.put(p)
    return r

def saveinfo(result):
    print(result)
    for i in result:
        fw=open('result.txt','a')
        fw.write(i+'\n')
        fw.close()

def poolmana(pages,keyword):
    p = Pool(10)
    q = Manager().Queue()
    for i in range(pages//5):
        for j in range(i*5,i*5+5):
            p.apply_async(getinfo, args=(j+1, keyword,q),callback=saveinfo)
        sleep(30)
    p.close()
    p.join()
    print('读取完成>>>>>\n请查看当前路径下文件：result.txt')


def run(keyword,pages):
    bkeyword=bytes(keyword,encoding="utf8")
    bs64 = base64.b64encode(bkeyword)
    bs64=bs64.decode()
    bs64 = bs64.replace('+','%2b')
    print(bs64)
    poolmana(pages,bs64)


if __name__ == '__main__':
    keyword='title="测试"||domain="baidu.com"'
    pages=10
    run(keyword,pages)