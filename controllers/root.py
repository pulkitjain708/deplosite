from flask import render_template

def sendSlash():
    return render_template('html/index.html')

def sendLogin():
    return render_template('html/login.html')

def sendRegister():
    return render_template('html/register.html')