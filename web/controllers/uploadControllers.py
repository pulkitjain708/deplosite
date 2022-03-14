from flask import (render_template,
                   request as req,
                   redirect,
                   flash,
                   session)
from config import UPLOAD_PATH, ALLOWED
from werkzeug.utils import secure_filename
import os
from shutil import unpack_archive
from helper import checkStatic,uploadFiles,create_bucket
from random import randint

def static():
    '''
    Test Cases
    1) title root description not be empty
    2) root should always be *.html / *.htm
    3) file should always be *.zip
    4) root_file_name to be present at root of file 
    5) only allowed files- media , css , js html ?
    '''
    errs = ""
    title = req.form['title'].strip()
    root = req.form['root'].strip()
    description = req.form['description'].strip()
    file = req.files['file']
    filename = file.filename
    bucketName="www.{}-{}-deplosite.com".format(title,randint(999,99999))
    parsed_name, ext = filename.rsplit(".", 1)
    username = session['username']
    if title == "" or root == "" or description == "":
        errs += "Upload Information not Specified,"
    if root != "" and not (root.rsplit(".", 1)[1] in ['htm', 'html']):
        errs += "The Specified root file is not html,"
    if filename == "" or ext != 'zip':
        errs += ' The Uploading file is not specified or is not zip .'
    if(errs == ""):
        filename = secure_filename(filename)
        file.save(os.path.join(UPLOAD_PATH, "zipped", filename))
        unpack_archive(os.path.join(UPLOAD_PATH, "zipped", filename),
                       os.path.join(UPLOAD_PATH, "unzipped", filename))
        absPath = os.path.join(UPLOAD_PATH, "unzipped", filename)
        flag, message = checkStatic(
            dir=absPath, allowed=ALLOWED, rootFile=root)
        # if flag:
        #     flash(message+", Try Checking Status in List of Deployments")
        create_bucket(bucketName=bucketName,error=root,index=root)
        uploadFiles(dir=absPath,bucket=bucketName)
        return redirect('/dashboard/new-site')
    else:
        flash(errs)
    return redirect('/dashboard/new-site')
