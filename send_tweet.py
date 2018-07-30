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
dynamodb = boto3.client('dynamodb')


def send_job_tweet(tweet_text):
    # Sends a tweet to Twitter
    api.update_status(status=tweet_text)


def handler(event, context):
    print(event)
    response = sqs.receive_message(
        QueueUrl=sqs.get_queue_url(
                    QueueName='jobsQueue.fifo',
                    QueueOwnerAWSAccountId=os.environ['ACCOUNT_ID'])
                    ['QueueUrl'],
        AttributeNames=['SentTimestamp'],
        MaxNumberOfMessages=10
    )
    print(response)
    try:
        tweets = []
        for message in response['Messages']:
            data = json.loads(message['Body'])
            text = data['Tweet']
            tweets.append(text)
            sqs.delete_message(
                QueueUrl=sqs.get_queue_url(
                            QueueName='jobsQueue.fifo',
                            QueueOwnerAWSAccountId=os.environ['ACCOUNT_ID'])
                            ['QueueUrl'],
                ReceiptHandle=message['ReceiptHandle']
            )
        for tweet in tweets:
            send_job_tweet(tweet)
            dynamodb.update_item(
                TableName='jobsTable',
                Key={
                    'job_id': {
                        'S': data['Job_ID']
                    }
                },
                UpdateExpression="SET posted_to_twitter = :t",
                ExpressionAttributeValues={
                    ':t': {
                        'BOOL': True
                    }
                }
            )
    except KeyError:
        print('No new jobs!')
