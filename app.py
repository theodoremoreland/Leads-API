# Native
import json

# App
from flask import request
from flask_api import FlaskAPI
from pymongo import MongoClient

# Formatting
from pprint import pprint
from bson.json_util import dumps

# Custom
from validation import has_all_keys, has_correct_datatypes, has_valid_emails
 
# Able to store a list of json for all leads and update status (from salesforce)
# Update lead records via application

# @param userID
# @param recordID
# @param consultant
# @param consEmail
# @param bizUnit
# @param clientAcct
# @param capability
# @param leadName
# @param tmEmail
# @param cmEmail
# @param desc
# @param status
# @param nextSteps
# @param dateSubmitted

# @param userID
# @param consultant
# @param password
# @param consEmail
# @param tmEmail
# @param cmEmail

# Initialize the Flask App
app = FlaskAPI(__name__)

# Establish connection to client
client = MongoClient('mongodb://localhost:27017/')

# Reference database
DB = client["Leads"]

# Reference each collection
users_collection = DB.Users
records_collection = DB.Records

# ? Renders index page with list of all endpoints.
@app.route("/", methods=["GET"])
def home():
        return {
        "routes": {
            "/": """Root, shows list of available routes.
             All GET requests return json object(s) and all POST requests accept json object(s)""",
            "/create-user": "Add a new user to the database",
            "/create-record": "Add a new lead to the database",
            "/get-records/{id}": "Return a specific lead document by userID",
            "/get-users": "Return a list of all user documents"
        }
    }

# ? Create new _id/consultant/password/consEmail
# ! Data passed through this function is not validated before sending to database.
@app.route("/create-user", methods=["POST"])
def create_user():
    q = request.data  
    users_collection.insert_one(q)
    return "Hey, you did it!"

# ? Users can create a new record.
@app.route("/create-record", methods=["POST"])
def create_record():
    q = request.data  
    print(has_all_keys(q))
    print(has_correct_datatypes(q))
    print(has_valid_emails(q)) 
    records_collection.insert_one(q)
    return "Hey, cool!"

# ? Users can retrieve records they have submitted.
@app.route("/get-records/<string:id>", methods=["GET"])
def get_record(id):
    if id.lower() == "All".lower():
        pass
    else:
        d = {"userID": id}
        results = records_collection.find(d)

        # Converts results to string.
        results = dumps(results)

        # Converts results to json / dictionary
        results = json.loads(results)

        return results
    return "Here's your stuff!"

# ? Returns all user records in json format
@app.route("/get-users", methods=["GET"])
def get_users():
    d = {}
    results = users_collection.find(d)

    # Converts results to string.
    results = dumps(results)

    # Converts results to json / dictionary
    results = json.loads(results)

    return results

# ? Accepts a list of json leads/records and updates them in database
@app.route("/update-records", methods=["POST"])
def update_records():
    q = request.data
    for document in q:

        # Specifies only records of the chosen ID.
        _filter = { "recordID": document["recordID"] }

        # Specifies key(s) : value(s) to be updated.
        update = { "$set": document }

        records_collection.update_one(_filter, update)
    return "Hi"

if __name__ == "__main__":
    app.run(debug=True)