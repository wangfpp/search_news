# -*- coding: utf-8 -*-
# @Author: wangfpp
# @Date:   2018-08-11 10:50:59
# @Last Modified by:   wangfpp
# @Last Modified time: 2018-08-11 13:03:51
import smtplib
from email.mime.text import MIMEText
from email.header import Header
 
sender = 'wangfpp@gmail.com'
receivers = ['285887933@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
 
# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = Header("菜鸟教程", 'utf-8')   # 发送者
message['To'] =  Header("测试", 'utf-8')        # 接收者
 
subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')
 
 

smtpObj = smtplib.SMTP('smtp.gmail.com:25')
smtpObj.login('wangfpp@gmail.com', 'W099001205010')
smtpObj.sendmail(sender, receivers, message.as_string())