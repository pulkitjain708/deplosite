from flask import (render_template,
                   request as req,
                   session)
from models.staticSite import Site
from os import walk, path , getcwd
import boto3
from datetime import date
import pandas as pd

rownames=['Bucket Owner', 'Bucket', 'Time', 'Time - Offset', 'Remote IP', 'Requester ARN/Canonical ID',
                                          'Request ID',
                                          'Operation', 'Key', 'Request-URI', 'HTTP status', 'Error Code', 'Bytes Sent', 'Object Size',
                                          'Total Time',
                                          'Turn-Around Time', 'Referrer', 'User-Agent', 'Version Id', 'Host Id', 'Signature Version',
                                          'Cipher Suite',
                                          'Authentication Type', 'Host Header', 'TLS version']
usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                          13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]


def sendDash():
    username = session['username']
    return render_template('dashpages/dash.html', username=username, page="Dashboard")


def sendListSites():
    username = session['username']
    id = session['id']
    projection = {"title": 1, "url": 1, "_id": 0, "img": 1, "bucketName": 1}
    lst = Site().getStaticSitesByUser(id, projection)
    return render_template('dashpages/listSites.html', username=username, page="List Sites", sites=lst)


def sendStats():
    username = session['username']
    return render_template('dashpages/stats.html', username=username, page="Statistics")


def sendNewSite():
    username = session['username']
    return render_template('dashpages/deploy-options.html', username=username, page="New Site")


def individualStats(bucketName):
    metricData = {}
    Metrics = ['BucketSizeBytes', 'NumberOfObjects']
    NumberOfObjects = {
        'Name': 'StorageType',
        'Value': 'AllStorageTypes'
    }
    BucketSizeBytes = {
        'Name': 'StorageType',
        'Value': 'StandardStorage'
    }
    cw = boto3.client('cloudwatch')
    s3 = boto3.client('s3')
    username = session['username']
    id = session['id']
    if bucketName not in ["", " "]:
        response = Site().userHasBucket(id, bucketName)
        if response:
            todayDate = date.today()
            setDate = response['date']

            for metric in Metrics:
                response = cw.get_metric_statistics(Namespace='AWS/S3', Dimensions=[
                    {
                        'Name': 'BucketName',
                        'Value': bucketName
                    },
                    NumberOfObjects if metric == Metrics[1] else BucketSizeBytes
                ],
                    MetricName=metric,
                    StartTime=setDate,
                    EndTime=todayDate,
                    Statistics=["SampleCount", "Average",
                                "Sum", "Minimum", 'Maximum'],
                    Period=60*60*24*2)

                metricData[metric] = response['Datapoints']
            
            dataPath=path.join(getcwd(),'logs','{}.csv'.format(bucketName))

            data=pd.read_csv(dataPath,sep=" ",names=rownames,usecols=usecols,engine='python')

            return '{}'.format(data)
            
