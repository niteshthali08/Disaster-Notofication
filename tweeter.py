from common_methods import console_log
import time
from pymongo import MongoClient
class Tweeter:
    tweet_id = None # doone
    user_mentions = None # done
    hashtags = None # done
    urls = None  # done
    media = None # done
    text = None # done
    author_name = None
    tweet_date = None # done
    location = None # done
    screen_name = None
    description = None
    profile_image_url = None

    speciales = ["'", '"', "/", "\\"];

    client = MongoClient('mongodb://localhost:27017/')
    db = client.generate_news  # generate news is a database
    coll = db.raw_tweets

    def get_one_tweet(self):
        # for now hard coding to return one tweet (author_name = "Nitesh Thali")
        obj = self.coll.find_one({"author_name" : "Nitesh Thali"})
        console_log(obj)
        self.tweet_id = obj["tweet_id"]
        self.user_mentions = obj["user_mentions"]
        self.hashtags = obj["hashtags"]
        self.urls = obj["urls"]
        self.text = obj["text"]
        self.tweet_date = obj["tweet_date"]
        self.location = obj["location"]
        self.author_name = obj["author_name"]
        self.media = obj["media"]
        self.screen_name = obj["screen_name"]
        self.description = obj["description"]
        self.profile_image_url = obj["media"]


if __name__ == '__main__':
    tw = Tweeter()
    tw.get_one_tweet()
    console_log(tw.text)