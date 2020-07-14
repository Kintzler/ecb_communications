# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
import tweepy
import urllib3


def get_api(bdf_proxy=True):
    """Returns tweepy API object
    """
    if bdf_proxy:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        os.environ["CURL_CA_BUNDLE"] = ""
        os.environ["HTTPS_PROXY"] = "localhost:3128"

    env_file_path = os.path.join(".", "ecb_communications", "twitter", ".env")

    if not os.path.isfile(env_file_path):
        raise FileNotFoundError(
            "You should an .env file with the following keys: "
            + ", ".join(["consumer_key", "consumer_secret", "key", "secret"])
        )
    else:
        load_dotenv(verbose=True, dotenv_path=env_file_path)

    consumer_info = dict(
        consumer_key=os.getenv("consumer_key"),
        consumer_secret=os.getenv("consumer_secret"),
    )

    access_info = dict(key=os.getenv("key"), secret=os.getenv("secret"),)

    oauth = tweepy.OAuthHandler(**consumer_info)
    oauth.set_access_token(**access_info)

    proxy = "localhost:3128" if bdf_proxy else None
    api = tweepy.API(
        oauth,
        proxy=proxy,
        wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True,
    )

    return api
