import boto3
import os

s3 = boto3.client('s3')
response = s3.list_objects(
    Bucket='deplosite-logging')

try:
    l=[]
    prevFileName=""
    if len(response["Contents"])!=0:
        for item in response['Contents']:
            currentFileName=item['Key'].split(":")[0]
            pathName=os.path.join(os.getcwd(),'logs',currentFileName)
            if prevFileName!=currentFileName:
                exists=os.path.exists(pathName)
                if not exists:
                    os.mkdir(pathName,mode = 0o666)
            prevFileName=currentFileName
            l.append(item['Key'])
            s3.download_file('deplosite-logging',item['Key'],os.path.join(pathName,item['Key'].split(":")[1]))

        for item in l:
            s3.delete_object(Bucket='deplosite-logging',Key=item)
except Exception as e:
    print(e)    

