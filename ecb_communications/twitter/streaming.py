# -*- coding: utf-8 -*-
import re

# General function
# from .config import api
# import tweepy
# def get_user_timeline(user, count=None):
#    """Get full user timeline, 'user' can be screen_name or user_id
#    """
#    c = tweepy.Cursor(api.user_timeline, user, tweet_mode="extended", count=200)
#    items = c.items(count) if count else c.items()
#    try:
#        out = list(items)
#    except tweepy.TweepError as e:
#        print(e)
#    else:
#        return out


def get_full_text_if_present(status):
    try:
        text = status.extended_tweet["full_text"]
    except AttributeError:
        text = status.text
    return text


def get_info_from_tweet(status):
    text = get_full_text_if_present(status)
    text = re.sub(pattern="'{1,}", repl="''", string=text)
    date = status.created_at.isoformat()
    d = {
        "id": status.id,
        "created_at": date,
        "text": text,
        "lang": status.lang,
        "retweet_count": status.retweet_count,
        "retweeted": status.retweeted,
        "entities": status.entities,
    }
    return d


def get_user_from_status(status):
    user_fields = [
        "id",
        "screen_name",
        "name",
        "description",
        "statuses_count",
        "protected",
        "verified",
        "followers_count",
        "friends_count",
        "created_at",
    ]
    return {key: status.user._json.get(key) for key in user_fields}


# USED in streaming
def bad_tweet(text_tweet):
    bad_keywords = ["cricket", "bowled", "footwork"]
    return any([bad in text_tweet.lower() for bad in bad_keywords])
