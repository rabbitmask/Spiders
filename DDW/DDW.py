#!/usr/bin/env python3
#_*_ coding:utf-8 _*_
'''
 ____       _     _     _ _   __  __           _    
|  _ \ __ _| |__ | |__ (_) |_|  \/  | __ _ ___| | __
| |_) / _` | '_ \| '_ \| | __| |\/| |/ _` / __| |/ /
|  _ < (_| | |_) | |_) | | |_| |  | | (_| \__ \   < 
|_| \_\__,_|_.__/|_.__/|_|\__|_|  |_|\__,_|___/_|\_\
                                                    
'''
import requests
import re
from multiprocessing import Pool, Manager

headers = {'user-agent': 'ceshi/0.0.1'}

#信息爬取模块
def getInfo(page,yourkey):
    r = requests.get('http://search.dangdang.com/?key='+str(yourkey)+'&ddsale=1&page_index='+str(page) , headers=headers)
    r1=re.compile(r'<a title=" (.*?)"  ddclick=')
    r2=re.compile(r'<span class="search_now_price">&yen;(.*?)</span>')
    re1 = r1.findall(r.text)
    re2 = r2.findall(r.text)
    return dict(zip(re1, re2))              #将列表转为字典

#文件存储模块
def saveinfo(page,yourkey,q):
    fw = open('DangDang.txt', 'a')
    di=getInfo(page,yourkey)                #新建字典接收返回结果
    for i in di:                            #整理格式写入文件
        fw.write('书籍名称:'+i+'\t'+'当前价格'+di[i]+'\n')
    fw.close()
    q.put(page)

#进程池管理模块
def poolmana(pages,yourkey):
    p = Pool(10)
    q = Manager().Queue()
    for i in range(pages):
        p.apply_async(saveinfo, args=(i+1, yourkey,q))
    p.close()
    p.join()
    print('读取完成>>>>>\n请查看当前路径下文件：DangDang.txt')

#助手函数，输入判断
def is_number(s):                           #当了个助手函数用来判断用户输入内容
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

#主函数，实现界面
def main():
    print('''
            ============================================
                【欢迎来到史上最屌的当当网查询系统】  
                                  （输入exit退出）      
            ============================================
                                    ''')
    while True:
        try:
            yourkey=input('请输入您要查询的内容：')
            if yourkey=='exit':
                break
            pa=input('请输入希望检索的页数：\n(默认为3)\n')
            if pa=='exit':
                break
            if is_number(pa)==False:        #使用助手函数判断输入是否为数字，如否，使用默认值3
                pa=3
            print('读取ing~>>>>>>\n数据量较大，请耐心等待>>>>>')
            poolmana(int(pa),str(yourkey))
        except:
            print("请规范您的输入！")

if "__main__" == __name__ :
    main()

