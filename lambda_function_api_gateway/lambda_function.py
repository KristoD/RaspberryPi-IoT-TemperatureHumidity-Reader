import json
import boto3
import os
import decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return list(o)
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
    print(event)
    
    data = table.scan()
    
    data = json.dumps(data, cls=DecimalEncoder)
    data = json.loads(data)
    
    if len(data['Items']) > 0:
        return {
            'status': 200,
            'body': data
        }
    else:
        return {
            'status': 400,
            'body': 'An error occurred.'
        }
    
    