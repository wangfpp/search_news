# -*- coding: utf-8 -*-
# @Author: wangfpp
# @Date:   2018-05-30 11:29:55
# @Last Modified by:   wangfpp
# @Last Modified time: 2018-05-30 16:23:31
import requests
import logging
import os,sys
import wget
from bs4 import BeautifulSoup as bs
'''路径处理'''
curr_path = os.path.dirname(os.path.abspath(__file__))
comm_path = os.path.dirname(curr_path)
if comm_path not in sys.path:
	sys.path.append(comm_path)
'''日志信息处理'''
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler('{}/log.txt'.format(curr_path))
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class searchppt(object):
	"""docstring for searchppt"""
	'''deatial url http://www.1ppt.com/kejian/#yuwen'''
	def __init__(self,homeurl,baseurl,path):#baseurl urlList[] 排除英语 美术 音乐 幼儿 path 资源存放路径 nas/ocr/downloadppt
		self.homeurl = homeurl
		self.baseurl = baseurl
		self.path = path
	def get_subject(self):
		self.nav = []
		self.downloadLink = []
		try:
			req = requests.get(self.baseurl)
			html = req.content
			soup = bs(html,'html.parser')
			nav = soup.find_all('div', id = "navMenu")
			nav_href = nav[0].find_all('a')
			for item in nav_href:
				href = item.get("href")
				if href:
					print href
					url = '{}{}'.format(self.homeurl,href)
					subject = url.split('#')[1]
					self.nav.append({'url' : url,'subject':subject})
			self.search_resource()
		except Exception as e:
			logger.error(e)

	def search_resource(self):
		for index in range(len(self.nav)):
			print '正在解析{}'.format(self.nav[index]['url'])
			if self.nav[index]['subject'] not in os.listdir(self.path):
				os.mkdir(self.path + self.nav[index]['subject'])
			try:
				req = requests.get(self.nav[index]['url'])
				html = req.content
				soup = bs(html,'html.parser')
				link = soup.find_all('dd', class_ = "ikejian_col_nav")
				link_a = link[index].find_all('a')
				for href in link_a:
					if href.get('href'):
						link_url = '{}{}'.format(self.homeurl,href.get('href'))
						self.get_all_href(link_url,self.nav[index]['subject'])
			except Exception as e:
				logger.error(e)
	def get_all_href(self,url,subject):#解析两种类型的url 一种目录结构  一种列表模式
		print '搜索{}的目录'.format(url)
		target_arr = []
		if 'html' in url:
			node_a = []
			type_one_soup = self.bs_parse(url)
			node = type_one_soup.find_all('table',class_ = "kjmulu")
			for i in range(len(node)):
				if i % 2 != 0:
					node_a += node[i].find_all('a')
			for a in node_a:
				href = a.get('href')
				downurl = self.get_download_url(href)
				for target in downurl:
					if target.get('href') and target.get('href') not in target_arr:
						target_arr.append(target.get('href'))
		else:
			type_two_soup = self.bs_parse(url)
			node = type_two_soup.find_all('ul', class_ = 'arclist')
			node_a = node[0].find_all('a')
			for a in node_a:
				href = '{}/{}'.format(self.homeurl,a.get('href'))
				if '.html' in href:
					downurl = self.get_download_url(href)
					for target in downurl:
						if target.get('href') and target.get('href') not in target_arr:
							target_arr.append(target.get('href'))
		for item in target_arr:#http://ppt.1ppt.com/uploads/soft/1612/2-161221132602.rar
			filename = os.path.split(item)[1]
			if not self.is_have_file(self.path+subject,filename):
				filename = wget.download(item,self.path+subject)
	def is_have_file(self,folder,filename):
		folder_content = os.listdir(folder)
		if filename in folder_content:
			return True
		return False
	def get_download_url(self,url):
		downhtml = self.bs_parse(url)
		downbutton = downhtml.find_all('ul', class_ = "downurllist")
		downurl = downbutton[0].find_all('a')
		return downurl
	def bs_parse(self,url):
		req = requests.get(url)
		html = req.content
		soup = bs(html,'html.parser')
		return soup




if __name__ == '__main__':
	homeurl = 'http://www.1ppt.com'
	baseurl = 'http://www.1ppt.com/kejian/'
	path = '/home/wang/nas/ocr/OCR_samples/downloadppt/'
	a = searchppt(homeurl,baseurl,path)
	a.get_subject()
	
