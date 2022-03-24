from flask import (render_template,
                    request as req,
                    session)
from models.staticSite import Site
from os import walk,path

def sendDash():
    username=session['username']
    return render_template('dashpages/dash.html',username=username,page="Dashboard")

def sendListSites():
    username=session['username']
    id=session['id']
    projection={"title":1,"url":1,"_id":0,"img":1,"bucketName":1}
    lst=Site().getStaticSitesByUser(id,projection)
    return render_template('dashpages/listSites.html',username=username,page="List Sites",sites=lst)

def sendStats():
    username=session['username']
    return render_template('dashpages/stats.html',username=username,page="Statistics")

def sendNewSite():
    username=session['username']
    return render_template('dashpages/deploy-options.html',username=username,page="New Site")

def individualStats(bucketName):
    if bucketName not in [""," "]:
        pass