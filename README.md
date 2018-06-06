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
# 定时计划任务
利用crontab来定时执行本程序 节约人力成本提高效率

- crontab -e(编辑) crontab -l(列出当前用户的计划任务)
- 编辑定时计划任务 f1 f2 f3 f4 f5 script
	- f1 minute  f2 hour f3 day f4 month f5 weekday  script 你的执行程序
	- 例子： 0 8-18/6 \* * * python /home/search_news/search_news.py (每天8点到18点每6个小时执行一次 search_news.py)
	- 这里有个特殊情况  比如我想让程序在 18-8执行  这里不能写0 18-8  计划任务不能跨天执行

[crontab参数说明](http://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/crontab.html)

# 有待优化项
	1.数据保存(Sqlite) 
		- 已经在shownews 项目中保存为Mysql
	2.函数内部优化
	3.。。。。。

