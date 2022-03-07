from driver_actions import driver_start, set_options, press_tab, press_enter, press_escape
from selenium.webdriver.common.action_chains import ActionChains
from pyperclip import paste


def find_tweets(number = 10, hashtags = ["NFTgiveaway", "NFT"]):

    options = set_options()
    driver = driver_start("https://www.google.com", options)
    actions = ActionChains(driver)

    for hashtag in hashtags:

        driver.get(f"https://twitter.com/search?q=%23{hashtag}&src=typed_query")
        tweets = []

        try:
            while True:

                press_tab(actions)
                active = driver.switch_to.active_element
                aria_label = active.get_attribute("aria-label")

                if aria_label == "Share Tweet":
                    
                    press_enter(actions, 0.2)
                    press_tab(actions, 0.2)
                    press_enter(actions, 0.2)
                    tweets.append(f"{paste()}\n")
                    press_escape(actions, 0.2)
                
                if len(tweets) >= number:
                    break

        finally:
            with open("_tweets.txt", "a") as f:
                f.writelines(tweets)
