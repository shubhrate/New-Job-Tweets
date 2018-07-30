import json

import boto3
import os

import random


def lambda_handler(event, context):
    print(event)
    for record in event['Records']:
        # Check that record is new
        if record['eventName'] == "INSERT":
            # Extract job title, description, apply link, employer, etc.
            job_title = record['dynamodb']['NewImage']['core_job_title']['S']
            print(f"Job title: {job_title}")
            job_category = record['dynamodb']['NewImage']['core_job_category']['S']
            print(f"Job category: {job_category}")
            org_name = record['dynamodb']['NewImage']['core_organization_name']['S']
            print(f"Org name: {org_name}")
            apply_link = record['dynamodb']['NewImage']['core_apply_link']['S']
            print(f"Apply link: {apply_link}")
            job_description = record['dynamodb']['NewImage']['core_job_description']['S']
            print(f"Job description: {job_description}")
            emp_type = record['dynamodb']['NewImage']['core_job_employment_type']['S']
            print(f"Employment type: {emp_type}")
            # Construct tweet from random list of tweet formats
            potential_tweets = [
                f'New job posting!\n{org_name} is looking for a {job_title} in {job_category}.\n{org_name} describes this {emp_type} job as: {job_description}.\nIf you are interested, apply here: {apply_link}',
                f'Want to get a job at {org_name}?\nWell, {org_name} wants a {emp_type} {job_title} to work in {job_category}.\nThis job is described as: {job_description} and you can apply for it at {apply_link}',
                f'Latest job posting at {org_name}:\nIf you want to work {emp_type} as a {job_title} in {job_category}, apply at {apply_link}!\nThis job is described by {org_name} as: {job_description}.'
            ]
            tweet = random.choice(potential_tweets)
            print(f"Full tweet: {tweet}")
            # Create python dictionary with tweet and image
            tweetDict = {
                'Tweet': tweet,
                'Image': 'https://goo.gl/images/focHyA',
                'Job_ID': record['dynamodb']['Keys']['job_id']['S']
            }
            # Store as string message for SQS
            message = json.dumps(tweetDict)
            # Send tweet message to FIFO queue
            sqs = boto3.client('sqs')
            response = sqs.send_message(
                QueueUrl=sqs.get_queue_url(
                            QueueName='jobsQueue.fifo',
                            QueueOwnerAWSAccountId=os.environ['ACCOUNT_ID']
                        )['QueueUrl'],
                MessageBody=message,
                MessageGroupId='twitter'
            )
            print(response)
