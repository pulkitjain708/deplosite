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
