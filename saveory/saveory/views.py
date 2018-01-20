#from saveory import app
from flask import Flask, render_template, redirect, url_for, request, session
from pymongo import MongoClient
#from db import mongo
from forms import SignupForm, SigninForm
from models import *
from flask_pymongo import PyMongo


app = Flask(__name__)

app.secret_key = "$aveory"
app.config['MONGO_DBNAME'] = 'saveory' 
app.config['MONGO_URI'] = 'mongodb://localhost:27017/saveory'

mongo = PyMongo(app, config_prefix='MONGO')



@app.route('/')
def index():
    return render_template('index.html',lform=SignupForm(),rform=SigninForm())


@app.route('/register', methods=['GET', 'POST'])
def register():
    
    lform = SignupForm(request.form, prefix="SignupForm")
    if request.method == 'POST':

        if lform.validate() == False:
            return render_template('index.html', lform=lform, rform=SigninForm())
        else:
            credentials = { 'firstName' : lform.firstName.data,
                             "lastName" : lform.lastName.data, 
                             "email" : lform.email.data,
                             "password" : lform.password.data
                             }
            newUser = User(True,**credentials)
            exist = newUser.addUser()
            if exist == "exist":
                return render_template('index.html', lform=lform, rform=SigninForm())
            return  render_template('profile.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    rform = SigninForm(request.form, prefix="SigninForm")
    if request.method == 'POST':
        if rform.validate() == False:
            return render_template('index.html', rform=rform, lform=SignupForm())
        else:
            credentials = { "email" : rform.email.data, "password" : rform.email.data}
            user = User(False,**credentials)
            #if exist == "userNotExist":
            #    return render_template('index.html', rform=rform, lform=SignupForm())
            if user.checkPass(rform.password.data):
                return render_template('main.html')
            return render_template('index.html', rform=rform, lform=SignupForm())


if __name__ == '__main__':
    #app.secret_key = '$aveory'
    app.run(host='0.0.0.0',port=5001,debug=True)
