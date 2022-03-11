from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from write_log import write_log
from time import sleep
from random import randint, choice
from driver_actions import type_text, click_element
import pyautogui


def change_profile(driver, actions):
    while True:
        try:
            sleep(2)
            driver.get("https://twitter.com/settings/profile")
            sleep(2)

            name_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@name="displayName"]')))
            click_element(actions, name_field)
            type_text(actions, " NFT")

            bio = "NFT" + choice([" artwork ", ". "]) + choice(
                ["Collector", "Enthusiast"]) + choice([".", ' :)', " "])
            bio_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//textarea[@name="description"]')))
            click_element(actions, bio_field)
            type_text(actions, bio)

            avatar_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Add avatar photo"]')))
            click_element(actions, avatar_input, 8)

            pyautogui.press('right')
            sleep(.5)
            pyautogui.press('right')
            sleep(.5)
            pyautogui.press('right')
            sleep(.5)

            for i in range(randint(0, 12)):
                pyautogui.press('down')
                sleep(.2)

            pyautogui.press('enter')
            sleep(1)

            apply_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="applyButton"]')))
            click_element(actions, apply_button)
            sleep(2)

            banner_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Add banner photo"]')))
            click_element(actions, banner_input)
            sleep(2)

            for i in range(randint(0, 12)):
                pyautogui.press('down')
                sleep(.2)

            pyautogui.press('enter')
            sleep(1)

            apply_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="applyButton"]')))
            click_element(actions, apply_button)
            sleep(2)

            save_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="Profile_Save_Button"]')))
            click_element(actions, save_button, 5)
            sleep(7)

        except Exception as e:
            write_log(f"🔴 FAIL : change_profile \n{str(e)}\nRetrying...")

        else:
            write_log("OK : change_profile")
            break


def switch_to_professional(driver, actions):
    while True:
        try:
            sleep(2)
            driver.get("https://twitter.com/i/flow/convert_to_professional")
            sleep(2)

            agree_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="ActionListNextButton"]')))
            click_element(actions, agree_button, 3)

            category_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//label[1]/div[1]/div[2]")))
            click_element(actions, category_button, 3)

            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="ChoiceSelectionNextButton"]')))
            click_element(actions, next_button, 3)

            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="ChoiceSelectionNextButton"]')))
            click_element(actions, next_button, 3)

            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="ActionListSkipButton"]')))
            click_element(actions, next_button, 4)

        except Exception as e:
            write_log(
                f"🔴 FAIL : switch_to_professional \n{str(e)}\nRetrying...")

        else:
            write_log("OK : switch_to_professional")
            break