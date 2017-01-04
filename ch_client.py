from flask import Flask,jsonify
from flask import request
import collections
import random
import math
import simplejson as json
import requests
from ConsistentHashing import ConsistentHashRing

# initate flask app
app = Flask(__name__)
chr = ConsistentHashRing()
chr["1"]="localhost:5000"
chr["2"]="localhost:5001" 
chr["3"]="localhost:5002"

@app.route('/')
def index():
	return 'Hello World! from Http Client\n'

#post method to redirect to the apps based on consistent hashing
@app.route('/v1/expenses',methods=['POST'])
def post_expense_to_instances():
	json_data= json.loads(request.data)
	if not json_data or not 'id' in json_data:
		abort(404)
	new_id = json_data['id']
	app = chr[str(new_id)]
	new_url ="http://"+app+"/v1/expenses"
	print new_url
	forward = requests.post(new_url,data=json.dumps(json_data))
	resp = jsonify({"status":forward.status_code})
	return resp

#get method to return values based on consistent hashing
@app.route('/v1/expenses/<expense_id>',methods =['GET'])
def get_expense_from_instances(expense_id):
	app=chr[str(expense_id)]
	new_url = "http://"+app+"/v1/expenses/"+expense_id
	forward = requests.get(new_url)
	print forward.url
	return forward.text

if __name__ =="__main__":
	app.run(host="0.0.0.0",port=5010, debug = True)
