# -*- coding : utf-8 -*-
# @Time      : 2020.02.06 11:30
# @Author    : CuiHanBin
# @File      : test_024_getIListenByType5.py

import os
import xlrd
import json
import requests
import unittest
import logging


class JhApp(unittest.TestCase):

    @unittest.skip("Interface discarding")
    def test_getIListenByType5_correct(self):
        try:
            case_path = path + "/case/jh_app.xls"
            get_sheet = xlrd.open_workbook(case_path).sheet_by_name('get')
            n_ro4ws, n_cols = get_sheet.nrows, get_sheet.ncols  # 分别为sheet页里的行数和列数

        except FileNotFoundError:
            logging.error('读取测试用例失败，请检查！！！')
        else:
            request_method = get_sheet.cell(1, 5).value.replace('\n', '').replace('\r', '')
            protocol = get_sheet.cell(1, 2).value.replace('\n', '').replace('\r', '')
            api_host = get_sheet.cell(1, 3).value.replace('\n', '').replace('\r', '')
            user_agent = get_sheet.cell(1, 6).value.replace('\n', '').replace('\r', '')
            authorization = get_sheet.cell(1, 9).value.replace('\n', '').replace('\r', '')

            line = int(get_sheet.cell(23, 0).value)
            num = str(int(get_sheet.cell(line, 0).value)).replace('\n', '').replace('\r', '')
            api_purpose = get_sheet.cell(line, 1).value.replace('\n', '').replace('\r', '')
            request_path = get_sheet.cell(line, 4).value.replace('\n', '').replace('\r', '')
            request_data = get_sheet.cell_value(line, 7).replace('\n', '').replace('\r', '')
            # assertion = json.loads(get_sheet.cell(line, 8).value.replace('\n', '').replace('\r', ''), strict=False)
            msg = get_sheet.cell(line, 10).value.replace('\n', '').replace('\r', '')
            get_end = get_sheet.cell(line, 11).value.replace('\n', '').replace('\r', '')

            url = ''.join((protocol, api_host, request_path))
            headers = {'User-Agent': user_agent, 'authorization': authorization}

            result = requests.get(url, data=request_data, headers=headers)
            result_text = result.text
            result_dict = json.loads(result_text)
            print(result_text)

            # if result.status_code == 200:
            #     if 'code' in result_dict:
            #         code_value = result_dict['code']
            #         self.assertEqual(int(code_value), 200, code_value + '---code码不正确，不为200')
            #     else:
            #         print('请求方法：' + request_method + '\n', '请求地址：' + result.url + '\n',
            #               '请求参数：' + request_data + '\n', '返回结果：' + result_text)
            #     if 'data' in result_dict:
            #         data_value = result_dict['data']['types'][0]
            #         for k, v in assertion.items():
            #             # self.assertIn(v, data_value[k], k + '---错误')
            #             self.assertEqual(v, data_value[k], k + '---错误')
            #         msg_value = result_dict['msg']
            #         self.assertEqual(msg, msg_value, 'msg:' + msg_value)
            #         print(result_text)
            #     else:
            #         print('请求方法：' + request_method + '\n', '请求地址：' + result.url + '\n',
            #               '请求参数：' + request_data + '\n', '返回结果：' + result_text)
            # else:
            #     print('http状态码是：' + result.status_code)
            #     print('请求方法：' + request_method + '\n', '请求地址：' + result.url + '\n',
            #           '请求参数：' + request_data + '\n', '返回结果：' + result_text)


if __name__ == '__main__':
    unittest.main()
