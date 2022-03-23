# CODE TO FETCH s3 free metrics
from datetime import datetime
import boto3

cw = boto3.client('cloudwatch')
s3 = boto3.client('s3')

NumberOfObjects = {
    'Name': 'StorageType',
    'Value': 'AllStorageTypes'
}

BucketSizeBytes = {
    'Name': 'StorageType',
    'Value': 'StandardStorage'
}

Metrics = ['BucketSizeBytes', 'NumberOfObjects']

for bucket in s3.list_buckets()['Buckets']:
    name = bucket['Name']
    print("----------------------------------------------------------------")
    print("Bucket : ",name)
    for metric in Metrics:
        print(f"--------------{metric}-------------------")
        response = cw.get_metric_statistics(Namespace='AWS/S3', Dimensions=[
            {
                'Name': 'BucketName',
                'Value': name
            },
            NumberOfObjects if metric==Metrics[1] else BucketSizeBytes
        ],
            MetricName=metric,
            StartTime=datetime(2022, 3, 1),
            EndTime=datetime(2022, 3, 20),
            Statistics=["SampleCount", "Average", "Sum", "Minimum", 'Maximum'],
            Period=60*60*24*2)
        print(response['Datapoints'])


# CODE TO PARSE LOGS as CSV

import pandas as pd

df = pd.read_csv('r.csv', sep=" ", names=['Bucket Owner', 'Bucket', 'Time', 'Time - Offset', 'Remote IP', 'Requester ARN/Canonical ID',
                                          'Request ID',
                                          'Operation', 'Key', 'Request-URI', 'HTTP status', 'Error Code', 'Bytes Sent', 'Object Size',
                                          'Total Time',
                                          'Turn-Around Time', 'Referrer', 'User-Agent', 'Version Id', 'Host Id', 'Signature Version',
                                          'Cipher Suite',
                                          'Authentication Type', 'Host Header', 'TLS version'],
                 usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                          13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
                 engine='python')
                 
df.to_csv('r2.csv')
