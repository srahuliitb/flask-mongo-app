# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
from flask import Flask, request, make_response, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util, ObjectId
import json
from db_connection import mongo_driver_uri
from functools import wraps
from file_reader import get_all_user_credentials_from_persistent_storage
from jwt_authentication import jwt_encode, jwt_decode
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = '1111-2222-3333-4444'
# Configure Flask app to use MongoDB
app.config['MONGO_URI'] = mongo_driver_uri
mongo = PyMongo(app)

# Create a decorator to perform HTTP Authentication for a given endpoint
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth:
            user_credentials = get_all_user_credentials_from_persistent_storage()
            for i in range(len(user_credentials)):
                if auth.username == user_credentials[i][0] and auth.password == user_credentials[i][1]:
                    return f(*args, **kwargs)
                
        return make_response('Invalid credentials provided. Could not verify your login!', 
                             401, 
                             {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return decorated

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token not provided'}), 401
        try:
            decoded_token = jwt_decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Invalid token provided'}), 403
        return f(*args, **kwargs)
    
    return decorated

@app.route('/')
def index():
   return '<h1>Welcome! This is a homepage for the REST APIs to retrieve MFlix movies data.<h1>'

@app.route('/login')
@auth_required
def login():
    auth = request.authorization
    encoded_token = jwt_encode({'user': auth.username, 
                                        'exp': datetime.utcnow() + timedelta(hours=24)}, 
                                       app.config['SECRET_KEY'])
    
    return jsonify({'message': 'Login successful', 'token': encoded_token})
    # return '<h1>Login successful!<h1>'

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'token accepted'})

# GET API endpoint to retrieve a record by ID
@app.route('/get_movie/<string:record_id>', methods=['GET'])
@auth_required
@token_required
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
@auth_required
@token_required
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
