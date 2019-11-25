#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
'''
 ____       _     _     _ _   __  __           _
|  _ \ __ _| |__ | |__ (_) |_|  \/  | __ _ ___| | __
| |_) / _` | '_ \| '_ \| | __| |\/| |/ _` / __| |/ /
|  _ < (_| | |_) | |_) | | |_| |  | | (_| \__ \   <
|_| \_\__,_|_.__/|_.__/|_|\__|_|  |_|\__,_|___/_|\_\

'''
import MySQLdb


def Connect():
    mydb = MySQLdb.connect(
        host="localhost",  # 数据库主机地址
        user="root",  # 数据库用户名
        passwd="root",  # 数据库密码
        database="SQW",  # 指定数据库
        charset="utf8"
    )
    return mydb