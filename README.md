##中国新闻网爬虫说明
##项目背景:##
	1.OCR识别可能会出现语义不通的情况
	2.根据语义模型来纠正OCR的识别结果
	3.从新闻网站获取大量的文字来训练语义模型

##使用
	1.安装Python python2.7
	2.安装依赖 pip install -r requirements.txt
	3.运行程序python search.py
##有待优化项
	1.极少数的txt乱码问题
	2.数据保存问题(使用MySql来存储数据)
	3.文件保存时浪费cpu资源(优化代码)
