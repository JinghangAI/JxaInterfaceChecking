# -*- coding : utf-8 -*-
# @Time      : 2020.01.04 18:00
# @Author    : CuiHanBin
# @File      : test_001_userLogin.py

import os
import xlrd
import json
import datetime
import requests
import unittest
from xlutils import copy

from common import jh_log
from common.wx_robot import send_msg
from common.jh_form_data import MultipartFormData

log = jh_log.MyLog()
now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class JhApp(unittest.TestCase):

    def test_userLogin_correct(self):
        try:
            case_path = path + "/case/jh_app.xls"
            post_sheet = xlrd.open_workbook(case_path).sheet_by_name('post')
            n_ro4ws, n_cols = post_sheet.nrows, post_sheet.ncols  # sheet页里的行数和列数

        except FileNotFoundError:
            log.error('读取测试用例失败，请检查！！！')
        else:
            request_method = post_sheet.cell(1, 5).value.replace('\n', '').replace('\r', '')
            protocol = post_sheet.cell(1, 2).value.replace('\n', '').replace('\r', '')
            api_host = post_sheet.cell(1, 3).value.replace('\n', '').replace('\r', '')
            user_agent = post_sheet.cell(1, 6).value.replace('\n', '').replace('\r', '')
            content_type = post_sheet.cell(1, 7).value.replace('\n', '').replace('\r', '')
            authorization = post_sheet.cell(1, 10).value.replace('\n', '').replace('\r', '')
            boundary = post_sheet.cell(1, 11).value.replace('\n', '').replace('\r', '')

            line = int(post_sheet.cell(2, 0).value)
            num = str(int(post_sheet.cell(line, 0).value)).replace('\n', '').replace('\r', '')
            api_purpose = post_sheet.cell(line, 1).value.replace('\n', '').replace('\r', '')
            request_path = post_sheet.cell(line, 4).value.replace('\n', '').replace('\r', '')
            request_data = json.loads(post_sheet.cell_value(line, 8).replace('\n', '').replace('\r', ''))
            assertion = json.loads(post_sheet.cell(line, 9).value.replace('\n', '').replace('\r', ''), strict=False)
            msg = post_sheet.cell(line, 12).value.replace('\n', '').replace('\r', '')

            url = ''.join((protocol, api_host, request_path))
            request_data = MultipartFormData.format(data=request_data, boundary=boundary)
            headers = {'User-Agent': user_agent, 'Content-Type': content_type}

            result = requests.post(url, data=request_data, headers=headers)
            result_text = result.text

            result_err = str('请求方法：' + request_method + '\n' + '请求地址：' + result.url + '\n' +
                             '请求参数：' + request_data + '\n' + '返回结果：' + result_text)
            send_err = '接口异常，请检查接口或服务！！' + '\n' + now_time + '\n' + result_err

            try:
                result_dict = json.loads(result_text)
            except json.decoder.JSONDecodeError:
                send_msg(send_err)
                log.error('The interface status code is incorrect!!!')
            else:
                if 'token' in result_dict:
                    rbook = xlrd.open_workbook(case_path, formatting_info=True)  # token每次重新写入
                    wbook = copy.copy(rbook)
                    post_sheet = wbook.get_sheet('post')
                    row = 1
                    col = 10
                    token = result_dict['token']
                    post_sheet.write(row, col, 'Bearer ' + token)

                    get_sheet = wbook.get_sheet('get')
                    row = 1
                    col = 9
                    token = result_dict['token']
                    get_sheet.write(row, col, 'Bearer ' + token)
                    wbook.save(case_path)  # 保存文件

                    if result.status_code == 200:
                        if 'code' in result_dict:
                            code_value = result_dict['code']
                            if code_value != '200':
                                send_msg(send_err)
                        else:
                            send_msg(send_err)
                        if 'data' in result_dict:
                            data_value = result_dict['data']
                            for k, v in assertion.items():
                                self.assertEqual(v, data_value[k], send_err + '返回值的data和期望值不同')
                            print(result_text)
                        else:
                            send_msg(send_err)
                    else:
                        log.error(result_err)
                        send_msg(send_err)
                else:
                    print(result_text)


if __name__ == '__main__':
    unittest.main()
