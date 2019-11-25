#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# 0 bug, 0 error, 0 warning

from time import sleep
import requests
import re
from dbconfig import Connect

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'}

def getinfo(num):
    response=requests.get('http://www.11467.com/qiye/{}.htm'.format(str(num)),headers=headers)
    if response.status_code == 200:
        r=response.text
        res1 = re.findall('法人名称：</td><td>(.*?)</td>', r)
        res2 = re.findall('地址：</dt><dd>(.*?)</dd>'.replace(" ", "").replace("-", ""), r)
        res3 = re.findall('经理：</dt><dd>(.*?)</dd>', r) or re.findall('联系人：</dt><dd>(.*?)</dd>', r) or re.findall('厂长：</dt><dd>(.*?)</dd>', r) or re.findall('老板：</dt><dd>(.*?)</dd>', r) or re.findall('销售员：</dt><dd>(.*?)</dd>', r) or re.findall('站长：</dt><dd>(.*?)</dd>', r)
        res4 = re.findall('手机号码：</dt><dd>(.*?)</dd>', r) or re.findall('手机：</dt><dd>(.*?)</dd>', r)
        res5 = re.findall('电子邮件：</dt><dd>(.*?)</dd>', r)
        return res1,res2,res3,res4,res5

def saveinfo(num):
    mydb = Connect()
    mycursor = mydb.cursor()
    res=getinfo(num)
    add = "INSERT INTO `sqw` (company,address,manager,telephony,email) VALUES (%s,%s,%s,%s,%s)"
    addV = [''.join(res[0]),''.join(res[1]),''.join(res[2]),''.join(res[3]),''.join(res[4])]
    mycursor.execute(add, addV)
    mydb.close()

def run():
    for i in range(1,100000000):
        print('当前进行至：{}'.format(i))
        sleep(0.1)
        saveinfo(i)

if __name__ == '__main__':
    run()