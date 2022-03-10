from flask import render_template , request as req , redirect , flash
import models
import re
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def sendSlash():
    return render_template('index.html')

def sendLogin():
    return render_template('login.html')

def sendRegister():
    return render_template('register.html')

def registerUser():
    username=req.form['username'].strip()
    email=req.form['email'].strip()
    password=req.form['password'].strip()
    if (username == "" or email=="" or password=="") or (not username.isalnum() or not len(password)>=8 or not re.fullmatch(regex, email)):
        flash('Credentials dont meet criteria')
        return redirect('/register')
    result = models.user.User(username=username,email=email,password=password).save()
    if result==True:
        flash('Try Logging in with your Account')
        return redirect('/login')
    elif result==False:
        flash('Username or Email already exist')
        return redirect('/register')

def loginUser():
    username=req.form['username']
    password=req.form['password']
    return redirect('/')

