from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['accounts_database']
collection = db['accounts']
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    elif request.method == "POST":
        # Do signup stuff
        if request.form['password'] != request.form['confirm-password']:
            return "Passwords don't match!"
        elif bool(collection.find_one({'Username': request.form['username']})):
            return "Account already exists!"
        else:
            username = request.form['username']
            password = request.form['password']
            
            to_db = {
                'Username': username,
                'Password': password,
            }
            collection.insert_one(to_db)
            return str("Created account " + username + "!")

@app.route('/login', methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if bool(collection.find_one({"Username": username})):
            if password == collection.find_one({"Username": username})['Password']:
                return redirect(url_for('home'))
        error='Invalid Username of Password. Please try again.'

    return render_template('landing.html', error=error)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)