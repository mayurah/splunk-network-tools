# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Whois(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_whois(self):
        driver = self.driver
        driver.get(self.base_url + "/en-US/app/network_tools/whois")
        for i in range(60):
            try:
                if driver.find_element_by_id("content1").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if not driver.find_element_by_id("tab_whois_controls").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        for i in range(60):
            try:
                if 0 == len(driver.find_elements_by_css_selector(".alert-info")): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        driver.find_element_by_link_text("Execute Whois").click()
        for i in range(60):
            try:
                if driver.find_element_by_id("execute_input").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        driver.find_element_by_css_selector("#host_input input").clear()
        driver.find_element_by_css_selector("#host_input input").send_keys("google.com")
        driver.find_element_by_id("execute_input").click()
        # The following wait for the single value to change to a state of running and then back
        for i in range(60):
            try:
                if driver.find_element_by_css_selector("#tab_whois_data .results-table tbody tr:nth-child(3) td").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        # Test the result (make sure it has at least some rows)
        self.assertEqual(2, len(driver.find_elements_by_css_selector("#tab_whois_data .results-table tbody tr:nth-child(3) td")))
        # Now try a different site and make sure it works too
        driver.find_element_by_css_selector("#host_input input").clear()
        driver.find_element_by_css_selector("#host_input input").send_keys("textcritical.net")
        driver.find_element_by_id("execute_input").click()
        for i in range(60):
            try:
                if "Wadsworth" == driver.find_element_by_css_selector("#tab_whois_data tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.assertEqual("Wadsworth", driver.find_element_by_css_selector("#tab_whois_data tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)").text)
    
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
