import os
import sys

sys.path.append(r"c:\users\13993\appdata\local\programs\python\python38\lib\site-packages")

import xmlrunner
import unittest
import requests
from ddt import ddt, file_data, unpack

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE_PATH = os.path.join(TEST_DIR, "data", "test_data.json")
REPORT_FILE_PATH = os.path.join(TEST_DIR, "data", "report.xml")


# Create your tests here.
@ddt
class Mytest(unittest.TestCase):
    @unpack
    @file_data(DATA_FILE_PATH)
    # @data(
    #     {"url": "http://httpbin.org/get", "method": "GET", "params_type": "json", "params_body": {"id": 111}},
    #     {"url": "http://httpbin.org/post", "method": "POST", "params_type": "json", "params_body": {"id": 111}},
    #     {"url": "http://httpbin.org/post", "method": "POST", "params_type": "json", "params_body": {"id": 111}},
    # )
    def test_case(self, url, method, params_type, params_body, header, assert_type, assert_text):
        """
         "case2": {
        "url": "http://httpbin.org/post",
        "method": "POST",
        "header": null,
        "params_type": "form",
        "params_body": "{'key':'interface'}",
        "assert_type": "equal",
        "assert_text": "httpbin.org"
        },
        """
        if header == "{}":
            header = {}
        if method == 'GET':
            ret_text = requests.get(url=url, params=params_body, headers=header)
            if assert_type == "include":
                self.assertIn(assert_text, ret_text)
            elif assert_type == "equal":
                self.assertEqual(assert_text, ret_text)
            else:
                pass
        if method == 'POST':
            if params_type == 'form':
                ret_text = requests.post(url=url, data=params_body, headers=header)
                if assert_type == "include":
                    self.assertIn(assert_text, ret_text)
                elif assert_type == "equal":
                    self.assertEqual(assert_text, ret_text)
                else:
                    pass
            if params_type == 'json':
                ret_text = requests.post(url=url, json=params_body, headers=header)
                if assert_type == "include":
                    self.assertIn(assert_text, ret_text)
                elif assert_type == "equal":
                    self.assertEqual(assert_text, ret_text)
                else:
                    pass
        if method == 'PUT':
            if params_type == 'form':
                ret_text = requests.put(url=url, data=params_body, headers=header)
                if assert_type == "include":
                    self.assertIn(assert_text, ret_text)
                elif assert_type == "equal":
                    self.assertEqual(assert_text, ret_text)
                else:
                    pass
            if params_type == 'json':
                ret_text = requests.put(url=url, json=params_body, headers=header)
                if assert_type == "include":
                    self.assertIn(assert_text, ret_text)
                elif assert_type == "equal":
                    self.assertEqual(assert_text, ret_text)
                else:
                    pass


if __name__ == '__main__':
    with open(REPORT_FILE_PATH, 'wb') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False
        )
