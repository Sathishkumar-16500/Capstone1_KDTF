from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from yaml_function import orange_yaml

yaml_file = "D:\\KDTF\\config.yaml"

orange_data = orange_yaml(yaml_file).yaml_reader()

class Test_orange_hrm:
    @pytest.fixture
    def booting_function(self):
        self.driver=webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        self.wait=WebDriverWait(self.driver,10)
        self.driver.maximize_window()
        yield
        self.driver.close()

    @pytest.fixture
    def login(self, booting_function):
        self.driver.get(orange_data['url'])
        self.wait.until(
            EC.presence_of_element_located((By.NAME,orange_data['username_locator']))).send_keys(
            orange_data['username'])
        self.driver.find_element(by=By.NAME, value=orange_data['password_locator']).send_keys(orange_data['password'])
        self.driver.find_element(by=By.XPATH, value=orange_data['submitButton_locator']).click()

    def test_login(self, booting_function):
        self.driver.get(orange_data['url'])
        self.wait.until(
            EC.presence_of_element_located((By.NAME,orange_data['username_locator']))).send_keys(
            orange_data['username'])
        self.driver.find_element(by=By.NAME, value=orange_data['password_locator']).send_keys(orange_data['password'])
        self.driver.find_element(by=By.XPATH, value=orange_data['submitButton_locator']).click()

        if 'https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index' in self.driver.current_url:
            print("success: Logged in with username {a} and password {b}".format(a=orange_data['username'],b=orange_data['password']))
        else:
            print("Failure: Unable to login with username {a} and password {b}".format(a=orange_data['username'],
                                                                                 b=orange_data['password']))

    def test_invalid_login(self,booting_function):
        self.driver.get(orange_data['url'])
        self.wait.until(
            EC.presence_of_element_located((By.NAME, orange_data['username_locator']))).send_keys(
            orange_data['invalid_username'])
        self.driver.find_element(by=By.NAME, value=orange_data['password_locator']).send_keys(orange_data['invalid_password'])
        self.driver.find_element(by=By.XPATH, value=orange_data['submitButton_locator']).click()
        result=self.wait.until(EC.presence_of_element_located((By.XPATH,orange_data['invalid_alert'])))
        if result:
            print('SUCCESS: cannot able to login with invalid credentials username {a} and password {b}'.format(a=orange_data['invalid_username'],b=orange_data['invalid_password']))
        else:
            print('FAILURE: can able to login with invalid credentials username {a} and password {b}'.format(a=orange_data['invalid_username'],b=orange_data['invalid_password']))

    def test_add_new_user(self,booting_function,login):
        self.wait.until(EC.presence_of_element_located((By.XPATH,orange_data['pim_tab']))).click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, orange_data['add_button']))).click()
        self.wait.until(EC.presence_of_element_located((By.XPATH,orange_data['firstname_textbox']))).send_keys(orange_data['test_first_name'])
        self.wait.until(EC.presence_of_element_located((By.XPATH, orange_data['middlename_textbox']))).send_keys(orange_data['test_middle_name'])
        self.wait.until(EC.presence_of_element_located((By.XPATH, orange_data['lastname_textbox']))).send_keys(orange_data['test_last_name'])






