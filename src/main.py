import time
import boto3
import json
import os

def handler(event, context):
    request_body = json.loads(event['body'])
    customer_complaints = request_body['complaints']
    customer_id = request_body['customer_id']

    try:
        file_content = bytes(customer_complaints, encoding='utf-8')
        s3_client = boto3.client('s3')
        bucket_name = os.environ['SOURCEBUCKET']
        print(f"BUCKET NAME :: {bucket_name}")
        s3_client.put_object(Body=file_content,
            Bucket=bucket_name,
            Key=f'complaints/{customer_id}-{str(int(time.time()))}-complaint.txt'
        )
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
