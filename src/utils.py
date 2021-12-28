###########################################################################
# File for general Functions, often related to connecting to a Service
###########################################################################

# Imports
from os import getenv
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Definitions
def authenticate_twitter_api():
    """ authenticates with the twitter api, returns an client object from the tweepy library"""
    load_dotenv()
    TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
    cli = tweepy.Client(TWITTER_BEARER_TOKEN)
    return cli   


def connect_to_database():
    """ connects to the PostgreSQL Database by loading the URL from the environment variable
    returns a session"""
    #load the URL
    load_dotenv()
    URL = getenv("DATABASE_URL")

    #connect to the database
    engine = create_engine(URL)
    engine.connect()

    #create the connection
    Session = sessionmaker(bind=engine)
    session = Session()

    return session