import json
import os
import boto3

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    print(event)
    
    try:
        dynamodb.put_item(
            TableName=os.environ['TABLE_NAME'],
            Item = {
                'time_stamp': {
                    'N': str(event['time_stamp'])
                },
                'temperature': {
                    'N': str(event['temperature'])
                },
                'humidity': {
                    'N': str(event['humidity'])
                }
            }
        )
        return
    except Exception as e:
        print(e)
        return e
