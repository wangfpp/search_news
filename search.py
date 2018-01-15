# -*- coding: utf-8 -*-
# @Author: wang
# @Date:   2017-1-10 17:45:59
# @Last Modified by:   wang
# @Last Modified time: 2017-1-15 17:46:13
#http://www.chinanews.com/  依次URL为主入口来获取所有的新闻信息

import requests#请求接口
from bs4 import BeautifulSoup#提取网页
import re#正则表达式
import os#路径操作
#import MySQLdb#MySQL

#
home_url = 'http://www.chinanews.com'
url = 'http://www.chinanews.com/cj/2018/01-03/8415342.shtml'#测试url
def save_txt(index, name, txt):#保存新闻信息　name : 文件名根据新闻日期来的
  			f = open(name + '.txt', 'a')#有待优化的地方  现在是重写
			f.write(txt + "\r\n")#写入文件 没写一句就换行
			f.close()#关闭读写文件
			print '保存文件:' + str(name) + '.txt'
def get_text(index,url):#获取新闻信息
  	req = requests.get(url)#request 模块去读网页信息  response 200
	html = req.content
	soup = BeautifulSoup(html, 'html.parser')#解析HTML页面
	tag = soup.find_all('div', class_ = "left_zw")#获取到新闻的主要内容
  	file_name = re.sub(home_url, '', re.sub(os.path.splitext(url)[1], '', url, 0), 0).replace('/', '_')#生成文件名  /replace ’‘
	for content in tag:#循环标签获取新闻信息
			for text in content.contents:
				if (text.string and len(text.string)) > 5:#大于５个字符算一句话
					save_txt(index,file_name,text.string.encode('utf-8'))
def get_herf (home_url):#获取主网页的a链接 然后进入网页 获取网页信息
	alink = []
	home_page = requests.get(home_url).content
	soup = BeautifulSoup(home_page, 'html.parser')
	a_link_to_news = soup.find_all('a')
	for a in a_link_to_news:
  		if a.get('href'): #and ('www.chinanews.com' in a.get('href') or re.match('//',a.get('href')) or re.match('/',a.get('href'))):
					alink.append(a.get('href'))
	for index, link in enumerate(alink):
  		if link.find('//', 0, 2) != -1:
  			link = link.replace('//', '', 1)
			if link.find('/', 0, 1) != -1 and link.find('//', 0, 2) == -1:
  			 link = home_url + link
			get_text(index , 'http://' + link)
get_herf(home_url)

























