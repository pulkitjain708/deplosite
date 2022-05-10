from flask import (redirect, render_template,
                   request as req,
                   session)
from models.staticSite import Site,getDb
from models.dynSite import DSite
from os import walk, path, getcwd
import boto3
from datetime import date, datetime
import pandas as pd
import math
import json

rownames = ['Bucket Owner', 'Bucket', 'Time', 'Time - Offset', 'Remote IP', 'Requester ARN/Canonical ID',
            'Request ID',
            'Operation', 'Key', 'Request-URI', 'HTTP status', 'Error Code', 'Bytes Sent', 'Object Size',
            'Total Time',
            'Turn-Around Time', 'Referrer', 'User-Agent', 'Version Id', 'Host Id', 'Signature Version',
            'Cipher Suite',
            'Authentication Type', 'Host Header', 'TLS version']
usecols = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
           13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]


def sendDynamicSites():
    username = session['username']
    id = session['id']
    sites=list(DSite().getSites(id))
    print(sites)
    return render_template('index.html',username=username,id=id,sites=sites)

def changeEmail(username):
    email=req.form['email']
    res=getDb(collection="user").find_one_and_update({"username":username},{"$set":{"email":email}})
    print(res)
    return redirect("/dashboard")

def changePassword(username):
    password=req.form['password']
    res=getDb(collection="user").find_one_and_update({"username":username},{"$set":{"password":password}})
    print(res)
    return redirect('/dashboard')

def sendDash():
    username = session['username']
    id = session['id']
    imgs = Site().getImageLinksforUserSite(id)
    return render_template('dashpages/dash.html', username=username, page="Dashboard", images=imgs,id=id)


def sendListSites():
    username = session['username']
    id = session['id']
    projection = {"title": 1, "url": 1, "_id": 0, "img": 1, "bucketName": 1}
    lst = Site().getStaticSitesByUser(id, projection)
    return render_template('dashpages/listSites.html', username=username, page="List Sites", sites=lst,id=id)


def sendNewSite():
    username = session['username']
    id = session['id']
    
    return render_template('dashpages/deploy-options.html', username=username,id=id)


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
                    StartTime=datetime(
                        setDate.year, setDate.month, setDate.day),
                    EndTime=datetime(
                        todayDate.year, todayDate.month, todayDate.day),
                    Statistics=["SampleCount", "Average",
                                "Sum", "Minimum", 'Maximum'],
                    Period=60*60*24*2)

                metricData[metric] = math.floor(
                    response['Datapoints'][0]['Maximum'])

            dataPath = path.join(getcwd(), 'logs', '{}.csv'.format(bucketName))

            data = pd.read_csv(dataPath, sep=" ", names=rownames,
                               usecols=usecols, engine='python')

            # data.to_csv('a.csv')
            fixes = ['Bytes Sent', 'Object Size',
                     'Total Time', 'Turn-Around Time']
            data[fixes] = data[fixes].replace('-', 0)
            data[fixes] = data[fixes].astype(int)
            # Metric 3 : unique ip
            metricData['unique_IP'] = data['Remote IP'].unique()
            # Metric 4 : total requests
            metricData['total_requests'] = len(data)
            # Metric 5 : average bites served
            metricData['average_bytes_served'] = math.floor(
                data['Bytes Sent'].mean())
            # Metric 6 : average object size
            metricData['average_object_size'] = math.floor(
                data['Object Size'].mean())
            # Metric 7 : average total time
            metricData['average_time'] = math.floor(data['Total Time'].mean())
            # Metric 8 : average turn around time
            metricData['average_turn_time'] = math.floor(
                data['Turn-Around Time'].mean())
            # Metric 8 : referer list
            metricData['referrer'] = data['Referrer'].unique()
            # website only requests , checking user agent
            c = 0
            for agent in data['User-Agent']:
                if 'Boto3' not in agent and 'S3Console' not in agent:
                    c += 1
            metricData['web_rel_req'] = c
            # Requests for other static Resources , each count in bar graph
            newdf = []
            for index, (agent, key) in enumerate(zip(data['User-Agent'], data['Key'])):
                if 'Boto3' not in agent and 'S3Console' not in agent:
                    newdf.append(key)
            new = pd.Series(newdf)
            metricData['static_sources_requests'] = json.dumps({
                "labels": list(new.unique()), "values": list(new.value_counts())})
            # Requests for static resources and their response code
            dt = []
            for index, (agent, key, status) in enumerate(zip(data['User-Agent'], data['Key'], data['HTTP status'])):
                if 'Boto3' not in agent and 'S3Console' not in agent:
                    dt.append([key, status])
            metricData['static_response_code'] = dt
            # Linear Graph representing TAT
            dt = {"time": [], "tat": []}
            for index, (time, agent, tat) in enumerate(zip(data['Time'], data['User-Agent'], data['Turn-Around Time'])):
                if 'Boto3' not in agent and 'S3Console' not in agent:
                    dt['time'].append(time)
                    dt['tat'].append(tat)
            metricData['linear_tat'] = json.dumps(dt)
            # Linear Graph representing TT
            dt = {"time": [], "tt": []}
            for index, (time, agent, tt) in enumerate(zip(data['Time'], data['User-Agent'], data['Total Time'])):
                if 'Boto3' not in agent and 'S3Console' not in agent:
                    dt['time'].append(time)
                    dt['tt'].append(tt)
            metricData['linear_tt'] = json.dumps(dt)
            # return '{}'.format(metricData)
            return render_template('dashpages/stats.html', username=username, page="Stats : {}".format(bucketName), **metricData,id=id)
