# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import time
import random

class SendOffer(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        #chromedriver = "C:\Users\user\Desktop\Harvard\chromedriver_win32"
        #os.environ["webdriver.chrome.driver"] = chromedriver
        #self.driver = webdriver.Chrome(chromedriver)
        self.driver.implicitly_wait(15)
        self.base_url = "https://www.airbnb.it/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_send_offer(self):
        #TO DO: ITERATE OVER THE GIVEN IDS AND DATES
        
        driver = self.driver
        #login
        driver.get(self.base_url + "")
        driver.find_element_by_link_text("Accedi").click()
        driver.find_element_by_id("signin_email").clear()
        driver.find_element_by_id("signin_email").send_keys("michele.invernizzi90@gmail.com")
        driver.find_element_by_id("signin_password").clear()
        driver.find_element_by_id("signin_password").send_keys("datashackAirbnb2016")
        #driver.find_element_by_id("user-login-btn").click()
        time.sleep(15)
        driver.get(self.base_url)
        time.sleep(10)
        driver.get(self.base_url + "/rooms/178131?check_in=2016-03-11&guests=1&check_out=2016-03-14")
        driver.find_element_by_css_selector("a > strong > span").click()
        time.sleep(10)
        driver.find_element_by_name("question").clear()
        driver.find_element_by_name("question").send_keys("Airbnb team; test ")
        driver.find_element_by_xpath("(//button[@type='submit'])[4]").click()
        driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
        
        time.sleep(random.uniform(0.5, 60))
        
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
