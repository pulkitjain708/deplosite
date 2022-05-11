import site
from flask import (redirect, request as req, flash, session, jsonify)
from models.dynSite import DSite
from datetime import date
from config import UPLOAD_PATH
import os
import boto3

EC2_Settings={
   # "AWS_REGION":'ap-south-1',
    "KeyName":"deplosite",
    "ImageId":"ami-0756a1c858554433e",
    "InstanceType":"t2.micro",
    "SecurityGroupIds":["sg-059f872cd3cee6310"],
    "MinCount":1,
    "MaxCount":1,
    "SubnetId":" subnet-0c7ed55ec9ad92b21"
}

def dyn():
    id = session['id']
    title = req.form['title'].strip().lower()
    file = req.files['file']
    stack=req.form['stack']
    filename = file.filename
    dateT=date.today()
    path=os.path.join(UPLOAD_PATH, "zipped", filename)
    dyS=DSite(objectId=id,title=title,date_project=f'${dateT}',project_path=path,stack=stack)
    file.save(path)
    dyS.save()
    return redirect('/dashboard')

def ec2_on(siteId):
    title=DSite().getName(siteId)
    EC2_Settings['TagSpecifications']=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': title
                },
            ]
        },
    ]
    ec2_resource = boto3.resource('ec2')
    instances = ec2_resource.create_instances(**EC2_Settings)
    for instance in instances:
        DSite.setInstanceId(0,siteId,instance.id)
    DSite().toggleEC2_ON(siteId)
    return jsonify({"msg":f" {title} Instantiated !!"})

def toggleEC2(siteId,instanceId):
    ec2 = boto3.resource('ec2')
    for res in ec2.instances.filter(InstanceIds=[instanceId]):
        if res.id==instanceId:
            if res.state['Name']=='stopped':
                res.start()
                DSite().toggleEC2(instanceId)
                return jsonify({"msg":f" {instanceId} Started !!"})
            elif res.state['Name']=='running':
                res.stop()
                DSite().toggleEC2(instanceId)
                return jsonify({"msg":f" {instanceId} Stopped !!"})
            else:
                return jsonify({"msg":f" {instanceId} Waiting to be in State !!"})
    # return redirect("/dashboard/dynamic-sites")   