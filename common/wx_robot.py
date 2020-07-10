#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/7/7 11:59
# @Author   : CuiHanBin
# @File     : wx_robot.py

import os
import sys
import json
import requests
from configparser import ConfigParser

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

cfg = ConfigParser()
cfg.read(path + '/config/robot_config.ini', encoding="utf-8-sig")
sections = cfg.sections()

wx_url = cfg.get('robot', 'wx_url')
send_message = cfg.get('robot', 'send_message')


def send_msg(content):
    """@all，并发送指定信息"""
    data = json.dumps({"msgtype": "text", "text": {"content": content, "mentioned_list": ["@all"]}})
    r = requests.post(wx_url, data, auth=('Content-Type', 'application/json'))
    print(r.json)


# if __name__ == '__main__':
#     send_msg(send_message)
