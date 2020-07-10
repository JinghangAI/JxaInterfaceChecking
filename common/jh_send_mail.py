# -*- coding : utf-8 -*-
# @Time      : 2019.12.11 17:00
# @Author    : CuiHanBin
# @File      : jh_send_mail.py

import os
import smtplib
import datetime
from email.header import Header                # 用来设置邮件头和邮件主题
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from common import mail_config


class SendEmail:
    global send_user
    global email_host
    global password
    password = mail_config.password
    email_host = mail_config.email_host
    send_user = mail_config.send_user

    def send_email(self, user_list, sub, content):
        user = "jh_app_api" + "<" + send_user + ">"
        # 创建一个带附件的实例
        message = MIMEMultipart()
        message['Subject'] = Header(sub, 'utf-8')  # 邮件主题
        # message['Subject'] = sub
        message['From'] = user
        message['To'] = ",".join(user_list)

        # 邮件正文内容
        message.attach(MIMEText(content, 'plain', 'utf-8'))

        # 构造附件（附件为HTML格式的网页）
        filename = r'../report\jh_app_report.html'
        time = datetime.date.today()
        att = MIMEText(open(filename, 'rb').read(), 'html', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="%s_jh_app_report.html"' % time
        message.attach(att)

        server = smtplib.SMTP_SSL(email_host)
        server.connect(email_host)  # 启用SSL发信, 端口一般是465,25
        # server.set_debuglevel(1)  # 打印出和SMTP服务器交互的所有信息
        server.login(send_user, password)
        server.sendmail(user, user_list, message.as_string())
        server.close()

    def send_main(self):
        user_list = mail_config.user_list
        sub = mail_config.sub
        content = mail_config.content
        self.send_email(user_list.split(','), sub, content)
