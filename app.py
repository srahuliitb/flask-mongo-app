# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
from flask import Flask, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util, ObjectId
import json
import getpass # Take user input without displaying the characters in the console

app = Flask(__name__)

username = input("Enter your username: ")
password = getpass.getpass("Enter your password: ")

db_name = 'sample_mflix'
mongo_driver_uri = f"mongodb+srv://{username}:{password}@rsmongodbpracticecluste.0nqes.mongodb.net/{db_name}?retryWrites=true&w=majority"

# Create a new client and connect to the server
# client = MongoClient(mongo_driver_uri, server_api=ServerApi('1'))

# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

# Configure Flask app to use MongoDB
app.config['MONGO_URI'] = mongo_driver_uri
mongo = PyMongo(app)

@app.route('/')
def home_page():
   return '\nHello, This is the homepage for the Flask-Mongo app!'

# GET API endpoint to retrieve a record by ID
@app.route('/get_movie/<string:record_id>', methods=['GET'])
def get_one_record(record_id):
    try:
        # Convert the provided ID to ObjectId
        obj_id = ObjectId(record_id)
        # Query the MongoDB collection for the specified ID
        record = mongo.db.movies.find_one({'_id': obj_id})
        if record:
            pretty_json = json_util.dumps(record, indent=2)
            response = Response(pretty_json, content_type='application/json')
            return response, 200
        else:
            return jsonify({'message': 'Record not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_all_movies', methods=['GET'])
def get_all_records():
    try:
        # Access MongoDB collection
        collection = mongo.db.movies
        # Retrieve all documents from the collection
        all_documents = list(collection.find())
        # Use json.dumps for pretty-printing with indent
        pretty_json = json.dumps(all_documents, default=str, indent=2)
        # Create a Flask Response with the content type set to 'application/json'
        response = Response(pretty_json, content_type='application/json')
        return response, 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
