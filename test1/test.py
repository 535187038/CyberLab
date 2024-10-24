import unittest
import os
from appium import webdriver
from cyberium.accessory import AccessoryApi
from appium.options.android import UiAutomator2Options
from test_cases.DesiredCapsParser import DesiredCapsParser

class SimpleTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.desired_caps = DesiredCapsParser().get_desired_caps()

        options = UiAutomator2Options().load_capabilities(cls.desired_caps)
        options.no_reset = False

        cls.url = DesiredCapsParser().get_url()
        cls.driver = webdriver.Remote(cls.url, options=options)
        cls.token = cls.desired_caps['token']
        cls.device_id = cls.desired_caps['deviceId']
        cls.api = AccessoryApi(token=cls.token, device_id=cls.device_id)

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()

    def test_simple_case(self):
        pass
