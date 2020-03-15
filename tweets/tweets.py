import pandas as pd
import os
from datetime import datetime


def get_data_json(tweet_num, df):
    top_tweets = {}
    for _ in range(tweet_num):
        top_tweets[_] = {"tweet": df['text'][_],
                         "username": df['username'][_],
                         "time": df['timestamp'][_],
                         "sentiment": "negative" if df['target_new'][_] else "positive"}
    return top_tweets
class Tweets:
    def __init__(self, app):
        csv_filename = os.path.join(app.root_path, 'tweets\\data', 'sentis.csv')
        self.df = pd.read_csv(csv_filename)
        self.df['timestamp'] = self.df['timestamp'].apply(lambda x: datetime.fromtimestamp(x))

    def get_recent_tweets(self, tweet_num=10):
        top_tweets = get_data_json(tweet_num, self.df)
        return top_tweets

    def get_most_positive(self, tweet_num=10):
        top_postive = self.df.sort_values('target', ascending=False)
        return get_data_json(10, top_postive)

    def get_most_negative(self, tweet_num=10):
        top_negative = self.df.sort_values('target', ascending=True)
        return get_data_json(10, top_negative)

