from datetime import datetime
import boto3

cw = boto3.client('cloudwatch')

response = cw.get_metric_statistics(Namespace='AWS/S3', Dimensions=[
    {
        'Name': 'BucketName',
        'Value': 'rainblur-78034-deplosite.co'
    },
    {
        'Name': 'StorageType',
        'Value': 'StandardStorage'
    }
],
    MetricName='BucketSize',
    StartTime=datetime(2022, 3, 1),
    EndTime=datetime(2022, 3, 20),
    Statistics=["SampleCount", "Average", "Sum", "Minimum",'Maximum'],
    Period=60*60*24)
print(response)
