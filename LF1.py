import json
import boto3
from datetime import datetime
# from elasticsearch import Elasticsearch, RequestsHttpConnection
import requests
# from requests_aws4auth import AWS4Auth

rek = boto3.client('rekognition')
s3 = boto3.resource('s3')
url_p = "https://vpc-photo-6r6is2fk5nvktuptrbsvyzmskq.us-east-1.es.amazonaws.com"
url = "https://vpc-photo-6r6is2fk5nvktuptrbsvyzmskq.us-east-1.es.amazonaws.com/photos/photo/"
# credentials = boto3.Session().get_credentials()
# awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
# region='us-east-2'

def lambda_handler(event, context):
    
    x = json.dumps(event)
    print(x)
    for record in event['Records']:
        objectKey = record['s3']['object']['key']
        bucket = record['s3']['bucket']['name']
        print(bucket)
        print(objectKey)
        rekResponse = rek.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':objectKey}},
        MaxLabels=100, MinConfidence=75)
        if rekResponse:
            jsonObject = {}
            jsonObject['objectKey'] = objectKey
            jsonObject['bucket'] = bucket
            jsonObject['createTimestamp'] = datetime.now().isoformat(timespec='seconds')
            jsonObject['labels'] = []
            for label in rekResponse['Labels']:
                jsonObject['labels'].append(label['Name'])
            print(jsonObject)
            id = "".join(list(filter(str.isalnum, objectKey)))
            esResponse = requests.post(url+id, data=json.dumps(jsonObject), headers={"Content-Type": "application/json"})
            print(esResponse.json())
            # getResponse = requests.get(url_p+"/_search?q="+id)
            # print(getResponse.json())
    return {
        'statusCode': 200,
    }