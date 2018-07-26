import json

import boto3
import os

import tweepy
from secrets import get_secret

auth = tweepy.OAuthHandler(
    get_secret('TWITTER_CONSUMER_KEY'), 
    get_secret('TWITTER_CONSUMER_SECRET')
)
auth.set_access_token(
    get_secret('TWITTER_ACCESS_TOKEN_KEY'), 
    get_secret('TWITTER_ACCESS_TOKEN_SECRET')
)
api = tweepy.API(auth)

sqs = boto3.client('sqs')

def send_job_tweet(tweet_text):
    #Sends a tweet to Twitter
    api.update_status(status=tweet_text)

def handler(event,context):
    response = sqs.receive_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/075904714953/jobsQueue.fifo',
        AttributeNames=['SentTimestamp']
    )
    # sqs.get_queue_url(
    #     QueueName='jobsQueue.fifo',
    #     QueueOwnerAWSAccountId=os.environ['ACCOUNT_ID']
    # ),
    tweets = []
    for message in response['Messages']:
        if message['Attributes']['SentTimestamp'] <= 14400000:
            tweets.append(message['Body'])
            for tweet in tweets:
                send_job_tweet(tweet)
        else:
            send_job_tweet('No jobs posted recently, check back in 4 hours!')


