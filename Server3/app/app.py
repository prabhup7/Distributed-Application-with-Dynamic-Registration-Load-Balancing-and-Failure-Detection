from flask import Flask,redirect, url_for, Response, jsonify
from flask import request
from model import db
from model import User
from model import CreateDB
from model import app as application
import pickle

import simplejson as json
from sqlalchemy.exc import IntegrityError
import os
import httplib
from threading import Thread

import redis

print "this is starting"


# initate flask app
app = Flask(__name__)

@app.route('/')
def first():
	return " i am in root"

@app.route('/v1/expenses', methods= ['POST'])
def set_post():
	try:
		CreateDB(hostname = "mysqlserver")
		db.create_all()
		request_data = request.get_json(force=True)

		name = request_data['name']
		email = request_data['email']
		category = request_data['category']
		description = request_data['description']
		link = request_data['link']
		estimated_costs = request_data['estimated_costs']
		submit_date = request_data['submit_date']
		status = "pending"
		decision_date = ""
		
		expen = User(name,email,category,description,link,estimated_costs,submit_date,status,decision_date)
		db.session.add(expen)
		db.session.commit()

		user_obj = User.query.filter_by(email=email).first()
		id2 = user_obj.id
		dict2={'id':id2,'name':name,'email':email,'category':category,'description':description,'link':link,'estimated_costs':estimated_costs,'submit_date':submit_date,'status':status,'decision_date':decision_date}
		response1 = jsonify(dict2)
		response1.status_code =201

		return response1
		#return Response(json.dumps({'id':name3,'name':name,'email':email,'category':category,'description':description,'link':link,'submitdate':submitdate,'status':status,'decision_date':decision_date}),status=httplib.CREATED)
	except Exception,e:
		db.session.rollback()
		return str(e)
		

@app.route('/v1/expenses/<expense_id>', methods = ['GET'])
def set(expense_id):
	try:
		db.create_all()
		fields= User.query.filter_by(id=expense_id).all()
		users_dict = {}
		for user in fields:
			users_dict = {
							'id': user.id,
							'name': user.name,
							'email': user.email,
							'category': user.category,
							'description': user.description,
							'link': user.link,
							'estimated_costs': user.estimated_costs,
							'submit_date': user.submit_date,
							'status': user.status,
							'decision_date': user.decision_date
						    }
		

		if users_dict == {}:
			return Response(status=httplib.NOT_FOUND)
		else:
			response1 = jsonify(users_dict)
			response1.status_code =200
			return response1
		
	except Exception,e:
		return str(e)



@app.route('/v1/expenses/<expense_id>', methods = ['PUT'])
def setup3(expense_id):
	try:
		
		request_data = request.get_json(force=True)
		estimated_costs1 = request_data['estimated_costs']

		update = db.session.query(User).filter_by(id=expense_id).update({"estimated_costs":estimated_costs1})
		db.session.commit()
				
		return Response(status=httplib.ACCEPTED)
	except Exception,e:
		return str(e)	

@app.route('/v1/expenses/<expense_id>', methods = ['DELETE'])
def setup4(expense_id):
	try:
		delete_this = User.query.filter_by(id=expense_id).first()
		db.session.delete(delete_this)
		db.session.commit()
		return Response(status=httplib.NO_CONTENT)
		#return httplib.responses[httplib.NO_CONTENT]
	except:
		return "eerror in delete"
	
	

@app.route('/info')
def app_status():
	return json.dumps({'server_info':application.config['SQLALCHEMY_DATABASE_URI']})

# run app service 
if __name__ == "__main__":
	print "before calling port"
	def port():
		r = redis.Redis(host='localhost',port=6379)
		r.rpush('ports',5002)
		return "5000 is inserted in redis"
	port()
	
	print "after calling port"

	app.run(host="0.0.0.0", port=5002, debug=True, use_reloader=False)

