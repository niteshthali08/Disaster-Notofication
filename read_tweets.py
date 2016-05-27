import sys
from pymongo import MongoClient
import tweepy
from tweepy import OAuthHandler
from tweepy import TweepError, cursor
from nltk.corpus import stopwords
import wikipedia
# reads tweets

client = None
debug = 1
def init_config():
    all_configs = {}
    try:
        #client = MongoClient('mongodb://admin:admin123@localhost:27017/')
        with open('user.config') as f:
            for line in f:
                if line == '\n':
                    continue
                line = line.strip().split('~')
                all_configs[line[0]] = line[1]
    except IOError as e:
        print e.strerror
    except:
        print sys.exc_info()[0]
    f.close()
    return all_configs

def console_log(param):
    if debug:
        print param
        if type(param) == tweepy.cursor.ItemIterator:
            for line in param:
                print line

def read_and_store_tweets(key):

    try:
        auth = OAuthHandler(all_configs['consumer_key'], all_configs['consumer_secret'])
        auth.set_access_token(all_configs['access_token'], all_configs['access_secret'])
        api = tweepy.API(auth)
        # q=&geocode=-22.912214,-43.230182,1km&lang=pt&result_type=recent
        all_tweets = tweepy.Cursor(api.search, q = key, geocode = '8.8981307,76.6159916,500km', lang = 'en').items(10)
        count = 0
        for l in all_tweets:
            count += 1
        console_log(count)
        #console_log(all_tweets)
    except TweepError as tw:
        print 'Exception:', tw


if __name__ == '__main__':
    init_config()
    #search_key = 'KeralaTempleFire '
    #read_and_store_tweets(search_key)