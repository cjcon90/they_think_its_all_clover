from pymongo import MongoClient
from flask import Flask, jsonify
import os
import json
from bson import json_util

# Connect to MongoDB database
client = MongoClient(f"mongodb+srv://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_CLUSTER')}.wijab.mongodb.net/{os.environ.get('DB_COLL')}?retryWrites=true&w=majority")
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
    data = (parse_json(coll.find()))
    return jsonify(tweets=data), 200

app.run()