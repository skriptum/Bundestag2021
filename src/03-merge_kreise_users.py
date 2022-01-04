#######################################################################
# File for cleaning the Wahlergebnisse CSV and merging it with the Twitter Users
#######################################################################

#%%####################################
# imports 

import pandas as pd
from utils import connect_to_database
import re

# definitions 

#######################################
# Running
engine = connect_to_database()

#read in the Wahlergebnisse der Kreise
kreise_df = pd.read_csv(
    "../data/raw/Wahlergebnisse_Kreise.csv", 
    delimiter=";", 
    skiprows=list(range(0,8)), 
    usecols=["Titel", "Namenszusatz", "Nachname", "Vornamen", "Gebietsart", "Gebietsnummer", "Gebietsname"]
    )
# clean this mess

#only direktkanditaten
kreise_df = kreise_df[kreise_df.Gebietsart == "Wahlkreis"] 

#combine names from first Vornamen and Nachnamen
kreise_df.Vornamen = kreise_df.Vornamen.str.split(" ").str[0] 
kreise_df["Name"] = kreise_df.Vornamen + " " + kreise_df.Nachname

# Read in the Users
users_df = pd.read_sql_table("users", engine, columns=["id", "name"])

#clean the name column from the Users
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "\U000024C2-\U0001F251" 
    "]+"
    )

users_df.name = users_df.name.str.replace(EMOJI_PATTERN, "")
users_df.name = users_df.name.str.replace("MdB","")
users_df.name = users_df.name.str.strip()

#%%
#try to merge as much as possible
merged_df = pd.merge(kreise_df, users_df, left_on="Name", right_on="name", how = "left")

#%%
#now we have to work ourselves
merged_df.to_csv("../data/raw/kreise_users.csv")
###merged_df.to_csv("../data/intermediate/kreise_users_edit.csv")


# %%
