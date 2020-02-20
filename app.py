from flask import request
from flask_api import FlaskAPI
from pprint import pprint
import json
from pymongo import MongoClient
from bson.json_util import dumps

# ? userID
# ? recordID
# ? consultant
# ? consEmail
# ? bizUnit- STL
# ? clientAcct-
# ? capability
# ? leadName
# ? tmEmail
# ? cmEmail
# ? desc
# ? status
# ? nextSteps
# ? dateSubmitted

# ? userID
# ? consultant
# ? password
# ? consEmail
# ? tmEmail
# ? cmEmail

# Initialize the Flask App
app = FlaskAPI(__name__)

# Establish connection to client
client = MongoClient('mongodb://localhost:27017/')

# Reference database
DB =client["Leads"]

# Reference companies collection
users_collection = DB.Users
records_collection = DB.Records

#print(users_collection)

# Build an API with endpoints to:
@app.route("/", methods=["GET"])
def home():
        return {
        "routes": {
            "/": "Root, shows list of available routes",
            "/create-user": "make a new user account",
            "/add": "get all",
            "/find": "Find a document"
        }
    }

# Create new _id/consultant/password/consEmail
## No validation
@app.route("/create-user", methods=["POST"])
def create_user():
    q = request.data  
    users_collection.insert_one(q)
    return "Hey, you did it!"

# users can create a new record
# Validation for all fields
# userID; recordID; consultant; consEmail; bizUnit; clientAcct
# capability; leadName; tmEmail; cmEmail; desc; status; nextSteps
# dateSubmitted

def has_all_keys(data):
    expected_keys = ["userID", "recordID", "consultant", "consEmail",
                    "bizUnit", "clientAcct", "capability", "leadName",
                    "tmEmail", "cmEmail", "desc", "status", "nextSteps",
                    "dateSubmitted"]
    actual_keys = data.keys()
    missing_keys = []
    for key in expected_keys:
        if key not in actual_keys:
            missing_keys.append(key)
    if len(missing_keys) == 0:
        return {"True":[]} 
    else:
        return {"False":missing_keys}


@app.route("/create-record", methods=["POST"])
def create_record():
    q = request.data  
    print(has_all_keys(q)) 
    records_collection.insert_one(q)
    return "Hey, cool!"

#users can retrieve records they have submitted
@app.route("/get-records/<string:id>", methods=["GET"])
def get_record(id):
    if id.lower() == "All".lower():
        pass
    else:
        d = {"userID":id}
        results = records_collection.find(d)
        results = dumps(results)
        results = json.loads(results)
        return results
    return "Here's your stuff!"

@app.route("/get-users", methods=["GET"])
def get_users():
    d = {}
    results = users_collection.find(d)
    results = dumps(results)
    results = json.loads(results)
    return results

if __name__ == "__main__":
    app.run(debug=True)