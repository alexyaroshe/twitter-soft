from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from write_log import write_log
from time import sleep
from dataclasses import dataclass
from os.path import exists
from random import random
from os import mkdir
from shutil import rmtree
from change_profile import change_profile, switch_to_professional


@dataclass
class Account:
    acc_name: str
    acc_pass: str
    email: str
    email_pass: str


def remove_cache(username):
    from shutil import rmtree
    from os.path import exists

    if exists(f"accounts/{username}/cache2"):
        rmtree(f"accounts/{username}/cache2")


def set_options(username = None):
    from selenium.webdriver.firefox.options import Options

    options = Options()
    options.add_argument("--no-sandbox")
    
    if username:
        options.add_argument("-profile")
        options.add_argument(f"accounts/{username}")
        
    return options


def __get_accounts():
    accounts = []

    with open("_accounts.txt") as f:
        lines = f.readlines()

    for line in lines:
        acc_name, acc_pass, email, email_pass = line.split(":")
        account = Account(acc_name, acc_pass, email, email_pass)
        accounts.append(account)

    return accounts


def driver_start(url, options):
    try:
        service = Service("driver/geckodriver")
        driver = Firefox(service=service, options=options)

        driver.get(url)
        driver.set_page_load_timeout(30)

    except Exception as e:
        write_log(f"ERROR : driver_start: ({url}) \n{str(e)}")
        if driver:
            driver.close()

    return driver


def login(username, password, email):

    while True:

        try:
            if not exists(f"accounts/{username}"):
                mkdir(f"accounts/{username}")

            options = set_options(username)
            driver = driver_start("https://twitter.com/i/flow/login", options)
            sleep(3)
            actions = ActionChains(driver)
            sleep(1)

            field = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "input"))
            )[-1]
            sleep(1)
            click_element(actions, field, 2)
            type_text(actions, username)
            press_enter(actions)

            field = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "input"))
            )[-1]

            click_element(actions, field, 2)
            type_text(actions, password)
            press_enter(actions)
            sleep(1)

            if driver.current_url == "https://twitter.com/i/flow/login":
                type_text(actions, email)
                press_enter(actions, 7)

            if driver.current_url == "https://twitter.com/home":
                change_profile(driver, actions)
                switch_to_professional(driver, actions)
                driver.close()
                break

            elif driver.current_url == "https://twitter.com/account/access":
                driver.close()
                write_log(f"🔴🔴🔴 ACCOUNT BLOCKED : {username} {password}")
                rmtree(f"accounts/{username}")

                with open('_accounts.txt') as f:
                    accounts = f.readlines()
                    for i in range(len(accounts)):
                        if username in accounts[i]:
                            accounts.pop(i)
                            break

                with open('_accounts.txt', "w") as f:
                    f.writelines(accounts)

                break

            else:
                driver.close()
                rmtree(f"accounts/{username}")

        except:
            if exists(f"accounts/{username}"):
                rmtree(f"accounts/{username}")
            
            try: driver.close()
            except: pass


def mass_login():
    accounts = __get_accounts()
    usernames = []

    for account in accounts:

        usernames.append(account.acc_name)
        
        if not exists(f"accounts/{account.acc_name}"):

            try:
                login(account.acc_name,account.acc_pass, account.email)
            except:
                write_log(f"🔴 FAIL : login {account.acc_name}")
                
    
    return usernames


def press_tab(actions, multiply_sleep_time_by = 1):
    actions.send_keys(Keys.TAB)
    actions.perform()
    sleep(random()*multiply_sleep_time_by)


def press_enter(actions, multiply_sleep_time_by = 1):
    actions.send_keys(Keys.ENTER)
    actions.perform()
    sleep((0.2+random()) * multiply_sleep_time_by)


def press_escape(actions, multiply_sleep_time_by = 1):
    actions.send_keys(Keys.ESCAPE)
    actions.perform()
    sleep((0.2+random()) * multiply_sleep_time_by)


def type_text(actions, text, multiply_sleep_time_by = 1):
    actions.send_keys(text)
    actions.perform()
    sleep((0.2+random()) * multiply_sleep_time_by)


def send_tweet(actions):
    actions.key_down(Keys.COMMAND)
    actions.send_keys(Keys.ENTER)
    actions.key_up(Keys.COMMAND)
    actions.perform()
    sleep(3+random())


def click_element(actions, element, multiply_sleep_time_by = 1):
    actions.move_to_element(element)
    actions.click(element)
    actions.perform()
    sleep(random()*multiply_sleep_time_by)
