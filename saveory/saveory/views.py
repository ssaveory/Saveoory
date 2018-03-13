from flask import Flask, render_template, redirect, url_for, request, session
from pymongo import MongoClient
from forms import SignupForm, SigninForm
from models import *
from flask_pymongo import PyMongo
import psycopg2
import os
import pandas as pd
import csv
from flask.ext.sqlalchemy import SQLAlchemy
import datetime 


from dateutil import parser


app = Flask(__name__)

app.secret_key = "$aveory"


app.config['MONGO_DBNAME'] = 'saveory' 
app.config['MONGO_URI'] = 'mongodb://localhost:27017/saveory'
mongo = PyMongo(app, config_prefix='MONGO')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://saveory:saveory@localhost:5432/saveory'
db = SQLAlchemy(app)






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
    fname = user.firstName
    
    #### Fetching data for the main table in home ####

    conn = psycopg2.connect("host=localhost dbname=saveory user=saveory password=saveory")

    cur = conn.cursor()
    cur.execute("""select datestamp as date from transactions where userid='%s' order by datestamp DESC limit 5""" % email)    
    conn.commit()
    dateList = cur.fetchall()
    cur.execute("""select action from transactions where userid='%s' order by datestamp DESC limit 5""" % email)    
    conn.commit()
    actionsList = cur.fetchall()
    cur.execute("""select amount from transactions where userid='%s' order by datestamp DESC limit 5""" % email)    
    conn.commit()
    amountList = cur.fetchall()
    cur.execute("""select category  from transactions where userid='%s' order by datestamp DESC limit 5""" % email)  
    conn.commit()
    categoryList = cur.fetchall()  
    
    values =[]
    for i in amountList:
	values.append(''.join(map(str, i)))    

    #####################################################

    ####fetching Data for the spend graph ####

    #Find current day in the month#
    todayDate = datetime.datetime.now().strftime('%Y%m%d')

    #Find first day in the month#
    todayDate = datetime.date.today()
    if todayDate.day > 25:
        todayDate += datetime.timedelta(7)
    monthStart= todayDate.replace(day=1).strftime('%Y%m%d')
    cur.execute("""select distinct category, sum(amount)  from transactions where userid='%s' and (datestamp between '%s' and '%s') group by userid, datestamp, category, action,amount""" % (email,monthStart,todayDate))
    conn.commit()

    labels = cur.fetchall()
 
    dct ={}
    for item in labels:
        if dct.has_key(item[0]):  
                 dct[item[0]] = dct[item[0]] + item[1]  
        else:  
                 dct[item[0]] = item[1]


    labels = dct
    cur.close()
    conn.close()
    return render_template('main.html',dateList=dateList, actionsList=actionsList, values=values, categoryList=categoryList, labels=labels)


####################################################
@app.route('/upload', methods=['GET','POST'])
def upload():


    #Getting the files from the request
    bankfile = request.files['bank_file']  if 'bank_file' in request.files else False
    cardfile = request.files['card_file'] if 'card_file' in request.files else False

#creating a connection to the database
    conn = psycopg2.connect("host=localhost dbname=saveory user=saveory password=saveory")
    cur = conn.cursor()
    email= session['email']


####### Reading Bank file and dump it to the database transactions table #######
    if bankfile :
        bank =pd.read_csv(bankfile)

        #converting to dataframe
        df = pd.DataFrame(bank)
        #dump the user data to the database
        for index, row in df.iterrows():
            cur.execute('INSERT INTO transactions VALUES(%s,%s,%s,%s,%s)',(email,parser.parse(row['Date']).strftime('%Y%m%d'), row['Action'], row['Amount'], row['Discription']))
            conn.commit()
        
####### Reading Cridet card file and dump it to the database transactions table #######
    if cardfile :
        card =pd.read_csv(cardfile)

        #converting to dataframe
        df = pd.DataFrame(card)
        #dump the user data to the database
        for index, row in df.iterrows():
            cur.execute('INSERT INTO transactions VALUES(%s,%s,%s,%s,%s)',(email,parser.parse(row['Date']).strftime('%Y%m%d'), row['Action'], row['Amount'], row['Discription']))
            conn.commit()

#Closing the connection to the database

    cur.close()
    conn.close()


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
    app.run(host='0.0.0.0',port=5000, debug=True)

