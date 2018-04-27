# 中国新闻网爬虫说明

# 项目背景:
	1.OCR识别可能会出现语义不通的情况
	2.根据语义模型来纠正OCR的识别结果
	3.从新闻网站获取大量的文字来训练语义模型

# 使用
	1.安装Python python2.7
	2.安装依赖 pip install -r requirements.txt
	3.mkdir txt
	4.运行程序python search_news.py
# 有待优化项
	1.数据保存(Sqlite) 
		- 已经在shownews 项目中保存为Mysql
	2.函数内部优化
	3.。。。。。

