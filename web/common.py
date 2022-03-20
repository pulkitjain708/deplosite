# from datetime import datetime
# import boto3

#  BucketSizeBytes
# NumberOfObjects
# ReplicationLatency
# 4xxErrors
# TotalRequestLatency
# AllRequests

# cw = boto3.client('cloudwatch')

# response = cw.get_metric_statistics(Namespace='AWS/S3', Dimensions=[
#     {
#         'Name': 'BucketName',
#         'Value': 'blog-59796-deplosite.co'
#     },
#     {
#         'Name': 'StorageType',
#         'Value': 'StandardStorage'
#     }
# ],
#     MetricName='BucketSizeBytes',
#     StartTime=datetime(2022, 3, 1),
#     EndTime=datetime(2022, 3, 20),
#     Statistics=["SampleCount", "Average", "Sum", "Minimum",'Maximum'],
#     Period=60*60*24)

# response = cw.get_metric_statistics(Namespace='AWS/S3', Dimensions=[
#     {
#         'Name': 'BucketName',
#         'Value': 'blog-59796-deplosite.co'
#     },
#     {
#         'Name': 'StorageType',
#         'Value': 'AllStorageTypes'
#     }
# ],
#     MetricName='NumberOfObjects',
#     StartTime=datetime(2022, 3, 1),
#     EndTime=datetime(2022, 3, 20),
#     Statistics=["SampleCount", "Average", "Sum", "Minimum",'Maximum'],
#     Period=60*60*24)
# print(response)
# 