###########################################################################
# File for importing all tweets from the users
###########################################################################

#%%
# Imports
from utils import authenticate_twitter_api, connect_to_database
import sys
import pandas as pd

from sqlalchemy import MetaData

# Definitions

# Runtime

if __name__ == "__main__":
    # get the api
    try:
        cli = authenticate_twitter_api()
        engine = connect_to_database()
    except Exception as e:
        sys.exit(f"Connection Error: {e}")

    user_ids = pd.read_sql_table("users", engine, columns=["id"]).id



    

    

# %%
