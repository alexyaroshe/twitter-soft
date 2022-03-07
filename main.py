from driver_actions import mass_login
from twitter_promote import start_promoting
from find_tweets import find_tweets


if __name__ == "__main__":

    usernames = mass_login()
    start_promoting(usernames)

    # find_tweets(15)