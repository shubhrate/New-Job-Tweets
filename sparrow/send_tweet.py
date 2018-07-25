#!/usr/bin/env python
import datetime
import json

import random
import boto3
import requests

from twython import Twython
from secrets import get_secret


# Decrypts API keys and sets config values from the config file
# Make sure this is loading KMS encrypted values in creds.json 
# or else you may see a TypeError: Incorrect padding error
CONSUMER_KEY = get_secret('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = get_secret('TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN_KEY = get_secret('TWITTER_ACCESS_TOKEN_KEY')
ACCESS_TOKEN_SECRET = get_secret('TWITTER_ACCESS_TOKEN_SECRET')

# Create the Twython Twitter client using our credentials
twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET,
                  ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

def send_job_tweet(tweet_text):
    """Sends a tweet to Twitter"""
    twitter.update_status(status = tweet_text)

def handler(event,context):
    """Sends random tweet from list of potential tweets"""
    send_job_tweet(random.choice(potential_tweets))

