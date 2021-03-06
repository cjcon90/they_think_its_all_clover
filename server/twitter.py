from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient
import json
from datetime import datetime as dt
from credentials import *

client = MongoClient(f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_CLUSTER}.wijab.mongodb.net/{DB_COLL}?retryWrites=true&w=majority")
db = client['they_think_its_all_clover']
collection = db['tweet']

# Override the Std Class (https://www.kite.com/python/docs/examples.streaming.StdOutListener)
class StdOutListener(StreamListener):
    # https://www.kite.com/python/docs/tweepy.streaming.StreamListener.on_data
    def on_data(self, data):
        text = json.loads(data)
        print(data)
        content = text["text"]
        username = text["user"]['name']
        avatar = text["user"]["profile_image_url"]
        url = f'https://twitter.com/{text["user"]["screen_name"]}'
        time_posted = dt.strptime(text["created_at"], '%a %b %d %H:%M:%S %z %Y')
        try:
            location = text["place"]["bounding_box"]["coordinates"]
        except:
            location = text["user"]["location"]
        tweet_data = {
                "content": content,
                "username": username,
                "avatar": avatar,
                "url": url,
                "location": location,
                "time_posted": time_posted
            }
        collection.insert_one(tweet_data)



if __name__ == "__main__":
    auth = OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    # Listen for a stream
    listen = StdOutListener()
    stream = Stream(auth, listen)
    # Filter the stream to tweets containing #theyThinkItsAllClover:
    stream.filter(track=['#theyThinkItsAllClover'])
