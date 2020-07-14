# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 16:59:11 2020

@author: D820091
"""
import tweepy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ecb_communications.twitter import (get_api,
                                        get_user_from_status,
                                        get_info_from_tweet,
                                        bad_tweet)
from ecb_communications.sql import (TwitterUser,
                                    Tweet)


#==============================================================================
# STREAMING AND WRITING
#==============================================================================

ENGINE_PATH = 'postgresql://postgres:postgres@localhost:5432/twitter'

engine = create_engine(ENGINE_PATH, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class ECBStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        user_dict = get_user_from_status(status)
        tweet_dict = get_info_from_tweet(status)
        
        text = tweet_dict["text"]
        
        if bad_tweet(text):
            print("Cricket:\n", text, "\n"*2)
            pass
        else:
            print("European Central Bank:\n", text, "\n"*2)
            current_user = TwitterUser(**user_dict)
            current_tweet = Tweet(**tweet_dict)
            
            try:
                session.add(current_user)
                session.add(current_tweet)
                session.commit()
            except Exception as e:
                print(e)
                session.rollback()

    def on_error(self, status_code):
        print(status_code)

api = get_api(bdf_proxy=True)
StreamListener = ECBStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=StreamListener)

myStream.filter(track=["ecb"], languages=["en"], is_async=False)

#==============================================================================
# QUERYING
#==============================================================================
#["Tweet {}: {}".format(i, tweet.text) for i, tweet in enumerate(session.query(Tweet).all())]