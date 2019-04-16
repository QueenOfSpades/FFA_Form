import urllib.parse
import urllib.request
import boto3
from flask import Flask, request, render_template
import json



application = Flask(__name__)

with open("keys.txt") as json_file:
    json_data = json.load(json_file)

dynamodb = boto3.client('dynamodb', region_name='us-east-1',
	aws_access_key_id=json_data["keyId"],
    aws_secret_access_key=json_data["secretKey"])

@application.route('/')
def my_form():
    return render_template('FFA_form.html')

	

@application.route('/', methods=['POST'])
def my_form_post():	
	data = request.values
	requestL = dict()

	for key, value in data.items(multi=True):
		if len(value) > 0:
			#print(key+ ", " + value)
			#classN = value.__class__.__name__.upper();
			if key in requestL:
				requestL[key][classN[0]] = requestL[key][classN[0]] + ", " + value
			else:
				classN = value.__class__.__name__.upper();
				requestL[key] = {classN[0]:value}

	
	print(requestL)
	try:
		dynamodb.put_item(TableName="clients", ConditionExpression= 'attribute_not_exists(clientName)', Item=requestL)
	except:
		return "Already in the database"

	return "Input Captured"
	
	
	
if __name__ == '__main__':
	application.run()