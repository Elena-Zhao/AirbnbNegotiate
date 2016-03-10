# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from bs4 import BeautifulSoup
import unittest, time, re
import time

class SendOffer(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        chromedriver = "C:\Users\user\Desktop\Harvard\chromedriver_win32"
        #os.environ["webdriver.chrome.driver"] = chromedriver
        #self.driver = webdriver.Chrome(chromedriver)
        self.driver.implicitly_wait(6)
        self.base_url = "https://www.airbnb.it/"
        self.verificationErrors = []
        self.accept_next_alert = True
    

    def test_send_offer(self):
        #TODO: ITERATE OVER THE GIVEN IDS AND SAVE THE RESULTS IN A DATAFRAME
        
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
        driver.get(self.base_url + "/rooms/7124590")
        driver.find_element_by_css_selector("a > strong > span").click()
        driver.find_element_by_css_selector("div.contacted-before > a > span").click()
        
        html = driver.page_source

        soup = BeautifulSoup(html)
        messages = soup.findAll('span', {"class" : "message-text"})

        for msg in messages:
            print msg.text
        
        
        time.sleep(300)  
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
