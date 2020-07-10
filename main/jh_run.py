#!/usr/bin/env python
# -*- coding : utf-8 -*-
# @Time      : 2019.12.11 15:00
# @Author    : CuiHanBin
# @File      : jh_run.py

import os
import sys
import time
import unittest
from common import jh_log
from common import HTMLTestRunner
# from common.jh_send_mail import SendEmail

log = jh_log.MyLog()
this_path = os.path.split(os.path.abspath(__file__))[0]
case_script_path = os.path.join(this_path, '../case_script')
report_path = os.path.join(case_script_path, '../report')


class JhRunMain:
    def __init__(self):
        print('---开始执行测试用例---')
        # self.send_mail = SendEmail()

    def run_case(self):
        # discover = unittest.defaultTestLoader.discover(case_script_path, pattern='test_000_sendSms.py')
        discover = unittest.defaultTestLoader.discover(case_script_path, pattern='test_*.py')
        # now_time = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime(time.time()))  # 获取当前时间
        # report_abspath = os.path.join(report_path, "result_" + now_time + ".html")
        report_abspath = os.path.join(report_path, "jh_app_report" + ".html")
        report = open(report_abspath, 'wb')      # 打开一个保存结果的html文件
        HTMLTestRunner.HTMLTestRunner(stream=report,
                                      verbosity=2,
                                      title=u'鲸小爱APP接口测试报告,测试结果如下：',
                                      description=u'接口自动化测试报告').run(discover)  # retry=1失败后，重跑1次生成执行用例的对象
        report.close()
        # try:
        #     self.send_mail.send_main()
        # except Exception as e:
        #     log.error('发送邮件失败，请检查邮箱配置')
        #     raise


if __name__ == '__main__':
    runner = JhRunMain()
    runner.run_case()
