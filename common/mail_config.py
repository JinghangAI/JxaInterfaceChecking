# -*- coding:utf-8 -*-
# @Time      : 2019.12.27 上午11:00
# @Author    : CuiHanBin
# @File      : mail_config.py

import os
from configparser import ConfigParser

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

cfg = ConfigParser()
cfg.read(path + '/config/mail_config.ini', encoding="utf-8-sig")
sections = cfg.sections()
# 发送者信息
send_user = cfg.get('send', 'send_user')
email_host = cfg.get('send', 'email_host')
password = cfg.get('send', 'password')
# 接收者信息
user_list = cfg.get('receiver', 'user_list')
sub = cfg.get('receiver', 'sub')
content = cfg.get('receiver', 'content')
