# -*- coding: utf-8 -*-
# @Author: wangfpp
# @Date:   2018-08-30 10:01:54
# @Last Modified by:   wangfpp
# @Last Modified time: 2018-08-31 19:55:38
import MySQLdb
class sqlQuery(object):
	"""docstring for sqlQuery"""
	def __init__(self, tableName):
		# 打开数据库连接
		self.db = MySQLdb.connect("localhost", "root", "ddkk1212", tableName, charset='utf8' )
		# 使用cursor()方法获取操作游标 
		self.cursor = self.db.cursor()
	def query(self, url):
		# 使用execute方法执行SQL语句
		sentence = "SELECT url from booklist WHERE url = '{}'".format(url)
		self.cursor.execute(sentence)
		# 使用 fetchone() 方法获取一条数据
		data = self.cursor.fetchone()
		print data
		return data
	def insert(self, url, filename):
		sentence = "INSERT INTO booklist (url, filename) VALUES ('%s', '%s')" % (url, filename)
		try:
			self.cursor.execute(sentence)
			self.db.commit() # 必须执行一次commit
			print self.cursor.execute("SELECT * from booklist")
		except Exception as e:
			print e
		
# if __name__ == '__main__':
# 	import MySQLdb
# 	msq = sqlQuery('book')
# 	#msq.query('bbb')
# 	msq.insert('bbb', 'bbbbb')
