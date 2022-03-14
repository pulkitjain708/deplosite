from os import walk, path, remove
import boto3
import logging
from botocore.exceptions import ClientError
from platform import system
import json

def mimeType(ext):
    mime=""
    if ext=='css':
        mime="text/css"
    elif ext=='html':
        mime="text/html"
    elif ext=="js":
        mime="application/javascript"
    return mime    
        
def checkStatic(dir="", allowed=[], rootFile=""):
    if dir == "" or len(allowed) == 0 or rootFile == "":
        return False, "No specifications provided"
    for index, (root, dir, files) in enumerate(walk(dir)):
        if index == 0 and len(dir) == 1 and len(files) == 0:
            return False, "Try zipping going into root of project,improper zip"
        if index == 0 and len(files) != 0:
            if rootFile not in files:
                return False, "Serving File not Found at Root of Project"
            elif len(files) == 0:
                return False, "No Files Found to Serve "
        if len(files) != 0:
            for file in files:
                ext = file.rsplit('.', 1)[1]
                if ext not in allowed:
                    purepath = path.join(root, file)
                    remove(purepath)

    return True, "Operation Completed"

def create_bucket(bucketName='',error="",index="",region="ap-south-1"):
    try:
        s3_client = boto3.client('s3', region_name=region)
        location = {'LocationConstraint': region}
        s3_client.create_bucket(Bucket=bucketName,
                                CreateBucketConfiguration=location)
        website_configuration = {
            'ErrorDocument': {'Key': error},
            'IndexDocument': {'Suffix': index},
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
        s3_client.put_bucket_policy(Bucket=bucketName, Policy=bucket_policy)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def uploadFiles(dir="", bucket=''):
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
                ext =  file.rsplit('.', 1)[1]
                objectName = '{}/{}'.format(relativePath,
                                            file).replace("\\", "/")[1:]
                v = file if index == 0 else objectName
                s3_client.put_object(Body=open(path.join(root, file), mode='rb'),
                                     Bucket=bucket,
                                     Key=v,
                                     ContentType=mimeType(ext))
            except ClientError as e:
                logging.error(e)
                return False,"Error.."
    return True,"Website Up .."
