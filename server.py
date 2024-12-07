from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Path to the JSON file
FILE_PATH = "users.json"

@app.route('/save', methods=['POST'])
def save_user():
    new_user = request.json

    # Check if file exists
    if not os.path.exists(FILE_PATH):
        # Create file and save the first user
        with open(FILE_PATH, 'w') as f:
            json.dump([new_user], f, indent=4)
        return jsonify({"message": "File created and user added!"})

    # Append user to the existing file
    try:
        with open(FILE_PATH, 'r') as f:
            users = json.load(f)

        users.append(new_user)

        with open(FILE_PATH, 'w') as f:
            json.dump(users, f, indent=4)

        return jsonify({"message": "User data appended successfully!"})
    except Exception as e:
        return jsonify({"message": f"Error processing the file: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
