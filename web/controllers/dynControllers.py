from flask import (redirect, request as req, flash, session, jsonify)
from models.dynSite import DSite
from datetime import date
from config import UPLOAD_PATH
import os

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
    print(siteId)
    return jsonify({"msg":"Instantiated !!"})