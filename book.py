# -*- coding: utf-8 -*-
# @Author: wangfpp
# @Date:   2018-09-03 11:56:51
# @Last Modified by:   wangfpp
# @Last Modified time: 2018-09-19 11:06:05
from requests_html import HTMLSession
from sql import sqlQuery
import logging
import os,sys,re
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
class searchBook(object):
	"""docstring for findbook"""
	def __init__(self, baseURL, totalPage, savePath, endPage):
		self.baseURL = baseURL
		self.totalPage = totalPage
		self.path = savePath
		self.endPage = endPage
	def findbook(self): # find book 按分页查找book
		session = HTMLSession()
		for i in range(self.totalPage, self.endPage, -1):
			url = self.baseURL + str(i)
			# print (url)
			try:
				res = session.get(url, timeout = 10)
				book = res.html.find('div.book-img-box > a')
				for a in book:
					a_href = list(a.absolute_links)[0]
					self.findchapter(a_href)
			except Exception as e:
				logger.error('解析第{}页, {}出错, error: {}'.format(i,url,e))
		session.close()

	def findchapter(self, url): # 寻找一本书的所有章节
		session = HTMLSession()
		try:
			res = session.get(url, timeout = 10)
			bookHtml = res.html.render(sleep = 5) # sleep 10s 这里需要render一下 等待js加载完成
			try:
				book = res.html.find('div.book-info > h1 > em', first = True)
				bookName = book.text.replace('/', '·')
				chapter = res.html.find('div.volume > ul.cf > li > a')
				if not os.path.exists(self.path + bookName):
					os.mkdir(self.path + bookName)
				for link in chapter:
					chapter_link = list(link.absolute_links)[0]
					chapter_name = link.text.replace('/', '·')
					if sql.query(chapter_link) == None:
						self.findtxt(chapter_link, bookName, chapter_name)
			except Exception as e:
				logger.error('解析书名出错, {book},{e}'.format(book,e))
		except Exception as e:
			logger.error('请求bookurl出错, {url}'.format(url))
		session.close()

	def findtxt(self, chapter_link, bookName, chapter_name): # 寻找某一章节的全部TXT
		session = HTMLSession()
		res = session.get(chapter_link, timeout = 10)
		content = res.html.find('div.read-content > p')
		name = chapter_name + '.txt'
		filename = re.sub('\"', '', re.sub("\'", '', name))
		string = ''
		for txt in content:
			string += txt.text
		if self.is_have_file(bookName, filename):
			self.savetext(string, bookName, filename)
		else:
			logger.info('文件已经存在{}'.format(self.path+bookName+'/'+filename))
		string = string.replace('"', '\"').replace("'", "\'")
		try:
			sql.insert(chapter_link, filename, string)
		except Exception as e:
			logger.error('插入数据库出错{}-{}:{} {}'.format(chapter_link, filename, string, e))
		session.close()
	def savetext(self, txt, bookName, filename):
		f = open(self.path + bookName + '/' + filename, 'a')
		f.write(txt)
		f.close()
	def is_have_file(self, bookName, filename):#判断是否已经存在此新闻 节省资源
		file_list = os.listdir(self.path + bookName)
		if filename in file_list:
			return False
		else:
			return True
if __name__ == '__main__':
	book = searchBook('https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=', 500, '/media/nas/speech_datas/newbook/', 0)
	book.findbook()


		
