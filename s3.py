import boto3
import logging
from botocore.exceptions import ClientError
from os import walk, path
from platform import system
import json

s3 = boto3.client('s3')


def create_bucket(bucketName='www.deplosite-pulkit-pes-project.com', region="ap-south-1"):
    try:
        s3_client = boto3.client('s3', region_name=region)
        location = {'LocationConstraint': region}
        s3_client.create_bucket(Bucket='www.deplosite-pulkit-pes-project.com',
                                CreateBucketConfiguration=location)
        website_configuration = {
            'ErrorDocument': {'Key': 'error.html'},
            'IndexDocument': {'Suffix': 'index.html'},
        }
        s3_client.put_bucket_website(Bucket=bucketName,
                                     WebsiteConfiguration=website_configuration)

        bucket_policy = {
            'Version': '2012-10-17',
            'Statement': [{
                'Sid': 'PublicRead',
                'Effect': 'Allow',
                'Principal': '*',
                'Action': ['s3:GetObject', 's3:GetObjectVersion'],
                'Resource': f'arn:aws:s3:::{bucketName}/*'
            }]
        }

        bucket_policy = json.dumps(bucket_policy)
        s3 = boto3.client('s3')
        s3.put_bucket_policy(Bucket=bucketName, Policy=bucket_policy)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def uploadFiles(dir="C:\\Users\intern\\project\\uploads\\unzipped\\1", bucket='www.deplosite-pulkit-pes-project.com'):
    if dir == "" or bucket == "":
        return False, "No specifications provided"
    s3_client = boto3.client('s3')
    delimiter = ""
    if system() == "Linux":
        delimiter = "/"
    else:
        delimiter = "\\"
    rootPath = dir.rsplit(delimiter, 1)[1]
    for index, (root, dir, files) in enumerate(walk(dir)):
        relativePath = root.split(delimiter+rootPath)[1]
        for file in files:
            try:
                ExtraArgs = {}
                if file.rsplit('.', 1)[1] in ['html', 'htm']:
                    ExtraArgs = {'ContentType': 'text/html'}
                objectName = '{}/{}'.format(relativePath,
                                            file).replace("\\", "/")[1:]
                v = file if index == 0 else objectName
                s3.put_object(Body=open(path.join(root, file),mode='rb'),
                              Bucket=bucket,
                              Key=v,
                              ContentType='text/html')
            except ClientError as e:
                logging.error(e)


create_bucket()
uploadFiles()
