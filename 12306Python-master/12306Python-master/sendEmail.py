# -*- coding:utf-8 -*-

"""
@time: 2018-01-17
@author: Skyge
"""

"""
Function:
    If book tickets successfully,then send an email to notice you!
"""

import smtplib
from email.header import Header
from email.mime.text import MIMEText

mail_host = "smtp.163.com"      # SMTP服务器
mail_user = "hujingbo16@163.com"       # 用户名
mail_pass = "xxx"               # 授权密码（非登录密码）