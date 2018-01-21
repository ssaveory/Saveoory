from werkzeug.security import generate_password_hash, check_password_hash
#from db import mongo
from flask import Flask
from views import mongo 


#main user object
#4 mandatory should be passed as a dictionary in this orded:
# {"first"}
#newUser to indicate if we are creating a new user or getting the profile of new user.
class User(object):
	#getting the database "saveory"
	#usersDb = mongo
	#tableName = 'usersData'
	def __init__(self, newUser, **kwargs):
		if newUser :
			self.firstName = kwargs['firstName'].title()
			self.lastName = kwargs['lastName'].title()
			self.email = kwargs['email']
			self.hashPassword = kwargs['password']
			#self.hashPass = self.hashPassword(self,kwargs['password'])

		else :
			res = mongo.db.usersData.find_one({'email' : kwargs['email']})
			if res == None:
				return "userNotExist" #if the newUser is 0 and the user is not exist.
			else :
				self.firstName = res['firstName']
				self.lastName = res['lastName']
				self.email = res['email']
				self.hashPassword = res['hashPassword']
				self.city = res['city']
				self.familyStatus = res['familyStatus']
				self.livingConditions = res['livingConditions']
				self.numOfRoomMate = res['numOfRoomMate']
				self.employmentStatus = res['employmentStatus']
				self.age = res['age']

	
	#Insert the user to the database    
	#@classmethod
	def addUser(self):
		data = mongo.db.usersData
		res = data.find_one({'email' : self.email})
		if res != None :
			return "exist"
		#print(self.hashPass)
		data.insert(
			{
				"firstName" : self.firstName,
				"lastName" : self.lastName,
				"email" : self.email,
				"hashPassword" : self.hashPassword,
				"age" : None,
				"city" : None,
				"familyStatus" : None, 
				"livingConditions" : None,
				"numOfRoomMate" : None,
				"employmentStatus" : None  
			}
		)
	def checkPass(self, password):
		if self.hashPassword == password:
			return True
		return False


	@staticmethod
	def hashPassword(self,password):
		return  generate_password_hash(password)
	#@classmethod
	def cehckPassword(self, password):
		return check_password_hash(self.hashPass,password)



#Profile class - defining the user profile
#the following fields are optional (default value is None) :
#age, city, familyStatus, livingConditions, numOfRoomMate, employmentStatus
class Profile(object):
	def __init__(self, **kwargs):
		self.firstName = kwargs['firstName']
		self.lastName = kwargs['lastName']
		self.email = kwargs['email']
		self.hashPassword = kwargs['password']
		self.age = kwargs['age']
		self.city = kwargs['city']
		self.familyStatus = kwargs['familyStatus']
		self.livingConditions = kwargs['livingConditions']
		self.numOfRoomMate = kwargs['numOfRoomMate']
		self.employmentStatus = kwargs['employmentStatus']
	    
	def editProfile(self):
		data = mongo.db.usersData
		data.update({"email": self.email}, {'$set':  {"firstName" : self.firstName } })
		data.update({"email": self.email}, {'$set' : {"lastName" : self.lastName }} )
		data.update({"email": self.email}, {'$set' : {"age" : self.age }})
		data.update({"email": self.email}, {'$set' : {"city" : self.city }})
		data.update({"email": self.email}, {'$set' : {"familyStatus" : self.familyStatus }})
		data.update({"email": self.email}, {'$set' : {"livingConditions" : self.livingConditions }})
		data.update({"email": self.email}, {'$set' : {"numOfRoomMate" : self.numOfRoomMate }})
		data.update({"email": self.email}, {'$set' : {"employmentStatus" : self.employmentStatus }})




	#transactions = db.relationship('user', 'datestamp', 'category', 'description', 'amout', 'action')
	