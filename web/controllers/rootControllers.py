from flask import (render_template , 
                    request as req , 
                    redirect , 
                    flash , 
                    session)
import models
import re
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def sendSlash():
    return render_template('separate/main.html')

def sendLogin():
    return render_template('separate/login.html')

def sendRegister():
    return render_template('separate/register.html')

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
    username=req.form['username'].strip()
    password=req.form['password'].strip()
    if (username == "" or  password=="") or (not username.isalnum() or not len(password)>=8):
        flash('Credentials dont meet criteria')
        return redirect('/login')
    user=models.user.User(username=username,password=password).doesExist(login=1)
    if user:
        session['id']=user["_id"]
        session['username']=username
        return redirect('/dashboard')


def logout():
    session.pop('username',None)
    return redirect('/')

