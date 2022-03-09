from main import mongo
from flask import render_template , request as req , redirect


def sendSlash():
    return render_template('html/index.html')

def sendLogin():
    return render_template('html/login.html')

def sendRegister():
    return render_template('html/register.html')

def registerUser():
    username=req.form['username']
    email=req.form['email']
    password=req.form['password']
    print(mongo)
    return redirect('/')
