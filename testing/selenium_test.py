from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import unittest
import time
import random
import string

class AgroAITest(unittest.TestCase):

    #Initial setup to home page
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://137.48.186.128:8000/")

    #Generate a unique username
    def generate_unique_username(self):
        timestamp = str(int(time.time()))
        random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return timestamp + random_chars

    #Test try now button on home page to navigate to login page
    def test_try_now_button(self):
        try_btn = self.driver.find_element(by=By.ID, value="try-now-btn")
        try_btn.click()
        expected_url = "http://137.48.186.128:8000/login.html"
        actual_url = self.driver.current_url
        self.assertEqual(expected_url, actual_url, f"Expected URL: {expected_url}, Actual URL: {actual_url}")

    #Test here link on login page to navigate to register page
    def test_register_link(self):
        try_btn = self.driver.find_element(by=By.ID, value="try-now-btn")
        try_btn.click()
        here_btn = self.driver.find_element(by=By.CLASS_NAME, value="underline-link")
        here_btn.click()
        expected_url = "http://137.48.186.128:8000/register.html"
        actual_url = self.driver.current_url
        self.assertEqual(expected_url, actual_url, f"Expected URL: {expected_url}, Actual URL: {actual_url}")

    #Test registering a user with a username that is too short
    def test_register_username_short(self):
        try_btn = self.driver.find_element(by=By.ID, value="try-now-btn")
        try_btn.click()
        here_btn = self.driver.find_element(by=By.CLASS_NAME, value="underline-link")
        here_btn.click()
        register_username = self.driver.find_element(by=By.NAME, value="username")
        register_password = self.driver.find_element(by=By.NAME, value="password")
        register_btn = self.driver.find_element(by=By.CSS_SELECTOR, value="button[type='submit']")
        register_username.send_keys("abc")
        register_password.send_keys("password123")
        register_btn.click()
        username_alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        self.assertIn("Username must be at least 4 characters long and can only contain letters and numbers", username_alert.text)
        username_alert.accept()

    #Test registering a user with a username that contains special characters
    def test_register_username_special_chars(self):
        try_btn = self.driver.find_element(by=By.ID, value="try-now-btn")
        try_btn.click()
        here_btn = self.driver.find_element(by=By.CLASS_NAME, value="underline-link")
        here_btn.click()
        register_username = self.driver.find_element(by=By.NAME, value="username")
        register_password = self.driver.find_element(by=By.NAME, value="password")
        register_btn = self.driver.find_element(by=By.CSS_SELECTOR, value="button[type='submit']")
        register_username.send_keys("abcd$")
        register_password.send_keys("password123")
        register_btn.click()
        username_alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        self.assertIn("Username must be at least 4 characters long and can only contain letters and numbers", username_alert.text)
        username_alert.accept()

    #Test registering a user with a password that is too short
    def test_register_password_short(self):
        try_btn = self.driver.find_element(by=By.ID, value="try-now-btn")
        try_btn.click()
        here_btn = self.driver.find_element(by=By.CLASS_NAME, value="underline-link")
        here_btn.click()
        register_username = self.driver.find_element(by=By.NAME, value="username")
        register_password = self.driver.find_element(by=By.NAME, value="password")
        register_btn = self.driver.find_element(by=By.CSS_SELECTOR, value="button[type='submit']")
        register_username.send_keys("autotest")
        register_password.send_keys("1234567")
        register_btn.click()
        password_alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        self.assertIn("Password must be at least 8 characters long", password_alert.text)
        password_alert.accept()

    #Test registering an account successfully, account already exists, and logging in
    def test_register_and_login(self):
        try_btn = self.driver.find_element(by=By.ID, value="try-now-btn")
        try_btn.click()
        here_btn = self.driver.find_element(by=By.CLASS_NAME, value="underline-link")
        here_btn.click()
        register_username = self.driver.find_element(by=By.NAME, value="username")
        register_password = self.driver.find_element(by=By.NAME, value="password")
        register_btn = self.driver.find_element(by=By.CSS_SELECTOR, value="button[type='submit']")
        username = "user" + self.generate_unique_username()[:12]
        register_username.send_keys(username)
        register_password.send_keys("password123")
        register_btn.click()
        success_heading = self.driver.find_element(By.XPATH, "//h1[text()='Your account has been created!']")
        self.assertTrue(success_heading.is_displayed(), "Registration success message not found")
        login_btn = self.driver.find_element(by=By.CLASS_NAME, value="btn")
        login_btn.click()
        expected_url = "http://137.48.186.128:8000/login.html"
        actual_url = self.driver.current_url
        self.assertEqual(expected_url, actual_url, f"Expected URL: {expected_url}, Actual URL: {actual_url}")
        here_btn = self.driver.find_element(by=By.CLASS_NAME, value="underline-link")
        here_btn.click()
        expected_url = "http://137.48.186.128:8000/register.html"
        actual_url = self.driver.current_url
        self.assertEqual(expected_url, actual_url, f"Expected URL: {expected_url}, Actual URL: {actual_url}")
        register_username = self.driver.find_element(by=By.NAME, value="username")
        register_password = self.driver.find_element(by=By.NAME, value="password")
        register_btn = self.driver.find_element(by=By.CSS_SELECTOR, value="button[type='submit']")
        register_username.send_keys(username)
        register_password.send_keys("password1234")
        register_btn.click()
        error_message = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "error_message")))
        self.assertTrue(error_message.is_displayed(), "Error message is not displayed")
        self.driver.get("http://137.48.186.128:8000/login.html")
        login_username = self.driver.find_element(by=By.NAME, value="username")
        login_password = self.driver.find_element(by=By.NAME, value="password")
        login_btn = self.driver.find_element(by=By.CSS_SELECTOR, value="button[type='submit']")
        login_username.send_keys(username)
        login_password.send_keys("password123")
        login_btn.click()
        expected_url = "http://137.48.186.128:8000/label.html"
        actual_url = self.driver.current_url
        self.assertEqual(expected_url, actual_url, f"Expected URL: {expected_url}, Actual URL: {actual_url}")

    def test_invalid_login(self):
        try_btn = self.driver.find_element(by=By.ID, value="try-now-btn")
        try_btn.click()
        login_username = self.driver.find_element(by=By.NAME, value="username")
        login_password = self.driver.find_element(by=By.NAME, value="password")
        login_btn = self.driver.find_element(by=By.CSS_SELECTOR, value="button[type='submit']")
        login_username.send_keys("abc")
        login_password.send_keys("123")
        login_btn.click()
        error_message = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "error_message")))
        self.assertTrue(error_message.is_displayed(), "Error message is not displayed")

    #Test logging out from label page returns user to home page
    def test_label_logout(self):
        try_btn = self.driver.find_element(by=By.ID, value="try-now-btn")
        try_btn.click()
        here_btn = self.driver.find_element(by=By.CLASS_NAME, value="underline-link")
        here_btn.click()
        register_username = self.driver.find_element(by=By.NAME, value="username")
        register_password = self.driver.find_element(by=By.NAME, value="password")
        register_btn = self.driver.find_element(by=By.CSS_SELECTOR, value="button[type='submit']")
        username = "user" + self.generate_unique_username()[:12]
        register_username.send_keys(username)
        register_password.send_keys("password123")
        register_btn.click()
        login_btn = self.driver.find_element(by=By.CLASS_NAME, value="btn")
        login_btn.click()
        login_username = self.driver.find_element(by=By.NAME, value="username")
        login_password = self.driver.find_element(by=By.NAME, value="password")
        login_btn = self.driver.find_element(by=By.CSS_SELECTOR, value="button[type='submit']")
        login_username.send_keys(username)
        login_password.send_keys("password123")
        login_btn.click()
        dropdown = self.driver.find_element(by=By.ID, value="dropdownMenuButton")
        dropdown.click()
        signout_btn = self.driver.find_element(by=By.CLASS_NAME, value="dropdown-item")
        signout_btn.click()
        expected_url = "http://137.48.186.128:8000/index.html"
        actual_url = self.driver.current_url
        self.assertEqual(expected_url, actual_url, f"Expected URL: {expected_url}, Actual URL: {actual_url}")

    #Test navigating to label page directly without logging in takes user to home page
    def test_not_in_session(self):
        self.driver.get("http://137.48.186.128:8000/label.html")
        expected_url = "http://137.48.186.128:8000/login.html"
        actual_url = self.driver.current_url
        self.assertEqual(expected_url, actual_url, f"Expected URL: {expected_url}, Actual URL: {actual_url}")

    #Quit
    def tearDown(self):
        self.driver.quit()

#Execute the tests
if __name__ == "__main__":
    unittest.main()