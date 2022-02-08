###########################################################################
# File for importing all tweets from the users
###########################################################################


# Imports
from sqlalchemy.sql.functions import user
from utils import authenticate_twitter_api, connect_to_database
import pandas as pd

from sqlalchemy import MetaData

# Definitions

#%%
def get_users_tweets(user_id, max_results = 50):
    """ Function to get users tweets after a schema and automatically parse them, returns a DataFrame"""

    user_tweet_df = pd.DataFrame()

    tweets = cli.get_users_tweets(
        user_id, max_results = max_results,
        tweet_fields = ["created_at", "public_metrics", "entities", "in_reply_to_user_id", "referenced_tweets"] 
    )

    try:
        for tweet in tweets.data:
            tweet_df = parse_tweet(tweet)
            user_tweet_df = user_tweet_df.append(tweet_df)
    except TypeError:
        return None

    user_tweet_df["author"] = user_id

    return user_tweet_df


def parse_tweet(tweet):
    """ parse information from a Tweet Object, returns an DataFrame"""

    tweet_df = pd.DataFrame()

    # extract public metrics
    tweet_df = tweet_df.append(tweet.public_metrics, ignore_index=True)

    # check type of Tweet
    if not tweet.referenced_tweets is None:
        #check the type of the first referenced tweet, this is a possibly flaw if more than one tweet is referenced
        tweet_df["type"] = tweet.referenced_tweets[0]["type"] 
    else:
        tweet_df["type"] = "original"

    # extract hashtags
    try:
        hashtag_string = ""
        for hashtag in tweet.entities["hashtags"]:
            hashtag_string += hashtag["tag"] + "|"
        tweet_df["hashtags"] = hashtag_string
    except:
        tweet_df["hashtags"] = None

    tweet_df["text"] = tweet.text
    tweet_df["created_at"] = tweet.created_at
    tweet_df["id"] = tweet.id

    tweet_df = tweet_df.set_index("id")

    return tweet_df
    
#%%
# Runtime
if __name__ == "__main__":
    # connect to services
    cli = authenticate_twitter_api()
    engine = connect_to_database()


    #get the user ids from the table
    user_ids = pd.read_sql_table("users", engine, columns=["id"]).id 

    all_users_tweets_df = pd.DataFrame()
    for id in user_ids:
        user_tweet_df = get_users_tweets(id, max_results=10)
        all_users_tweets_df = all_users_tweets_df.append(user_tweet_df)

    all_users_tweets_df.to_sql("tweets", engine, if_exists="replace")
    

