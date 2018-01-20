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
            credentials = { "firstName" : lform.firstName.data,
                             "lastName" : lform.lastName.data, 
                             "email" : lform.email.data,
                             "password" : lform.password.data
                             }
            newUser = User(True,**credentials)
            try:
                newUser.addUser()
            except 'userNotExist':
                return render_template('index.html', lform=lform, rform=SigninForm())
            session['email'] = newUser.email
            return  render_template('profile.html',newUser=True)


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
                session['email'] = rform.email.data
                return redirect(url_for('home'))
            return render_template('index.html', rform=rform, lform=SignupForm())

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('email', None)
    return render_template('index.html',lform=SignupForm(),rform=SigninForm())



@app.route('/home', methods=['GET','POST'])
def home():
    return render_template('main.html')

@app.route('/upload', methods=['GET','POST'])
def upload():
    return render_template('main.html')



@app.route('/profile', methods=['GET','POST'])
def profile():
    return render_template('profile.html')

@app.route('/analyze', methods=['GET','POST'])
def analyze():
    return render_template('main.html')

@app.route('/masswiz', methods=['GET','POST'])
def masswiz():
    return render_template('main.html')




if __name__ == '__main__':
    #app.secret_key = '$aveory'
    app.run(host='0.0.0.0',port=5001,debug=True)
