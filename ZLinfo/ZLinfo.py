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
import MySQLdb
import requests
import logging

#请根据您的需求配置以下参数
place_name = ['济南']
job_name = ['渗透测试', '网络安全', '信息安全']

#测试专用header头
headers = {'user-agent': 'ceshi/0.0.1'}

#日志记录配置
logging.basicConfig(filename='logging.log',
                    format='%(asctime)s %(message)s',
                    filemode="w", level=logging.INFO)

#生成地址列表
def get_urls():
    urls=[]
    for keyword in job_name:
        for i in place_name:
            url = 'https://fe-api.zhaopin.com/c/i/sou?pageSize=1800' + '&cityId=' + str(i) + '&kw=' + str(keyword) + '&kt=3'
            urls.append(url)
    return urls


#配置数据库
def Connect():
    mydb = MySQLdb.connect(
        host="localhost",  # 数据库主机地址
        user="root",  # 数据库用户名
        passwd="root",  # 数据库密码
        database="zhilian",  # 指定数据库
        charset="utf8"
    )
    return mydb


#创建数据表
def CreateTable():
    mydb = Connect()
    mycursor = mydb.cursor()
    create_sql = "CREATE TABLE if not exists `zhilian`.`zhilian`  (  `id` int(0) NOT NULL,  `jobName` varchar(255) NULL,  `salary` varchar(255) NULL,  `company` varchar(255) NULL,  `city` varchar(255) NULL,  `eduLevel` varchar(255) NULL,  `workingExp` varchar(255) NULL,  PRIMARY KEY (`id`))"
    mycursor.execute(create_sql)
    mydb.close()
    print ('数据表创建成功')
    logging.info('数据表创建成功')


#数据获取
def getinfo(url):
    r=requests.get(url,headers=headers)
    r1 = re.compile(r'"jobName":"(.*?)"')
    re1 = r1.findall(r.text)
    r2 = re.compile(r'"salary":"(.*?)"')
    re2 = r2.findall(r.text)
    r3 = re.compile(r'"company".*?"},"name":"(.*?)"')
    re3 = r3.findall(r.text)
    r4 = re.compile(r'"city":{"display":"(.*?)"')
    re4 = r4.findall(r.text)
    r5 = re.compile(r'"eduLevel".*?"name":"(.*?)"')
    re5 = r5.findall(r.text)
    r6 = re.compile(r'"workingExp".*?"name":"(.*?)"')
    re6 = r6.findall(r.text)
    return (re1,re2, re3, re4, re5, re6)


#写入数据表
def AddTable(re1,re2, re3, re4, re5, re6):
    for i in range(len(re1)):
        mydb = Connect()
        mycursor = mydb.cursor()
        sql = "INSERT INTO zhilian (jobName,salary,company,city,eduLevel,workingExp) VALUES (%s,%s,%s,%s,%s,%s)"
        val = [(re1[i],re2[i],re3[i],re4[i],re5[i],re6[i])]
        mycursor.executemany(sql,val)
        mydb.close()
        print ('数据添加成功')
        logging.info('数据添加成功')


#执行模块
def run():
    CreateTable()
    urls=get_urls()
    for i in range(len(urls)):
        url=urls[i]
        re1,re2, re3, re4, re5, re6 =getinfo(url)
        AddTable(re1,re2, re3, re4, re5, re6)


if __name__ == '__main__':
    run()