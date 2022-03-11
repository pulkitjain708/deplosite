from re import I
from flask import (render_template , 
                    request as req , 
                    redirect , 
                    flash , 
                    session)

def static():
    '''
    Test Cases
    1) title root description not be empty
    2) root should always be *.html / *.htm
    3) file should always be *.zip
    4) root_file_name to be present at root of file 
    '''
    errs=""
    title=req.form['title'].strip()
    root=req.form['root'].strip()
    description=req.form['description'].strip()
    file = req.files['file']
    filename=file.filename
    parsed_name,ext=filename.rsplit(".",1)
    
    if title=="" or root=="" or description=="":
        errs+="Upload Information not Specified,"
    if root!="" and not (root.rsplit(".",1) in ['htm','html']):
        errs+="The Specified root file is not html,"
    if filename=="" or ext!='zip':
        errs+=' The Uploading file is not specified or is not zip .'
    if(errs==""):
        flash(errs)
    else:
        flash("Uploading Zip..")
    return redirect('/dashboard/new-site')
    
    