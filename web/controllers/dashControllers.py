from flask import (render_template,
                    request as req,
                    session)

def sendDash():
    username=session['username']
    return render_template('dashpages/dash.html',username=username,page="Dashboard")

def sendListSites():
    username=session['username']
    return render_template('dashpages/listSites.html',username=username,page="List Sites")

def sendStats():
    username=session['username']
    return render_template('dashpages/stats.html',username=username,page="Statistics")

def sendNewSite():
    username=session['username']
    return render_template('dashpages/deploy-options.html',username=username,page="New Site")