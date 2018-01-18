from werkzeug.security import generate_password_hash, check_password_hash
from db import mongo

#main user object
#4 mandatory should be passed as a dictionary in this orded:
# {"first"}
#newUser to indicate if we are creating a new user or getting the profile of new user.
class User(object):
	#getting the database "saveory"
	usersDb = mongo
	__tableName__ = 'usersData'
	def __init__(self, newUser, **kwargs):
		if newUser :
			self.firstName = kwargs['firstName'].title()
			self.lastName = kwargs['lastName'].title()
			self.email = kwargs['email']
			#self.password = kwargs['password']
			self.hashPass = self.hashPassword(kwargs['password'])

		else :
			res = usersDb.__tableName__.find_one({'email' : kwargs['email']})
			if res == None:
				return "userNotExist" #if the newUser is 1 and the user is not exist.
			else :
				self.firstName = res['firstName']
				self.lastName = res['lastName']
				self.email = res['email']
				self.hashPassw = res['hashPass']
				self.age = res['age']
				self.city = res['city']
				self.familyStatus = res['familyStatus']
				self.livingConditions = res['livingConditions']
				self.numOfRoomMate = res['numOfRoomMate']
				self.employmentStatus = res['employmentStatus']
	
	#Insert the user to the database    
	@classmethod
	def addUser(self):
		res = usersDb.__tableName__.find_one({'email' : self.email})
		if res != None :
			return "exist"
		self.usersDb.__tableName__.isnert(
			{
				"firstName" : self.firstName,
				"lastName" : self.lastName,
				"email" : self.email,
				"hashPassword" : self.hashPassword,
				"age" : null,
				"city" : null,
				"familyStatus" : null, 
				"livingConditions" : null,
				"numOfRoomMate" : null,
				"employmentStatus" : null  
			}
		)
	
	@staticmethod
	def hashPassword(self,password):
		return  generate_password_hash(password)
	@classmethod
	def cehckPassword(self, password):
		return check_password_hash(self.hashPass,password)



#Profile class - defining the user profile
#the following fields are optional (default value is None) :
#age, city, familyStatus, livingConditions, numOfRoomMate, employmentStatus
class Profile(User):
	def __init__(self,newUser, **kwargs):
		User.__init__(self,newUser,**kwargs)
		
		self.age = kwargs['age']
		self.city = kwargs['city']
		self.familyStatus = kwargs['familyStatus']
		self.livingConditions = kwargs['livingConditions']
		self.numOfRoomMate = kwargs['numOfRoomMate']
		self.employmentStatus = kwargs['employmentStatus']
	    
	def editProfile(**kwargs):
		for key, value in kwargs.iteritems():
			self.usersDb.__tableName__.update({ key : value})
		


