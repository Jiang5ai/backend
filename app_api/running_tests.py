import os
import unittest
import requests
from ddt import ddt, data, file_data, unpack

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
    def test_case(self, url, method, params_type, params_body):
        if method == "GET":
            r = requests.get(url, params=params_body)
        elif method == "POST":
            if params_type == "json":
                r = requests.post(url, json=params_body)
            elif params_type == "data":
                r = requests.post(url, data=params_body)
            else:
                r = "{}"
        else:
            r = "{}"
