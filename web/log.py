import boto3

s3 = boto3.resource('s3')
bucket_logging = s3.BucketLogging('blog-59796-deplosite.co')

BucketLoggingStatus = {
    'LoggingEnabled': {
        'TargetBucket': 'deplosite-logging',
        'TargetPrefix': 'blog-59796-deplosite.co'
    }
}

response = bucket_logging.put(
    BucketLoggingStatus=BucketLoggingStatus)

print(response)
