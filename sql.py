# -*- coding: utf-8 -*-
# @Author: wangfpp
# @Date:   2018-09-03 11:57:12
# @Last Modified by:   wangfpp
# @Last Modified time: 2018-09-18 14:08:30
import pymysql
class sqlQuery(object):
	"""docstring for sqlQuery"""
	def __init__(self, tableName):
		# 打开数据库连接
		self.db = pymysql.connect("localhost", "root", "ddkk1212", tableName, charset='utf8mb4' )
		# 使用cursor()方法获取操作游标 
		self.cursor = self.db.cursor()
	def query(self, url):
		# 使用execute方法执行SQL语句
		self.db.ping(reconnect = True)
		sentence = "SELECT url from booklist WHERE url = '{}'".format(url)
		self.cursor.execute(sentence)
		# 使用 fetchone() 方法获取一条数据
		data = self.cursor.fetchone()
		self.db.close()
		return data
	def insert(self, url, filename, text):
		self.db.ping(reconnect = True)
		string = text.replace('"', '\"').replace("'", "\'")
		sentence = "INSERT INTO booklist (url, filename, text) VALUES (%s, %s, %s)"
		self.cursor.execute(sentence, (url, filename, text))
		self.db.commit() # 必须执行一次commit
		self.db.close()
# if __name__ == '__main__':
# # 	import pymysql
# 	msq = sqlQuery('book')
# 	msq.query('bbb')
	#msq.insert('bbb', 'bbbbb')
#数据库数据类型更改 https://stackoverflow.com/questions/6115612/how-to-convert-an-entire-mysql-database-characterset-and-collation-to-utf-8
#https://blog.csdn.net/gethin_h/article/details/75090198
