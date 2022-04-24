from flask import (redirect, request as req, flash, session)
from models.dynSite import DSite
from datetime import date
from config import UPLOAD_PATH
import os

def dyn():
    id = session['id']
    title = req.form['title'].strip().lower()
    file = req.files['file']
    filename = file.filename
    date=date.today()
    path=os.path.join(UPLOAD_PATH, "zipped", filename)
    dyS=DSite(objectId=id,title=title,date_project=date,project_path=path)
    file.save(path)
    dyS.save()
    return redirect('/dashboard')