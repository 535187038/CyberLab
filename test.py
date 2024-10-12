#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : CyberLab
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test_cases.DesiredCapsParser import DesiredCapsParser


# HINT: fixtures below could be extracted into conftest.py
# HINT: and shared across all tests in the suite
@pytest.fixture(scope="class")
def driver() -> webdriver.Remote:
    """Fixture to set up and teardown the appium driver."""
    desired_caps = DesiredCapsParser().get_desired_caps()
    options = UiAutomator2Options().load_capabilities(desired_caps)
    options.no_reset = False
    url = DesiredCapsParser().get_url()
    print("url----",url)
    driver = None
    if not (options is None) and not (url is None):
        try:
            driver = webdriver.Remote(url, options=options)
            driver.implicitly_wait(3)
            yield driver
        finally:
            if driver:
                driver.quit()


class TestExample:

    def test_app_is_open(self, driver):
        """ Check if the CyberLab Sample is on the main page"""
        # HINT: use resource id to locate the element
        target_resource_id = "com.pax.us.pay.std.cyberlab:id/et_amount_prompt"
        target_text = "Transaction Amount ($)"
        text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ID, target_resource_id))
        ).text

        assert text == target_text

    def test_simple_case(self, driver):
        pass
