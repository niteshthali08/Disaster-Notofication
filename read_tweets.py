import sys
import json
from common_methods import console_log
import time
from pymongo import MongoClient
import tweepy
from tweepy import OAuthHandler
from tweepy import TweepError, cursor

# reads tweets using API

import tweepy
#override tweepy.StreamListener to add logic to on_status
class MyTweeetListener(tweepy.StreamListener):
    auth = None
    client = None
    db = None
    coll = None
    start_time = None
    def __init__(self):
        console_log('--- Inside __init__() function of read_tweets ---')
        configs = {}
        try:
            # client = MongoClient('mongodb://admin:admin123@localhost:27017/')
            with open('user.config') as f:
                for line in f:
                    if line == '\n':
                        continue
                    line = line.strip().split('->')
                    configs[line[0]] = line[1]

        except IOError as e:
            print e.strerror
        except:
            print sys.exc_info()[0]

        self.auth = tweepy.OAuthHandler(configs['consumer_key'], configs['consumer_secret'])
        self.auth.set_access_token(configs['access_token'],configs['access_secret'])
        #console_log('*** auth: ', self.auth)

        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client.generate_news  # generate news is a database
        self.db.raw_tweets.drop() # drop the collection if exists
        self.coll = self.db.raw_tweets

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        if time.time() - self.start_time < 15:
            try:
                decoded = json.loads(data)
                console_log(decoded)
                if (decoded["lang"] == 'en'):
                    obj = { "tweet_id" : decoded["id"],
                        "text" : decoded['text'].encode('ascii', 'ignore'),
                        "tweet_date" : decoded["timestamp_ms"],
                        "user_mentions" : decoded["entities"]["user_mentions"],
                        "hashtags" :  decoded ["entities"]["hashtags"],
                        "urls" : decoded["entities"]["urls"],
                        "location" : decoded["user"]["location"],
                        "author_name": decoded["user"]["name"],
                        "media" : decoded["user"]["profile_image_url"],
                        "screen_name" : decoded["user"]["screen_name"],
                        "description" : decoded["user"]["description"],

                        }
                    self.coll.save(obj)
                return True
            except:
                console_log('Exception in on_data tweeter stream function: ')
        else:
            return False


        # Also, we #NariShakticonvert UTF-8 to ASCII     ignoring all bad characters sent by users
        #console_log(decoded.encode('ascii', 'ignore'))

        #print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        # continue looping

    def on_error(self, status):
        print status


if __name__ == '__main__':
    l = MyTweeetListener()
    console_log(l.auth)
    console_log("Showing all new tweets for #programming:")
    stream = tweepy.Stream(l.auth, l)
    l.start_time = time.time()
    stream.filter(track=['accident'])
    console_log("*** Done with reading tweets for a minute *** ")
    obj = {"tweet_id": 123478900,
           "text": "Venezuela blackout stops subway causes traffic jams and interrupts presidential broadcast",
           "tweet_date": 1464639362,
           "user_mentions": [],
           "hashtags": [],
           "urls": [],
           "location": "USA, AZ",
           "author_name": "Nitesh Thali",
           "media": "https://pbs.twimg.com/profile_images/438552129699971072/gMBMUfUw.jpeg",
            "screen_name": "@Nitesh_Thali",
            "description": "I am cool",
            "profile_image_url": "https://pbs.twimg.com/profile_images/438552129699971072/gMBMUfUw.jpeg"
    }
    l.coll.save(obj)

# def read_and_store_tweets(key, configs):
#     try:
#         console_log(configs)
#         # code for tweeter search API
#         # auth = OAuthHandler(configs['consumer_key'], configs['consumer_secret'])
#         # auth.set_access_token(configs['access_token'], configs['access_secret'])
#         # api = tweepy.API(auth)
#         # # q=&geocode=-22.912214,-43.230182,1km&lang=pt&result_type=recent
#         # all_tweets = tweepy.Cursor(api.search, q = "Google", geocode = '8.8981307,76.6159916,500km', lang = 'en')\
#         #     .items(20)
#         # count = 0
#         # for l in all_tweets:
#         #     count += 1
#         # console_log(count)
#         # console_log(l)
#     except TweepError as tw:
#         print 'Exception:', tw