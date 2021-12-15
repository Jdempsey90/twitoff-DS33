'''Uses lambda-ds-twit-assist to pull twitter user and tweet
info from twitter api'''

import requests
import spacy
from .models import DB, Tweet, User


class Twit:
    """
    Uses lambda-ds-twit-assist
    """
    def __init__(self, twitter_handle):
        self.twitter_handle = twitter_handle
        self.user_id = ""
        self.user_json = {}
        self.tweets = []

    def query(self):
        url = "https://lambda-ds-twit-assist.herokuapp.com/user/" \
            + str(self.twitter_handle)

        r = requests.get(url)

        self.user_id = r.json()['twitter_handle']['id']
        self.user_json = r.json()
        self.tweets = r.json()['tweets']


# Load our pretrained SpaCy Word Embeddings model
nlp = spacy.load('my_model/')


# Turn tweet text into word embeddings.
def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


def add_or_update_user(username):
    try:
        # create user object
        twitter_user = Twit(username)
        twitter_user.query()

        # Is there a user in the database that already has this id?
        # If not, then create a User in the database with this id.
        db_user = (User.query.get(twitter_user.user_id)) \
            or User(id=twitter_user.user_id, username=username)

        # add the user to the database.
        DB.session.add(db_user)

        # get the user's tweets
        tweets = twitter_user.tweets

        # check if tweets exist in DB
        if tweets:
            db_user.newest_tweet_id = tweets[0]['id']

        # add each tweet to the database
        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet['full_text'])
            db_tweet = Tweet(id=tweet['id'],
                             text=tweet['full_text'][:300],
                             vect=tweet_vector)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

        # Save the changes to the DB
        DB.session.commit()

    except Exception as e:
        print(f"Error Processing {username}: e")
        raise e
