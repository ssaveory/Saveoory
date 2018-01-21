from flask import Flask, render_template, redirect, url_for, request, session
from pymongo import MongoClient
from forms import SignupForm, SigninForm
from models import *
from flask_pymongo import PyMongo
import psycopg2
import os
import pandas as pd
import csv



app = Flask(__name__)

app.secret_key = "$aveory"


app.config['MONGO_DBNAME'] = 'saveory' 
app.config['MONGO_URI'] = 'mongodb://localhost:27017/saveory'
mongo = PyMongo(app, config_prefix='MONGO')

#app.config.from_object('APP_SETTING')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://saveory:saveory@localhost:5432/saveory'
#db = SQLAlchemy(app)

#with app.app_context():
    #db.create_all()
    #conn = psycopg2.connect("host=localhost dbname=saveory user=saveory password=saveory")
   # cur = conn.cursor()
  #  cur.execute("CREATE TABLE transactions("User" VARCHAR(40) PRIMARY KEY, datestamp VARCHAR(40), category VARCHAR(40), description VARCHAR(40), amount FLOAT, action VARCHAR(40));")






@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('home'))
    return render_template('index.html',lform=SignupForm(),rform=SigninForm())

####################################################




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
            session['password'] = lform.password.data
            return  render_template('profile.html', fname = newUser.firstName,
                                                    lname = newUser.firstName,
                                                    city = None,
                                                    fstatus = None,
                                                    licond = None,
                                                    numppl = None,
                                                    empstatus = None,
                                                    age = None)

####################################################





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
                session['password'] = rform.password.data
                return redirect(url_for('home'))
            return render_template('index.html', rform=rform, lform=SignupForm())


####################################################



@app.route('/logout', methods=['GET'])
def logout():
    session.pop('email', None)
    session.pop('password',None)
    return render_template('index.html',lform=SignupForm(),rform=SigninForm())


####################################################




@app.route('/home', methods=['GET','POST'])
def home():
    if 'email' not in session:
        return redirect(url_for('index'))
    email= session['email']
    credentials = { "email" : email }
    user = User(False,**credentials)
    print user.firstName
    fname = user.firstName
    return render_template('main.html')


####################################################
@app.route('/upload', methods=['GET','POST'])
def upload():
    
    #bankfile = request.files['bank_file']
    #cardfile = request.files['card_file']
    #bank = pd.read_table(bankfile)
    #for row in bank:
     #   print(row)

    return redirect(url_for('home'))


@app.route('/savemoney', methods=['GET','POST'])
def save():
    return redirect(url_for('home'))


@app.route('/manualupload', methods=['GET','POST'])
def manual():
    return redirect(url_for('home'))



####################################################


@app.route('/profile', methods=['GET','POST'])
def profile():
    return render_template('profile.html' )
    email= session['email']
    password = session['password']
    credentials = { "firstName": request.form['fname'], "lastName": request.form['lname'],"email" : email,
                    "password" : password, "city": request.form['city'],
                    "familyStatus": request.form['family'], "livingConditions": request.form['living'],
                     "numOfRoomMate": request.form['people'], "employmentStatus": request.form['job'],
                     "age": request.form['bday'] }
    
    profile = Profile(**credentials)
    if request.method == 'POST':
        profile.editProfile()
        return render_template('main.html' )
    return  render_template('profile.html', fname = request.form['fname'],
                                                    lname = request.form['lname'],
                                                    city = None,
                                                    fstatus = None,
                                                    licond = None,
                                                    numppl = None,
                                                    empstatus = None,
                                                    age = None)






####################################################
@app.route('/analyze', methods=['GET','POST'])
def analyze():
    labels = ["January","February","March","April","May","June","July","August"]
    values = [10,9,8,7,6,4,7,8]
    return render_template('analyze.html', values = values, lasbels = labels)

@app.route('/masswiz', methods=['GET','POST'])
def masswiz():
    return render_template('masswiz.html')




if __name__ == '__main__':
    #app.secret_key = '$aveory'
    app.run(host='0.0.0.0',port=5000,debug=True)
