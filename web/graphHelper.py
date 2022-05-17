import boto3
from PIL import Image
import io
import json
import datetime as DT

cloudwatch = boto3.client('cloudwatch')

metrics=['NetworkPacketsIn','NetworkPacketsOut','CPUUtilization',
'NetworkIn','NetworkOut','DiskReadBytes','DiskWriteBytes','DiskReadOps','DiskWriteOps','CPUCreditUsage',
'CPUCreditBalance']

def genGraphs(instanceId):
    today = DT.date.today()
    before = today - DT.timedelta(days=7)
    for index,metric in enumerate(metrics):
        MetricWidget=json.dumps({"metrics":[['AWS/EC2',metric,'InstanceId',instanceId]],"start":str(before),"end":str(today)})
        response = cloudwatch.get_metric_widget_image(MetricWidget=MetricWidget,OutputFormat='png')
        im = Image.open(io.BytesIO(response["MetricWidgetImage"]))
        im.save('static/graphs/{}.png'.format(index+1))
