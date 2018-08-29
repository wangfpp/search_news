# -*- coding: utf-8 -*-
# @Author: wangfpp
# @Date:   2018-08-27 17:31:11
# @Last Modified by:   wangfpp
# @Last Modified time: 2018-08-28 13:43:06
import requests#接口请求模块
from bs4 import BeautifulSoup#网页解析模块
import logging
import time
import os,sys
import re
sys.setrecursionlimit(1000000)
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


class searchBook(object):
	"""docstring for main"""
	def __init__(self, baseURL, totalPage, path):
		self.baseURL = baseURL
		self.totalPage = totalPage
		self.path = path
	def findBook(self):
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
					self.book.append(bookLink)
		self.beginReading()
	def beginReading(self):
		self.oneChapter = []
		for book in self.book:
			req = requests.get(book)
			if req.status_code == 200:
				html = req.content
				soup = BeautifulSoup(html, 'html.parser')
				pagination = soup.find_all('a', id = 'readBtn')
				chapter =  'https:' + pagination[0].get('href')
				#self.oneChapter.append(chapter)
				self.getText(chapter)
		# for link in self.oneChapter:
			
	def getText(self, link):
		req = requests.get(link)
		index =  link.find('chapter')
		filename = link[index + 8:len(link)].replace('/', '-') + '.txt'
		if req.status_code == 200:
			html = req.content
			soup = BeautifulSoup(html, 'html.parser')
			pagination = soup.find_all('div', class_ = 'read-content j_readContent')[0]
			nextChapter = soup.find_all('a', id = 'j_chapterNext')[0]
			nextChapterLink = 'https:' + nextChapter.get('href')
			nextChapterText = nextChapter.string
			if self.is_have_file(filename):
				for text in pagination.descendants:
					if text.string != None:
						self.saveText((text.string).encode('utf-8'), filename)
			if not ((nextChapter.string).encode('utf-8') == '书末页'):
				self.getText(nextChapterLink)
	def saveText(self, txt, filename):
		f = open(self.path  + filename, 'a')
		f.write(txt)
		f.close()
	def is_have_file(self,filename):#判断是否已经存在此新闻 节省资源
		file_list = os.listdir(self.path)
		if filename in file_list:
			return False
		else:
			return True
if __name__ == '__main__':
	a = searchBook('https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=', 50027, '/media/nas/speech_datas/booktext/')
	a.findBook()
		