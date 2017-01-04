from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand



# Database Configurations
app = Flask(__name__)
DATABASE = 'newtest'
PASSWORD = 'password'
USER = 'root'
HOSTNAME = 'mysqlContainer1'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@mysqlContainer1/newtest'
db = SQLAlchemy(app)

# Database migration command line
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

class User(db.Model):

	__tablename__="expenses"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=False)
	email = db.Column(db.String(100), unique=True)
	category = db.Column(db.String(100), unique=False)
	description = db.Column(db.String(100), unique=False)
	link= db.Column(db.String(100), unique=False)
	estimated_costs= db.Column(db.String(100), unique=False)
	submit_date=db.Column(db.String(100), unique=False)
	status=db.Column(db.String(100), unique=False)
	decision_date = db.Column(db.String(100), unique=False)
	
	def __init__(self,name, email, category, description, link, estimated_costs, submit_date, status, decision_date):
		# initialize columns
		self.name = name
		self.email = email
		self.category = category
		self.description = description
		self.link= link
		self.estimated_costs = estimated_costs
		self.submit_date = submit_date
		self.status = status
		self.decision_date = decision_date



class CreateDB():
	def __init__(self, hostname=None):
		if hostname != None:	
			HOSTNAME = hostname
		import sqlalchemy
		engine = sqlalchemy.create_engine('mysql://root:password@mysqlContainer1') # connect to server
		engine.execute("CREATE DATABASE IF NOT EXISTS %s "%(DATABASE)) #create db

if __name__ == '__main__':
	
	manager.run()



    

    

    
