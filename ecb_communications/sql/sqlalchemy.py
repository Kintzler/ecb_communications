from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
        Column,
        Integer,
        String,
        DateTime,
        Boolean,
        JSON,
        BigInteger)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..twitter.streaming import get_info_from_tweet, get_user_from_status, bad_tweet


Base = declarative_base()

class TwitterUser(Base):
    __tablename__ = 'users'
    
    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime)
    screen_name = Column(String)
    name = Column(String)
    description = Column(String)
    followers_count = Column(Integer)
    friends_count = Column(Integer)
    verified = Column(Boolean)
    protected = Column(Boolean)
    statuses_count = Column(Integer)
    
    def __repr__(self):
        return "<TwitterUser(id={}, screen_name={}, followers_count={})>".format(self.id, self.screen_name, self.followers_count)

class Tweet(Base):
    __tablename__ = 'tweets'
    
    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime)
    text = Column(String)
    lang = Column(String)
    retweet_count = Column(Integer)
    retweeted = Column(Boolean)
    entities = Column(JSON)
    
    def __repr__(self):
        return "<Tweet(id={}, created_at={}, text={})>".format(self.id, self.created_at, self.text)


# STREAM
#engine = create_engine('postgresql://postgres:postgres@localhost:5432/twitter', echo=True)
#Session = sessionmaker(bind=engine)
#session = Session()
#
#
#class ECBStreamListener(tweepy.StreamListener):
#    def on_status(self, status):
#        user_dict = get_user_from_status(status)
#        tweet_dict = get_info_from_tweet(status)
#        
#        text = tweet_dict["text"]
#        
#        if bad_tweet(text):
#            print("Cricket:\n", text, "\n"*2)
#            pass
#        else:
#            print("European Central Bank:\n", text, "\n"*2)
#            current_user = TwitterUser(**user_dict)
#            current_tweet = Tweet(**tweet_dict)
#            
#            try:
#                session.add(current_user)
#                session.add(current_tweet)
#                session.commit()
#            except Exception as e:
#                print(e)
#                session.rollback()
#
#    def on_error(self, status_code):
#        print(status_code)
#
