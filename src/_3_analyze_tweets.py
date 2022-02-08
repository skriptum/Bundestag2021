from utils import * 
import pandas as pd


engine = connect_to_database()
user_df = pd.read_sql_table("users", engine)

t_df = pd.read_sql("tweets", engine)

def extract_hashtags(column):
    concatenated_string = column.str.cat()
    hashtag_list = concatenated_string.split("|")[:-1]
    sorted_list = pd.Series(hashtag_list, dtype="string").value_counts()

    return sorted_list


def parse_tweets(df):
    user_dict = df.type.value_counts() # extract most used type of tweets
    
    user_dict["likes_per_tweet"] = ( df.like_count.sum() ) / df.shape[0] # number of total likes

    hashtags = extract_hashtags(df.hashtags).keys()
    for i in range(5):
        try:
            tag = hashtags[i]
        except:
            tag = None
        user_dict[f"hashtag_{i}"] = tag

    #tweets per day
    n_tweets = df.index[-1]
    oldest_tweet = df.created_at.sort_values().values[0]
    time_passed = pd.Timestamp.today() - oldest_tweet
    user_dict["tweets_per_day"] = n_tweets / time_passed.days

    return user_dict


if __name__=="__main__":
    user_metric_df = pd.DataFrame()

    for index, user in user_df.iterrows():
        #extract the users tweets from the tweets table
        user_tweets = t_df[t_df.author == user.id]

        #parse the tweets
        if not user_tweets.empty:
            user_metrics = parse_tweets(user_tweets)
        else:
            user_metrics = pd.Series(dtype="int")

        #append it to the metric dataframe
        user_metric_df = user_metric_df.append(user_metrics, ignore_index=True)

    #merge the two dataframes back together purely based on index, maybe bad idea
    combined_df = user_df.join(user_metric_df) 
    
    combined_df.to_sql("user_with_metrics", engine)


    
    

