from random import choice
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
from write_log import write_log
from driver_actions import driver_start, remove_cache, set_options, press_tab, press_enter, press_escape, type_text, send_tweet


def get_tweets():
    with open("_tweets.txt") as f:
        tweets = [link.strip() for link in f.readlines()]

    return tweets


def get_promotion_texts():
    with open("_promotion_text.txt") as f:
        promotion_texts = [link.strip() for link in f.readlines()]
    
    return promotion_texts


def start_account(username, tweet):

    remove_cache(username)
    options = set_options(username)
    driver = driver_start(tweet, options)

    return driver


def write_tweet_repliedto_usedaccounts(tweet, repliedto, usedaccounts):
    with open("_used.txt", "a") as f:
        f.writelines([tweet, repliedto, usedaccounts])


def __read_tweet_repliedto_usedaccounts():
    with open("_used.txt") as f:
        lines = [link.strip() for link in f.readlines()]
    
    tweet_repliedto_usedaccounts = zip(
        lines[::3],
        [line.strip('][').replace('\'', '').replace(' ', '').split(',') for line in lines[1::3]],
        [line.strip('][').replace('\'', '').replace(' ', '').split(',') for line in lines[2::3]]
            )

    return tweet_repliedto_usedaccounts


def get_repliedto_usedaccounts(tweet):
    tweet_repliedto_usedaccounts = __read_tweet_repliedto_usedaccounts()

    for tweet_repliedto_usedaccounts_set in tweet_repliedto_usedaccounts:
        if tweet_repliedto_usedaccounts_set[0] == tweet:
            
            repliedto = tweet_repliedto_usedaccounts_set[1]
            usedaccounts = tweet_repliedto_usedaccounts_set[2]

    return repliedto, usedaccounts


def get_usedtweets():
    tweet_repliedto_usedaccounts = __read_tweet_repliedto_usedaccounts()
    usedtweets = [tweet_repliedto_usedaccounts_set[0] for tweet_repliedto_usedaccounts_set in tweet_repliedto_usedaccounts]

    return usedtweets


def get_usedaccounts():
    tweet_repliedto_usedaccounts = __read_tweet_repliedto_usedaccounts()
    usedaccounts = [tweet_repliedto_usedaccounts_set[2] for tweet_repliedto_usedaccounts_set in tweet_repliedto_usedaccounts]

    return usedaccounts


def use_account(driver, promotion_texts, repliedto, username, tweet):

    playsound('start_short.mp3')
    actions = ActionChains(driver)
    replies_count = 0
    passed_replies = 0
    sleep(0.5)

    try:
        while True:
            
            if passed_replies >= 100:
                break

            press_tab(actions, 0.1)
            active = driver.switch_to.active_element
            data_testid = active.get_attribute("data-testid")

            if data_testid == "caret":

                press_enter(actions, 0.2)
                twitter_username = driver.find_element(By.XPATH, '//div[@role="menuitem"]').text.split()[-1]
                press_escape(actions)
        
                while True:

                    if twitter_username in repliedto:
                        passed_replies += 1
                        break

                    repliedto.append(twitter_username)

                    press_tab(actions, 0.2)
                    active = driver.switch_to.active_element
                    data_testid = active.get_attribute("data-testid")
                    
                    if data_testid == "reply":

                        press_enter(actions)

                        if driver.current_url == "https://twitter.com/compose/tweet":

                            sleep(.1)
                            type_text(
                                actions,
                                choice(["Hey!", "Hii!", "Hello!", "Hey there!", "Heyy!", "GM!"]) + " " + choice(promotion_texts)
                                )
                            send_tweet(actions)
                            replies_count += 1

                            # if tweet was not sent
                            if driver.current_url == "https://twitter.com/compose/tweet":
                                sleep(3)

                                if driver.current_url == "https://twitter.com/compose/tweet":
                                    try: 
                                        failed_message = driver.find_element(By.XPATH, '//div[@aria-live="assertive"]').text

                                        replies_count -= 1
                                        write_log(f"🔴 FAIL : ({username}) {failed_message}")
                                        break

                                    except:
                                        pass
                        break

            if replies_count >= 8:
                print(replies_count)
                break

            if driver.current_url == "https://twitter.com/i/flow/login":
                write_log(f"🔴 FAIL : at login url ({username})")
                break
            
            elif driver.current_url != tweet and driver.current_url != "https://twitter.com/compose/tweet":
                driver.back()

    except Exception as e:
        write_log(f"🔴 ERROR : {username} (reply {replies_count}) under {tweet}\n{str(e)}")

    else:
        write_log(f"✅ : {username} sent {replies_count} under {tweet} 🐢")
        

def start_promoting(usernames):

    promotion_texts = get_promotion_texts()
    tweets = get_tweets()
    usedaccounts = get_usedaccounts()
    get_repliedto_usedaccounts
    usedtweets = get_usedtweets()

    for tweet in [tweet for tweet in tweets if tweet not in usedtweets]:

        repliedto = ["@"+tweet.split("/")[3]]

        for username in usernames:

            if username not in usedaccounts:

                driver = start_account(username, tweet)
                use_account(driver, promotion_texts, repliedto, username, tweet)
                print(repliedto)
                usedaccounts.append(username)

                driver.close()

        write_tweet_repliedto_usedaccounts(tweet, repliedto, usedaccounts)

        write_log(f"✅ TWEET DONE : {tweet}, {len(usedaccounts)} accs used, {len(repliedto)-1} replies sent")

    write_log(f"✅ : DONE")
