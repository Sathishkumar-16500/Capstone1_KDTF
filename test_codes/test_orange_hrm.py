from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
import time
import pytest
from yaml_function import orange_yaml
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

yaml_file = "D:\\Capstone1_KDTF\\config.yaml"
data_file='D:\\Capstone1_KDTF\\data_config.yaml'
locators_file='D:\\Capstone1_KDTF\\locators_config.yaml'

orange_data = orange_yaml(yaml_file).yaml_reader()
data = orange_yaml(data_file).yaml_reader()
locators = orange_yaml(locators_file).yaml_reader()


class Test_orange_hrm:
    @pytest.fixture
    def booting_function(self):
        self.driver=webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        self.wait=WebDriverWait(self.driver,10)
        self.action = ActionChains(self.driver)
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
            assert True
        else:
            print('FAILURE: can able to login with invalid credentials username {a} and password {b}'.format(a=orange_data['invalid_username'],b=orange_data['invalid_password']))
            assert False
    def test_add_new_user(self,booting_function,login):
        result=None
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH,orange_data['pim_tab']))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, orange_data['add_button']))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH,orange_data['firstname_textbox']))).send_keys(orange_data['test_first_name'])
            self.wait.until(EC.presence_of_element_located((By.XPATH, orange_data['middlename_textbox']))).send_keys(orange_data['test_middle_name'])
            self.wait.until(EC.presence_of_element_located((By.XPATH, orange_data['lastname_textbox']))).send_keys(orange_data['test_last_name'])
            self.driver.find_element(by=By.XPATH, value=orange_data['save_button']).click()
            # self.wait.until(EC.presence_of_element_located((By.XPATH, orange_data['added_user_toast'])))
            result = self.wait.until(EC.presence_of_element_located((By.XPATH, orange_data['added_user_toast'])))
        except Exception as e:
            print('error occurred:', e)
        if result:
            print("success: user created and add with firstname {a},middlename {b},lastname {c}".format(
                a=orange_data['test_first_name'], b=orange_data['test_middle_name'],
                c=orange_data['test_last_name']))
            assert True
        else:
            print("failure: Cannot able to create and add user with firstname {a},middlename {b},lastname {c}".format(
                a=orange_data['test_first_name'], b=orange_data['test_middle_name'],
                c=orange_data['test_last_name']))
            assert False

    def test_edit_employee_details(self,booting_function,login):
        result=None
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH,orange_data['pim_tab']))).click()
            self.wait.until(
                EC.presence_of_element_located((By.XPATH,orange_data['edit_button']))).click()
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH,orange_data['edit_firstname_textbox']))).send_keys(
                orange_data['test_first_name'])
            self.driver.find_element(by=By.XPATH,
                                     value=orange_data['edit_middlename_textbox']).send_keys(
                orange_data['test_middle_name'])
            self.driver.find_element(by=By.XPATH, value=orange_data['edit_lastname_textbox']).send_keys(
                orange_data['test_last_name'])
            self.driver.find_element(by=By.XPATH,
                                     value=orange_data['edit_employee_id_textbox']).send_keys(
                orange_data['test_employee_id'])
            self.driver.find_element(by=By.XPATH,
                                     value=orange_data['edit_employee_details_save']).click()
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, orange_data['edit_employee_toast'])))
            result = EC.presence_of_element_located((By.XPATH, orange_data['edit_employee_toast']))
        except Exception as e:
            print('error occured',e)

        if result:
            print(
                "success: user details edit and saved with firstname {a},middlename {b},lastname {c}, employee_id {d}".format(
                    a=orange_data['test_first_name'], b=orange_data['test_middle_name'],
                    c=orange_data['test_last_name'], d=orange_data['test_employee_id']))
            assert True
        else:
            print(
                "failure: Cannot edit and save user details with firstname {a},middlename {b},lastname {c}, employee_id {d}".format(
                    a=orange_data['test_first_name'], b=orange_data['test_middle_name'],
                    c=orange_data['test_last_name'], d=orange_data['test_employee_id']))
            assert False
    def test_delete_employee(self,booting_function,login):
        result=None
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH,orange_data['pim_tab']))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, orange_data['delete_user_button']))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, orange_data['confirm_delete_button']))).click()
            result=self.wait.until(EC.presence_of_element_located((By.XPATH, orange_data['deleted_user_toast'])))
        except Exception as e:
            print('error occured',e)
        if result:
            print("success: employee deleted successfully")
            assert True
        else:
            print("failure: Cannot able to delete employee")
            assert False

    def test_admin_search_validation(self,booting_function,login):
        self.wait.until(EC.presence_of_element_located((By.XPATH, locators['admin_tab']))).click()
        #--------verifying menu options are present
        menu_options_flag=self.wait.until(EC.presence_of_element_located((By.XPATH, locators['menu_options'])))
        #--------verifying search bar is present
        search_bar_flag = self.wait.until(EC.presence_of_element_located((By.XPATH, locators['search_bar'])))
        time.sleep(3)

        small_tabs_flag_list=[]
        caps_tabs_flag_list = []

        #-------verifying the individual menus are present after search in lower_case
        for i in range(len(locators['small_tabs'])):
            try:
                search=self.wait.until(EC.presence_of_element_located((By.XPATH, locators['search_bar'])))
                search.send_keys(Keys.CONTROL + "a")
                search.send_keys(Keys.DELETE)
                time.sleep(1)
                search.send_keys(locators['small_tabs'][i])
                time.sleep(1)
                self.wait.until(EC.presence_of_element_located((By.XPATH, locators['tabs_xpath'][i])))
                print(locators['small_tabs'][i],"menu_option found")
                small_tabs_flag_list.append(True)

            except TimeoutException:
                print(locators['small_tabs'][i], "menu_option not found")
                small_tabs_flag_list.append(False)
        small_tab_flag=all(small_tabs_flag_list)
        print('-------------------------------###############################------------------------------')
        # -------verifying the individual menus are present after search in upper_case
        for i in range(len(locators['caps_tabs'])):
            try:
                search=self.wait.until(EC.presence_of_element_located((By.XPATH, locators['search_bar'])))
                search.send_keys(Keys.CONTROL + "a")
                search.send_keys(Keys.DELETE)
                time.sleep(1)
                search.send_keys(locators['caps_tabs'][i])
                time.sleep(1)
                self.wait.until(EC.presence_of_element_located((By.XPATH, locators['tabs_xpath'][i])))
                print(locators['caps_tabs'][i],"menu_option found")
                caps_tabs_flag_list.append(True)

            except TimeoutException:
                print(locators['caps_tabs'][i],"menu_option not found")
                caps_tabs_flag_list.append(False)
        caps_tab_flag=all(caps_tabs_flag_list)

        # -------combining all the result to validate the testcase
        result=[search_bar_flag,menu_options_flag,small_tab_flag,caps_tab_flag]

        if all(result):
            print("#-----Test_case_passed-----#")
            assert True
        else:
            print("#-----Test_case_failed-----#")
            assert False

    def test_user_management_dropdown_validation(self,booting_function,login):
        self.wait.until(EC.presence_of_element_located((By.XPATH, locators['admin_tab']))).click()
        # --------verifying menu options are present
        # menu_options_flag = self.wait.until(EC.presence_of_element_located((locators['menu_options'])))
        self.wait.until(EC.presence_of_element_located((By.XPATH, locators['user_management_dropdown']))).click()
        time.sleep(2)
        self.wait.until(EC.presence_of_element_located((By.XPATH, locators['users_option']))).click()
        user_role_flag=None
        status_flag=None
        try:
            user_role=self.wait.until(EC.presence_of_element_located((By.XPATH, locators['user_role_dropdown'])))
            time.sleep(2)
            self.action.click(user_role).perform()
            time.sleep(2)
            drop_down_options = user_role.find_elements(by=By.XPATH, value=locators['user_role_dropdown'])
            # self.driver.find_element(by=By.XPATH,value="//div[@role='listbox']//span[text()='ESS']").click()
            time.sleep(3)
            options=[]
            for option in drop_down_options:
                options.append(option.get_attribute("innerText"))
            options=options[1].split("\n")
            options.pop(0)
            print(options)
            if options==data['user_role_expected_options']:
                user_role_flag=True
                print('#------user_role_dropdown options has been validated------#\n')
            else:
                user_role_flag=False
                print('#------user_role_dropdown options are not found------#\n')
        except Exception as e:
            print('Cannot able to click the user_role dropdown\n',e)

        try:
            status=self.wait.until(EC.presence_of_element_located((By.XPATH, locators['status_dropdown'])))
            time.sleep(2)
            self.action.click(status).perform()
            time.sleep(2)
            drop_down_options = status.find_elements(by=By.XPATH, value=locators['status_dropdown'])
            options=[]
            for option in drop_down_options:
                options.append(option.get_attribute("innerText"))
            options=options[1].split("\n")
            options.pop(0)
            print(options)
            if options==data['status_expected_options']:
                status_flag=True
                print('#------status_dropdown options has been validated------#\n')
            else:
                status_flag=False
                print('#------status_dropdown options are not found------#\n')
        except:
            print('Cannot able to click the status_dropdown\n')

        #--------combining all the result to validate the testcase--------#
        result = [user_role_flag, status_flag]

        if all(result):
            print("#-----Test_case_passed-----#\n")
            assert True
        else:
            print("#-----Test_case_failed-----#\n")
            assert False

    def test_new_employee_creation(self,booting_function,login):
        # menu_options_flag = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.Orange_hrm_Locators().menu_options)))
        employee_list_flag=None
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH,locators['pim_xpath']))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH,locators['add_button']))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH,locators['firstname_textbox']))).send_keys(data['test_first_name'])
            self.wait.until(EC.presence_of_element_located((By.XPATH, locators['middlename_textbox']))).send_keys(data['test_middle_name'])
            time.sleep(2)
            self.wait.until(EC.presence_of_element_located((By.XPATH, locators['lastname_textbox']))).send_keys(data['test_last_name'])
            time.sleep(2)
            self.wait.until(EC.presence_of_element_located((By.XPATH, locators['employee_id_textbox']))).send_keys(data['test_employee_id'])
            self.wait.until(EC.presence_of_element_located((By.XPATH, locators['login_details_toggle']))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, locators['login_status_radio']))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, locators['login_username_textbox']))).send_keys(data['test_login_username'])
            self.wait.until(EC.presence_of_element_located((By.XPATH, locators['login_password_textbox']))).send_keys(data['test_login_password'])
            self.wait.until(EC.presence_of_element_located((By.XPATH, locators['login_password_confirm_textbox']))).send_keys(data['test_login_password'])
            self.wait.until(EC.presence_of_element_located((By.XPATH, locators['login_save_button']))).click()
            employee_list_flag=self.wait.until(EC.presence_of_element_located((By.XPATH,locators['personal_details_heading'])))
        except Exception as e:
            print('Cannot be able to Access employee list page, error occurred:',e)
        #--------combining all the result to validate the testcase--------#
        result = [employee_list_flag]
        #
        if all(result):
            print(
                "success: new user created using firstname {a},middlename {b},lastname {c}, employee_id {d}".format(
                    a=orange_data['test_first_name'], b=orange_data['test_middle_name'],
                    c=orange_data['test_last_name'], d=orange_data['test_employee_id']))
            print("#-----Test_case_passed-----#\n")
            assert True
        else:
            print(
                "failure: new user cannot be created using firstname {a},middlename {b},lastname {c}, employee_id {d}".format(
                    a=orange_data['test_first_name'], b=orange_data['test_middle_name'],
                    c=orange_data['test_last_name'], d=orange_data['test_employee_id']))
            print("#-----Test_case_failed-----#\n")
            assert False




