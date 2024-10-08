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

def test():
  num1 = 1
  num2 = 2
  sum = num1 + num2
  return sum
