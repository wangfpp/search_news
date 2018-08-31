# -*- coding: utf-8 -*-
# @Author: wangfpp
# @Date:   2018-08-27 17:31:11
# @Last Modified by:   wangfpp
# @Last Modified time: 2018-08-31 20:07:43
import requests#接口请求模块
from bs4 import BeautifulSoup#网页解析模块
import logging
import time
import os,sys
import re
import hashlib
from booklist import sqlQuery
curr_path = os.path.dirname(os.path.abspath(__file__))
comm_path = os.path.dirname(curr_path)
if comm_path not in sys.path:
    sys.path.append(comm_path)
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("{}/log.txt".format(curr_path))
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

sql = sqlQuery('book')
# print sql.query('https://read.qidian.com/chapter/ORlSeSgZ6E_MQzCecGvf7A2/_z6MiQn6sK9Ms5iq0oQwLQ2')
class searchBook(object):
	"""docstring for main"""
	def __init__(self, baseURL, totalPage, path):
		self.baseURL = baseURL
		self.totalPage = totalPage
		self.path = path
	def findBook(self): # find book according page
		self.book = []
		for page in range(1, self.totalPage):
			url = '{}{}'.format(self.baseURL, page)
			req = requests.get(url)
			if req.status_code == 200:
				html = req.content
				soup = BeautifulSoup(html, 'html.parser')
				pagination = soup.find_all('div', class_ = 'book-img-box')
				for tag in pagination:
					aTag = tag.find_all('a')
					href = aTag[0].get('href')
					bookLink = 'https:{}'.format(href) 
					#sql.insert(bookLink, str(hashlib.md5(bookLink).hexdigest()))
					self.beginReading(bookLink)
	def beginReading(self, url): # 找出章节
		allcharpter = []
		req = requests.get(url)
		if req.status_code == 200:
			html = req.content
			soup = BeautifulSoup(html, 'html.parser')
			volume = soup.find_all('div', class_ = "volume");
			bookName = soup.find('div', class_ = "book-info").h1.em.string.encode('utf-8')
			for item in volume:
				for atag in item.find_all('ul', class_ = "cf"):
					for a in atag.find_all('a'):
						allcharpter.append({'name': a.string.encode('utf-8') + '.txt', 'link': 'https:' + a.get('href')})
			if not os.path.exists(self.path + bookName):
				os.mkdir(self.path + bookName)
		for obj in allcharpter:
			print  obj['name'], obj['link']
			if sql.query(obj['link']) == None:
				self.getText(obj['link'], bookName, obj['name'])
	def getText(self, link, bookName, chapterName):
		req = requests.get(link)
		index =  link.find('chapter')
		if req.status_code == 200:
			html = req.content
			soup = BeautifulSoup(html, 'html.parser')
			pagination = soup.find_all('div', class_ = 'read-content j_readContent')[0]
			for text in pagination.descendants:
				if text.string != None:
					self.saveText((text.string).encode('utf-8'), chapterName, bookName)
			sql.insert(link, str(hashlib.md5(chapterName).hexdigest()))
	def saveText(self, txt, filename, bookName):
		f = open(self.path + bookName + '/' + filename, 'a')
		f.write(txt)
		f.close()
	def is_have_file(self,filename):#判断是否已经存在此新闻 节省资源
		file_list = os.listdir(self.path)
		if filename in file_list:
			return False
		else:
			return True
if __name__ == '__main__':
	a = searchBook('https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=', 2, './')
	a.findBook()
		