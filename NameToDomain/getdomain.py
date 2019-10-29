#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# 0 bug, 0 error, 0 warning

import re
import requests

headers = {'user-agent': 'Mozilla/5.1 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',}

def getinfo(username):
    response=requests.get("http://www.baidu.com"+'/s?wd='+str(username),headers=headers)
    # print(response.text)
    r1=re.compile(r'bds.comm.iaurl=\["http:\\\/\\\/(.*?)\\\/",')
    re1 = r1.findall(response.text)
    return re1

def run():
    fr=open('name.txt','r')
    res=fr.readlines()
    fr.close()
    for i in res:
        i=i.replace('\n','')
        r=getinfo(i)
        print(r)
        if r:
            fw=open('domain.txt','a')
            fw.write(r[0]+'\n')
            fw.close()
        else:
            fw=open('domain.txt','a')
            fw.write('\n')
            fw.close()


if __name__ == '__main__':
    run()