# Flask-MongoDB Web App

This web application serves as a simple interface to interact with a MongoDB database. It employs Flask for web routing and MongoDB for data storage and retrieval.

### Motivation:
Managing a large data efficiently through a user-friendly interface is highly desirable which this application attempts to deliver by interacting with a MongoDB database. Whether you need to fetch a specific movie record or retrieve the entire collection, this Flask-MongoDB app has got you covered.

### Features:
1. Secure Authentication:
    - Utilizes getpass to securely take the MongoDB password as user input without displaying characters in the console.
2. MongoDB Connection:
    - Establishes a connection to MongoDB Atlas using the official pymongo driver.
    - Configures the Flask app to use MongoDB with Flask-PyMongo.
3. Endpoints:
    - ```/```: Displays a welcoming homepage message for the Flask-Mongo app.
    - ```/get_movie/<string:record_id>```: Retrieves a movie record by its unique ID and returns it in a well-formatted JSON response.
    - ```/get_all_movies```: Retrieves all movie records from the MongoDB collection and presents them in a readable JSON format.

### Usage:
- Clone the repository.
- Install the required dependencies using pip install -r requirements.txt.
- Run the application with python app.py.
