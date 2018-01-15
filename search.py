# -*- coding:utf-8 -*-
import requests#请求接口
from bs4 import BeautifulSoup#提取网页
import datetime#日期时间
import re#正则表达式
import os#路径操作
#import MySQLdb#MySQL

#
home_url = 'http://www.chinanews.com'
url = 'http://www.chinanews.com/cj/2018/01-03/8415342.shtml'

def save_txt(index, name, txt):#保存新闻信息　name : 文件名根据新闻日期来的
	f = open(name + '.txt', 'a')
	f.write(txt + "\r\n")
	f.close()

def get_text(index,url):
  	print '正在读取第' + str(index) + '个网页'
  	req = requests.get(url)
	html = req.content
	soup = BeautifulSoup(html, 'html.parser')
	tag = soup.find_all('div', class_ = "left_zw")
  	file_name = re.sub(home_url, '', re.sub(os.path.splitext(url)[1], '', url, 0), 0).replace('/', '_')
	is_have_file = False
	for file in os.listdir('./'):
			if file == file_name + '.txt':
					is_have_file = True
	for content in tag:
			for text in content.contents:
				if (text.string and len(text.string)) > 5:#大于５个字符算一句话
					if not is_have_file:
  						print '正在保存文件:' + str(file_name) + '.txt'
						save_txt(index,file_name,text.string.encode('utf-8'))

def get_herf (home_url):
  	print '正在读取超链接......'
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
























