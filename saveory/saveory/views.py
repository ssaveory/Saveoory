#from saveory import app
from flask import Flask, render_template, redirect, url_for, request, session
from pymongo import MongoClient
from db import mongo
from forms import SignupForm, SigninForm


app = Flask(__name__)

app.secret_key = "$aveory"




@app.route('/')
def index():
	return render_template('index.html',lform=SignupForm(),rform=SigninForm())


@app.route('/register', methods=['GET', 'POST'])
def register():
    #error = None
    lform = SignupForm(request.form, prefix="SignupForm")
    #print(request.form)
    if request.method == 'POST':

        if lform.validate() == False:
            return render_template('index.html', lform=lform, rform=SigninForm())
        else:
            return  "register"


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    rform = SigninForm(request.form, prefix="SigninForm")
    if request.method == 'POST':
        if rform.validate() == False:
            return render_template('index.html', rform=rform, lform=SignupForm())
        else:
            return "signig"


if __name__ == '__main__':
    #app.secret_key = '$aveory'
    app.run(host='0.0.0.0',port=5001,debug=True)
