from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

# Load existing data from the file
try:
    with open('data.json', 'r') as file:
        stored_data_dict = json.load(file)
except FileNotFoundError:
    # If the file doesn't exist yet, initialize an empty dictionary
    stored_data_dict = {}

@app.route('/', methods=['GET'])
def index():
    return render_template('admin/adminPage.html')# Assuming your HTML file is named user.html

#Admin form for user
@app.route('/admin/cameraOwner', methods=['GET','POST'])
def admin_cameraOwner():
    return render_template('admin/user.html') 

#Admin Login page for police
@app.route('/admin/police')
def admin_police():
    return render_template('admin/policeAdmin.html')


#police 
@app.route('/police/home')
def police_home():
    return render_template('/police/noti.html') 


@app.route('/your-server-endpoint', methods=['POST'])
def receive_data():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Generate a unique key (you may use a more robust method in production)
        key = len(stored_data_dict) + 1

        # Store the data in the dictionary with the generated key
        stored_data_dict[key] = data

        # Save the updated data to the file
        with open('data.json', 'w') as file:
            json.dump(stored_data_dict, file)

        # Print the received data to the console
        print('Received data:', data)

        # Send a response back to the client
        response = {'message': 'Data received and stored successfully', 'key': key}
        return jsonify(response), 200

    except Exception as e:
        # Handle any exceptions that may occur
        print('Error:', str(e))
        response = {'error': 'Failed to process the data'}
        return jsonify(response), 500

@app.route('/get-stored-data')
def get_stored_data():
    # Return the stored data as JSON
    return jsonify(stored_data_dict)

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Set the port to 5000 or another available port

# from flask import Flask, request, jsonify, render_template
# import json

# app = Flask(__name__)

# # Load existing data from the file
# try:
#     with open('data.json', 'r') as file:
#         stored_data_dict = json.load(file)
# except FileNotFoundError:
#     # If the file doesn't exist yet, initialize an empty dictionary
#     stored_data_dict = {}

# @app.route('/')
# def index():
#     return render_template('user.html')  # Assuming your HTML file is named user.html

# @app.route('/your-server-endpoint', methods=['POST'])
# def receive_data():
#     try:
#         # Get JSON data from the request
#         data = request.get_json()

#         # Generate a unique key (you may use a more robust method in production)
#         key = len(stored_data_dict) + 1

#         # Store the data in the dictionary with the generated key
#         stored_data_dict[key] = data

#         # Save the updated data to the file
#         with open('data.json', 'w') as file:
#             json.dump(stored_data_dict, file)

#         # Print the received data to the console
#         print('Received data:', data)

#         # Send a response back to the client
#         response = {'message': 'Data received and stored successfully', 'key': key}
#         return jsonify(response), 200

#     except Exception as e:
#         # Handle any exceptions that may occur
#         print('Error:', str(e))
#         response = {'error': 'Failed to process the data'}
#         return jsonify(response), 500

# @app.route('/get-stored-data')
# def get_stored_data():
#     # Return the stored data as JSON
#     return jsonify(stored_data_dict)

# if __name__ == '_main_':
#     app.run(debug=True, port=5000)  # Set the port to 5000 or another available port