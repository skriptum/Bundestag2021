###########################################################################
# File for importing all list members and saving their data to the Database
###########################################################################

# Imports 
from utils import authenticate_twitter_api, connect_to_database
import sys 

import tweepy
import pandas as pd

#%%

#Definitions
def get_list_members(list_id):
    """get all members from a twitter list and traverse the pagination
    takes as input list_id, returns list of Tweepy.UserObjects"""
    token = None

    list_members = []
    while True:
        list_response = cli.get_list_members(
            list_id, pagination_token = token,
            user_fields = ["created_at", "description", "public_metrics", "location", "profile_image_url", "verified"]
            )
        list_members+= list_response.data
        try: 
            token = list_response.meta["next_token"]
        except:
            break

    return list_members

def create_partei_dataframe(parteien_listen):
    #Create the central dataframe
    user_df = pd.DataFrame()

    # get members from all lists 
    for partei, l_id in parteien_listen.items():

        #get the list members
        list_members = get_list_members(l_id)

        #transform to DF
        partei_df = pd.DataFrame(list_members)

        partei_df["partei"] = partei

        #clean the resulting dataframe
        partei_df = partei_df.set_index("id") #set index column
        metrics_df = partei_df.public_metrics.apply(pd.Series) # flatten the column
        partei_df = pd.concat([partei_df, metrics_df], axis= 1) #merge back the flattened columns
        partei_df = partei_df.drop(columns=["public_metrics"])
        #append to big DF
        user_df = user_df.append(partei_df)

    return user_df
#%%

#Running
if __name__ == "__main__":
    cli = authenticate_twitter_api()
    engine = connect_to_database()

    # Get user pollytix_GMBH where Lists are saved
    pollytix = cli.get_user(username = "pollytix_gmbh")
    pollytix_id = pollytix.data["id"]
    pollytix_listen = cli.get_owned_lists(pollytix_id)

    # get lists from polyltix and name them accordingly
    parteien_keys = ["CDU", "SPD", "DIE LINKE", "GRÜNE", "AfD", "CSU", "FDP"]
    parteien_values = pollytix_listen.data[1:8].id
    parteien_listen = dict(zip(parteien_keys, parteien_values))

    #Create the central dataframe
    user_df = create_partei_dataframe(parteien_listen)

    user_df.to_csv("../data/intermediate/twitter_users.csv")
    user_df.to_sql("users", engine, if_exists="replace")
