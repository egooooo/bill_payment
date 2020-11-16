import logging
import sys
import unittest

import requests
import urllib3



class SmokeTests(unittest.TestCase):
    def testEndPointExist(self):
        logging.info("Ensuring endpoints exist")
        self.assertEqual(SmokeTests.get("http://127.0.0.1:5000/").status_code, 200)

    @staticmethod
    def get(url):
        return requests.get(url, verify=False)
