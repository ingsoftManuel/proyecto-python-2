from firebase_database import FirebaseDB
from flask import Flask, request, jsonify
from datetime import datetime
from firebase_admin.exceptions import FirebaseError
from flask_cors import CORS

path = 'project_credentials.json'
url ="https://proyecto-python-2b9ef-default-rtdb.firebaseio.com/"

fb_db = FirebaseDB(path,url)

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Route to save sensor data (POST)
@app.route('/api/sensor_data', methods=['POST'])
def save_sensor_data():
    """
    Handles POST requests to save sensor data.
    Validates the incoming request body, generates timestamp, and stores the data in Firebase.

    Returns:
    - JSON response with a success message and saved data, or an error message.
    """
    try:
        # Extract data from the request body
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is missing"}), 400

        idsensor = data.get('idsensor')
        valor = data.get('valor')

        # Validate required fields
        if not idsensor or valor is None:
            return jsonify({"error": "idsensor and valor are required"}), 400

        # Generate timestamp for the record
        timestamp = datetime.now()
        record = {
            "fecha": timestamp.strftime("%Y-%m-%d"),  # Date in YYYY-MM-DD format
            "hora": timestamp.strftime("%H:%M:%S"),  # Time in HH:MM:SS format
            "idsensor": idsensor,
            "valor": valor
        }

        # Save the record to Firebase (auto-generating an ID)
        fb_db.write_record('sensor_data', record)

        return jsonify({"message": "Sensor data saved successfully", "data": record}), 201
    except FirebaseError as e:
        return jsonify({"error": f"Firebase error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

# Route to retrieve all sensor data (GET)
@app.route('/api/sensor_data', methods=['GET'])
def get_sensor_data():
    """
    Handles GET requests to retrieve all sensor data from Firebase.

    Returns:
    - JSON response containing a list of sensor data or an empty list if no data exists.
    """
    try:
        # Read all data from Firebase
        data = fb_db.read_record('sensor_data')

        # Return an empty list if no data exists
        if not data:
            return jsonify({"message": "No sensor data found", "data": []}), 200

        # Convert data into a list for easier handling
        sensor_data_list = [{"id": key, **value} for key, value in data.items()]
        return jsonify({"data": sensor_data_list}), 200
    except FirebaseError as e:
        return jsonify({"error": f"Firebase error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

# Run the Flask app
if __name__ == "__main__":
    """
    Main entry point for the Flask app.
    The app will run in debug mode on localhost and port 5000.
    """
    app.run(debug=True, host='0.0.0.0', port=5000)
