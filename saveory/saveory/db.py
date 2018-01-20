from flask import Flask
from flask_pymongo import PyMongo
from views import *

app.config['MONGO_DBNAME'] = 'saveory' 
app.config['MONGO_URI'] = 'mongodb://localhost:27017/saveory'

mongo = PyMongo(app, config_prefix='MONGO')


