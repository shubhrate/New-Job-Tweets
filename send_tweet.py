import json

import boto3
import os

from twython import Twython
from secrets import get_secret

#get API keys
CONSUMER_KEY = get_secret('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = get_secret('TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN_KEY = get_secret('TWITTER_ACCESS_TOKEN_KEY')
ACCESS_TOKEN_SECRET = get_secret('TWITTER_ACCESS_TOKEN_SECRET')

# Create the Twython Twitter client using credentials
twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET,
                  ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

sqs = boto3.client('sqs')

def send_job_tweet(tweet_text):
    #Sends a tweet to Twitter
    twitter.update_status(status = tweet_text)

def handler(event,context):
    response = sqs.receive_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/075904714953/jobsQueue.fifo'
    )
    # sqs.get_queue_url(
    #     QueueName='jobsQueue.fifo',
    #     QueueOwnerAWSAccountId=os.environ['ACCOUNT_ID']
    # ),
    tweet_text = response['Messages']['Body']
    send_job_tweet(tweet_text)

