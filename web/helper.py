from os import walk, path, remove
import boto3
import logging
from botocore.exceptions import ClientError
from platform import system
import json
from config import HCTI_ID, HCTI_KEY
import os
import shutil
import requests
from requests.exceptions import HTTPError


def enableLogging(bucketName):
    s3 = boto3.resource('s3')
    bucket_logging = s3.BucketLogging(bucketName)

    BucketLoggingStatus = {
        'LoggingEnabled': {
            'TargetBucket': 'deplosite-logging',
            'TargetPrefix': '{}:'.format(bucketName)
        }
    }

    bucket_logging.put(
        BucketLoggingStatus=BucketLoggingStatus)


def getThumbnail(url):
    response = os.popen(
        """curl -X POST https://hcti.io/v1/image -u '{}:{}' --data-urlencode url='{}' > out.json """.format(HCTI_ID, HCTI_KEY, url)).read()
    with open('out.json') as f:
        res = json.load(f)
        return res['url']


def removeBucket(bucketName):
    cmd = 'aws s3 rb --force s3://{}'.format(bucketName)
    response = os.popen(cmd).read()
    if "remove_bucket" in response.split(":"):
        return True
    else:
        return False


def mimeType(ext):
    mime = ""
    if ext == 'css':
        mime = "text/css"
    elif ext == 'html':
        mime = "text/html"
    elif ext == "js":
        mime = "application/javascript"
    elif ext == "png":
        mime = "image/png"
    elif ext == "svg":
        mime = "image/svg+xml"
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
                try:
                    ext = file.rsplit('.', 1)[1]
                    if ext not in allowed:
                        purepath = path.join(root, file)
                        remove(purepath)
                except Exception as e:
                    purepath = path.join(root, file)
                    remove(purepath)
                    print(e)

    return True, "Operation Completed"


def create_bucket(bucketName='', error="", index="", region="ap-south-1"):
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
        return s3_client.get_bucket_website(Bucket=bucketName)
    except ClientError as e:
        logging.error(e)
        return False
    # return True


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
                if "." not in file:
                    continue
                ext = file.rsplit('.', 1)[1]
                objectName = '{}/{}'.format(relativePath,
                                            file).replace("\\", "/")[1:]
                v = file if index == 0 else objectName
                s3_client.put_object(Body=open(path.join(root, file), mode='rb'),
                                     Bucket=bucket,
                                     Key=v,
                                     ContentType=mimeType(ext))
            except ClientError as e:
                logging.error(e)
                return False, "Error.."
    return True, "Website Up .."

def periodic():
    s3 = boto3.client('s3')
    response = s3.list_objects(
        Bucket='deplosite-logging')

    try:
        l = []
        prevFileName = ""
        if len(response["Contents"]) != 0:
            for item in response['Contents']:
                currentFileName = item['Key'].split(":")[0]
                pathName = os.path.join(os.getcwd(), 'logs', currentFileName)
                if prevFileName != currentFileName:
                    exists = os.path.exists(pathName)
                    if not exists:
                        os.mkdir(pathName, mode=0o666)
                prevFileName = currentFileName
                l.append(item['Key'])
                s3.download_file(
                'deplosite-logging', item['Key'], os.path.join(pathName, item['Key'].split(":")[1]))
            for item in l:
                s3.delete_object(Bucket='deplosite-logging', Key=item)
    except Exception as e:
        print(e)

    logsPath=os.path.join(os.getcwd(),'logs')
    for index,(root,dir,files) in enumerate(os.walk(logsPath)):
        if os.path.isdir(root) and index!=0:
            logFileName=root.rsplit("/",1)[1]
            logFileNamePath=os.path.join(logsPath,"{}.csv".format(logFileName))
            print(logFileNamePath)
            with open(logFileNamePath,"a+") as filePointer:
                for file in files:
                    fileToRead=os.path.join(root,file)
                    fileToReadPointer=open(fileToRead,'r')
                    filePointer.write(fileToReadPointer.read()+"\n")
            shutil.rmtree(root)

