# 起点中文网小说爬虫说明

# 项目背景:
	1.起点中文网的小说获取增加样本

# 使用
	1.安装Python python2.7
	2.依赖Mysql
	3.bs4
	4.运行程序python search_book.py
# 说明
	1.每个小说为一个文件夹 
	2.文件夹下以每一章节命名的txt文件
	3.不会重复爬虫 也就是说小说更新只要网址不变就不会重复获取
	4.利用Mysql存储已经爬取的章节URL
# 有待优化项
	1.增加项目日志的输出
	2.优化代码

# 遇到的问题
	在Mysql INSERT TABLE (some) VALUES (?) 插入数据时要执行一次db.commit()
	不然不能成功插入数据

