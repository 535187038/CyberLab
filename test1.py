# -*- coding: UTF-8 -*-
import functools
import random
import time
import traceback
import unittest

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from cyberium.accessory import AccessoryApi
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from test_cases.DesiredCapsParser import DesiredCapsParser


def case_exception():
    def wrapper(func):
        @functools.wraps(func)
        def wrapper_(self, *args):
            try:
                func(self, *args)
            except Exception as e:
                if self.not_removed:
                    self.api.remove_card(self.card)
                traceback.print_exc()
                self.driver.close_app()
                self.driver.launch_app()
                if not self.printable:
                    self.wait.until(lambda x: x.find_element(
                        AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cancel")')).click()
                raise e

        return wrapper_

    return wrapper


class TransactionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.desired_caps = DesiredCapsParser().get_desired_caps()
        cls.url = DesiredCapsParser().get_url()
        cls.driver = webdriver.Remote(cls.url, cls.desired_caps)
        cls.token = cls.desired_caps['token']
        cls.device_id = cls.desired_caps['deviceId']
        cls.api = AccessoryApi(token=cls.token, device_id=cls.device_id)
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.api.inject_dukpt_key(1, 'FFFF5B0999000000', ('0000000000000000', '0000000000000000'),
                                 ('0000000000000000', '0000000000000000'))
        cls.not_removed = False
        # connect to BP60A
        try:
            cls.wait.until(lambda x: x.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cancel")')).click()
            cls.printable = False
        except WebDriverException:
            cls.printable = True

    def setUp(self) -> None:
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    @case_exception()
    def test1_credit_sale_swipe(self):

        self.wait.until(lambda x: x.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("CREDIT")')).click()
        # Click Credit Sale
        self.wait.until(lambda x: x.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("SALE")')).click()
        # Wait For Amount Menu
        self.wait.until(lambda x: x.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Please Enter Amount")'))
        # Input Transaction Amount
        self.wait.until(lambda x: x.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText")')
                        ).send_keys('200')
        # Confirm
        self.wait.until(lambda x: x.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("CONFIRM")')).click()

        # Wait For Account Menu
        self.wait.until(lambda x: x.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                                 'new UiSelector().textContains("Please Enter Account")'))
        start_time = int(round(time.time() * 1000))
        # Input Card Account Number
        result, msg = self.api.swipe_card('4012000033330026=3012')
        self.assertEqual(result, True, msg)

        # Signature
        self.wait.until(lambda x: x.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("PLS Sign Your Name")'))
        self.driver.swipe(100, 500, 100, 600, 500)
        time.sleep(0.5)
        self.wait.until(lambda x: x.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.pax.us.pay.std.cyberlab:id/confirm_btn")')
                        ).click()
        # Print receipt
        if self.printable:
            self.wait.until(lambda x: x.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("OK")')).click()
        self.get_receipt_data(start_time)
