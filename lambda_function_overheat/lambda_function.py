import json
import boto3
import os

sns = boto3.client('sns')

def lambda_handler(event, context):
    print(event)
    # Lambda function gets triggered by IoT Core rule if temperature on sensor is above 80. Sends SMS to topics subscribed phone number through SNS.
    sns.publish(
        TopicArn="arn:aws:sns:us-east-1:123940773876:chris-test-temp-sensor-overheat",
        Message="WARNING: Raspberry PI temperature sensor has reached over 80 degrees Fahrenheit."
    )
