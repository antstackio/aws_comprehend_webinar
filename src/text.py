import json
import boto3

def handler(event, context):
    try:
        record = event['Records'][0]
        bucket_name = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        s3_client = boto3.client('s3')
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key=key
        )
        data = response['Body'].read().decode('utf-8')
        # call comprehend endpoint

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "success"})
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error"})
        }
