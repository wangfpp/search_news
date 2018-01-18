# -*- coding: utf-8 -*-
# @Author: wang
# @Date:   2018-01-17 10:15:25
# @Last Modified by:   wangfpp
# @Last Modified time: 2018-01-18 20:04:55
import requests
from bs4 import BeautifulSoup
import os
import re

class ClassName(object):
    """获取base_url http://www.chinanews.com/的新闻材料"""
    def __init__(self,base_url):#Class类初始化函数  base_url为解读的新闻网页的主页
        self.base_url = base_url
        pass
    def get_href(self):#获取 网页的a标签的 href  过滤后 进行解析其新闻文本
        # try:
        self.alink = alink = []
        req = requests.get(self.base_url)
        req.status_code == 200
        print ('\033[0;32;47m 解析正常进行\033[0m')
        req_content = req.content
        soup = BeautifulSoup(req_content, 'html.parser')
        a_tag = soup.find_all('a')
        for href in a_tag:
            if href.get('href'):
                alink.append(href.get('href'))
        self.filter_a_href()#对获取的a标签进行过滤
        for url in self.alink:
            file_name = (re.sub(self.base_url, '', os.path.splitext(url)[0], 0) + "{0}").replace('/','_').format('.txt')
            print self.is_have_file(file_name),file_name
            if self.is_have_file(file_name):
                print ('正在提取:{0}的文字').format(url)
                self.get_text(url)
        # except:
        #     print ('\033[7;31;47m 网页解析出错 \033[0m')#https://www.cnblogs.com/ping-y/p/5897018.html
        #     #print color ('\033[显示方式;字体颜色;背景颜色m　print text　\033[0m')

    def get_text (self,url):#获取新闻网页的新闻内容
        file_name = (re.sub(self.base_url, '', os.path.splitext(url)[0], 0) + "{0}").replace('/','_').format('.txt')
        #try:
        req = requests.get(url)#, timeout=3
        #print ('\033[0;32m 正在获取网页　\033[0m {0} {1}').format(req.status_code,url) 
        
        req.encoding = 'GB2312' 
        html = req.text
        #try:   
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.find_all('div', class_ = 'left_zw')
        for item in content:
            for txt_contene in item.contents:
                if txt_contene.string and len(txt_contene.string) > 5:
                    #print url,txt_contene.string
                    print ('保存新闻内容到:{0}').format(file_name)
                    self.save_text(txt_contene.string.encode('utf-8'),file_name)
        #     except:
        #         print ('\033[0;31m 网页解析错误\033[0m {0}').format(url)
        # except:
        #     print ('\033[0;31m 网页获取错误\033[0m {0}').format(url)

    def save_text(self,txt,filename):#保存新闻内容到txt文件中
        f = open('./txt/' + filename, 'a')
        f.write(txt)
        f.close()
    
    def is_have_file(self,filename):#判断是否已经存在此新闻 节省资源
        file_list = os.listdir('./txt/')
        if filename in file_list:
            return False
        else:
            return True

    def filter_a_href (self):#过滤a标签
        for a in  range(len(self.alink)):
            if self.alink[a].find('//', 0, 2) != -1:
                self.alink[a] = 'http:' + self.alink[a]
            if self.alink[a].find('/', 0, 1) != -1:
                self.alink[a] = 'http://www.chinanews.com' + self.alink[a]
        for item in range(len(self.alink))[::-1]:
            if not 'http://www.chinanews.com' in self.alink[item]:
                del self.alink[item] 

if __name__ == '__main__':
    base_url = 'http://www.chinanews.com/'
    a = ClassName(base_url)
    a.get_href()
        
  			
  		

				

