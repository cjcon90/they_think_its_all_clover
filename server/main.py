from pymongo import MongoClient
from flask import Flask, jsonify
import os
import json
from bson import json_util

user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
cluster = os.environ.get('DB_CLUSTER')
collection = os.environ.get('DB_COLL')
# Connect to MongoDB database
client = MongoClient(f"mongodb+srv://{user}:{password}@{cluster}.wijab.mongodb.net/{collection}?retryWrites=true&w=majority")
db = client['they_think_its_all_clover']
coll = db['tweet']

app = Flask(__name__)

# parse BSON data so it is usable for jsonify to return as JSON
# https://stackoverflow.com/a/18405626
def parse_json(data):
    return json.loads(json_util.dumps(data))

# return as json with success code of 200
@app.route('/tweets')
def tweets():
    total = coll.count()
    data = (parse_json(coll.find().limit(100)))
    return jsonify(tweets=data, total=total), 200

app.run()