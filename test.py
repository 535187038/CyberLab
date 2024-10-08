#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : CyberLab
import pytest
import os
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException


# HINT: fixtures below could be extracted into conftest.py
# HINT: and shared across all tests in the suite
@pytest.fixture(scope="session")
def driver() -> webdriver.Remote:
    """Fixture to setup and teardown the appium driver."""
    options = UiAutomator2Options()
    options.platform_version = '7.1.1'
    # options.udid = os.getenv("udid")
    options.device_name = os.getenv("deviceName")
    options.app_package = 'com.pax.us.pay.std.cyberlab'
    options.app_activity = 'com.pax.pay.ui.SplashActivity'
    options.no_reset = False

    appium_url = "127.0.0.1:4723"
    driver = None
    try:
        driver = webdriver.Remote(f'http://{appium_url}', options=options)
        driver.implicitly_wait(3)
        yield driver
    finally:
        if driver:
            driver.quit()


class TestExample:

    def test_app_is_open(self, driver):
        """Test Case 1: Check if the App is on the main page"""
        target_resource_id = "com.pax.us.pay.std.cyberlab:id/et_amount_prompt"  # HINT: use resource id to locate the element
        target_text = "Transaction Amount ($)"
        text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ID, target_resource_id))
        ).text

        assert text == target_text

    def test_case2(self):
        pass

    @pytest.mark.parametrize("i, amount", [(1, "1111"), (2, "2222")])
    def test_manual_input_card_number(self, driver, i, amount):
        """测试用例2：手动输入卡号的交易Demo"""
        # 进入Credit - SALE, 输入金额
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("SALE")'))
        ).click()
        driver.find_element(AppiumBy.ID, "com.pax.us.pay.std.cyberlab:id/amount_edt").send_keys(amount)
        driver.find_element(AppiumBy.ID, "com.pax.us.pay.std.cyberlab:id/credit_sale_btn").click()

        # 确认金额后输卡号
        if amount == driver.find_element(AppiumBy.ID, "com.pax.us.pay.std.cyberlab:id/amount_tv").text:
            pass
        # driver.find_element(AppiumBy.ID, "com.pax.us.pay.std.cyberlab:id/cardNum_edt").click()
        # 应用限制，必须使用数字键盘输入卡号
        for s in "4012000033330026":
            driver.press_keycode(int(s) + 7)
            time.sleep(0.2)
        driver.press_keycode(66)  # ENTER
        # driver.find_element(AppiumBy.ID, "com.pax.us.pay.std.cyberlab:id/confirm_btn").click()

        # 输入卡号有效期
        driver.find_element(AppiumBy.ID, "com.pax.us.pay.std.cyberlab:id/amount_edt").send_keys("1212")
        driver.find_element(AppiumBy.ID, "com.pax.us.pay.std.cyberlab:id/credit_sale_btn").click()

        driver.find_element(AppiumBy.ID, "com.pax.us.pay.std.cyberlab:id/confirm_btn").click()
        # 输入卡号校验码CVV
        driver.find_element(AppiumBy.ID, "com.pax.us.pay.std.cyberlab:id/amount_edt").send_keys("123")
        driver.find_element(AppiumBy.ID, "com.pax.us.pay.std.cyberlab:id/credit_sale_btn").click()

        # 等待交易处理，签名
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (AppiumBy.ID, "com.pax.us.pay.std.cyberlab:id/trans_amount_tv")))
        # driver.find_element(AppiumBy.ID, "com.pax.us.pay.std.cyberlab:id/tv_text_signature")
        driver.swipe(100, 500, 100, 600, 500)
        driver.find_element(AppiumBy.ID, "com.pax.us.pay.std.cyberlab:id/confirm_btn").click()

        success_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ID, "com.pax.us.pay.std.cyberlab:id/title_text"))
        ).text

        assert 'Tear Slip?' == success_text

        try:
            driver.find_element(AppiumBy.ID, "com.pax.us.pay.std.cyberlab:id/confirm_button").click()
        except NoSuchElementException:
            pass
