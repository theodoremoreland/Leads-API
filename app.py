# Native
import json

# App
from flask import request
from flask_cors import CORS
from flask_api import FlaskAPI, status
from pymongo import MongoClient

# Formatting
from pprint import pprint
from bson.json_util import dumps

# Custom
from validation import has_all_keys, has_valid_emails, has_valid_date, has_valid_ids
from sendEmail import sendEmail

# @param userID
# @param salesForceId
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
# @param clientContact
# @param clientDept
# @param oppOwner

# @param userID
# @param consultant
# @param password
# @param consEmail
# @param tmEmail
# @param cmEmail

# Initialize the Flask App
app = FlaskAPI(__name__)
CORS(app)

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
            "/get-records/{salesForceId}": "Return a specific lead document by salesForceId",
            "/get-users": "Return a list of all user documents",
            "/update-records": "Updates one or more lead documents",
            "/get-highest-id/<string:collection>/<string:field>" : "Get highest id"
        }
    }

# ! Data passed through this function is not validated before sending to database.
@app.route("/create-user", methods=["POST"])
def create_user():
    q = request.data  
    users_collection.insert_one(q)
    return f'{status.HTTP_201_CREATED} : Content created.'

# ? Users can create a new record.
@app.route("/create-record", methods=["POST"])
def create_record():
    q = request.data
     
    print(f'Keys: {has_all_keys(q)}')
    print(f'E-mails: {has_valid_emails(q)}')
    print(f'Date: {has_valid_date(q)}')
    print(f'userId: {has_valid_ids(q)}')

    if has_all_keys(q)["Valid"]:
        pass
    else:
        return f'{status.HTTP_406_NOT_ACCEPTABLE} : Missing Keys {has_all_keys(q)["Data"]}'

    if has_valid_emails(q):
        pass
    else:
        return f'{status.HTTP_406_NOT_ACCEPTABLE} : Invalid Email Format'
    
    if has_valid_date(q):
        pass
    else:
        return f'{status.HTTP_406_NOT_ACCEPTABLE} : Invalid Date Format'
    
    if has_valid_ids(q):
        pass
    else:
        return f'{status.HTTP_406_NOT_ACCEPTABLE} : User ID should be int'
    records_collection.insert_one(q)
    sendEmail(q)

    return f'{status.HTTP_201_CREATED} : Content created.'
    
# ? Users can retrieve records they have submitted.
@app.route("/get-records/<string:id>", methods=["GET"])
def get_record(id):

    # ? The below variable assignment represents either a "find all" query...
    # ? or a "find by id" query.
    d = {} if id.lower() == "all" else {"userId": int(id)}

    results = records_collection.find(d)

    # Converts results to string.
    results = dumps(results)

    # Converts results to json / dictionary
    results = json.loads(results)

    return results

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

# ? Returns the highest userID or salesForceId.
@app.route("/get-highest-id/<string:collection>/<string:field>", methods=["GET"])
def get_highest_id(collection, field):
    
    if collection.lower() == "users":
        results = users_collection.find().sort(field, -1).limit(1)
    else:
        results = records_collection.find().sort(field, -1).limit(1)

    # Converts results to string.
    results = dumps(results)

    # Converts results to json / dictionary
    results = json.loads(results)

    return results

# ? Accepts a list of json leads/records and updates them in database.
# ? Can update all records or just one, but data must be passed in as an array / list
@app.route("/update-records", methods=["POST"])
def update_records():

    json_array = request.data

    if not isinstance(json_array, list):
        return f'{status.HTTP_406_NOT_ACCEPTABLE} : json objects much be in an array.'

    for document in json_array:

        # Specifies only records of the chosen ID.
        _filter = { "salesForceId": document["salesForceId"] }

        # Specifies key(s) : value(s) to be updated.
        update = { "$set": document }

        records_collection.update_one(_filter, update)
    return f'{status.HTTP_202_ACCEPTED} : Updates accepted.'



if __name__ == "__main__":
    app.run(debug=True)