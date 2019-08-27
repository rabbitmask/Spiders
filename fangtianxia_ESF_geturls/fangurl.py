#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
'''
 ____       _     _     _ _   __  __           _
|  _ \ __ _| |__ | |__ (_) |_|  \/  | __ _ ___| | __
| |_) / _` | '_ \| '_ \| | __| |\/| |/ _` / __| |/ /
|  _ < (_| | |_) | |_) | | |_| |  | | (_| \__ \   <
|_| \_\__,_|_.__/|_.__/|_|\__|_|  |_|\__,_|___/_|\_\

'''

import re
import requests
from lxml import etree
from multiprocessing import Pool, Manager
from config import city_list,Connect




DEFAULT_REQUEST_HEADERS = {
  'User-Agent':'Mozilla/5.1 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
  'Referer':'http://www.fang.com/',
  'cookie':'global_cookie=jq9ij5i8s9n62dn25l0pfh0uo20jzm7mbc8; unique_cookie=U_jq9ij5i8s9n62dn25l0pfh0uo20jzm7mbc8*7; city=sh; Integrateactivity=notincludemc; __utma=147393320.647448841.1566449556.1566456403.1566460507.4; __utmc=147393320; __utmz=147393320.1566456403.3.3.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/captcha-f51adebf75/redirect; token=451973f7040b44bba9941ca23fe31a1d; Captcha=32356466796C397247506E737750366441725656347A676B37537848645A49774A7159795836434932437A6A5A5365516C716B55385A2B58486671764A73306E71657276525252595355773D; sfut=08151F2C7835F952680781C547DCA18BA585EACEE8F729083F8F56B93467BDC5371F368D60E5913FECC871042988761D758F6C6D8F37C853C08AB8132F21626560C0096C37CF1D700FDEA14BF3F9F2097C9DC9428EBC8CFAE7EC69061A0085A3; new_loginid=107336404; g_sourcepage=undefined; new_loginid=107336404; login_username=passport1809838837; __utmb=147393320.3.10.1566460507; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1',
}

def saveinfo(url):
    mydb = Connect()
    mycursor = mydb.cursor()
    add = "INSERT INTO `urls` (url) VALUES (%s)"
    addV = [url]
    mycursor.execute(add, addV)
    mydb.close()

def cityscan(url,q):
    r1=requests.get(url,headers=DEFAULT_REQUEST_HEADERS)
    print("任务装载：{}    {}".format(url,r1.status_code))
    pages1=int(re.findall('<p>共(.*?)页</p>',r1.text)[0])
    print('一级页数：{}'.format(pages1))
    if pages1 < 100:
        for i in range(pages1):
            saveinfo(url+'/house/i3'+str(i+1))
    else:
        city=etree.HTML(r1.text).xpath("/html/body/div[3]/div[1]/div[3]/div[2]/div[1]/ul/li[1]/ul/li[*]/a/@href")
        for i in city:
            r2 = requests.get(url+i, headers=DEFAULT_REQUEST_HEADERS)
            pages2 = int(re.findall('<p>共(.*?)页</p>', r2.text)[0])
            print('二级页数：{}'.format(pages2))
            if pages2 < 100:
                for j in range(pages2):
                    saveinfo(url + i + 'i3' + str(j+1))
            else:
                area=etree.HTML(r2.text).xpath("/html/body/div[3]/div[1]/div[3]/div[2]/div[1]/ul/li[2]/ul/li[*]/a/@href")
                for j in area:
                    r3 = requests.get(url + j, headers=DEFAULT_REQUEST_HEADERS)
                    pages3 = int(re.findall('<p>共(.*?)页</p>', r3.text)[0])
                    print('三级页数：{}'.format(pages3))
                    if pages3 < 100:
                        for k in range(pages3):
                            saveinfo(url + j + 'i3' + str(k + 1))
                    else:
                        for k in range(pages3):
                            saveinfo(url + j + 'i3' + str(k + 1))
    q.put(url)


def poolmana():
    p = Pool(60)
    q = Manager().Queue()
    for i in city_list:
        p.apply_async(cityscan,args=(i,q,))
    p.close()
    p.join()


if __name__ == '__main__':
    poolmana()

