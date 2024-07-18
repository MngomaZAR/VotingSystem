from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Your in-memory databases
users = {}
candidates = {}
votes = {}

@app.route('/')
def index():
    return "Welcome to the College Voting System API!"

@app.route('/ussd', methods=['POST'])
def ussd():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")

    if text == "":
        response = "CON Welcome to College Voting System\n"
        response += "1. Register to vote\n"
        response += "2. Register a candidate\n"
        response += "3. Vote\n"
        response += "4. View results"
    elif text == "1":
        response = "CON Enter your name to register:"
    elif text.startswith("1*"):
        name = text.split('*')[1]
        if name.strip():
            users[phone_number] = name  # Register user
            response = f"END Registration successful for {name}."
        else:
            response = "END Name cannot be empty."
    elif text == "2":
        response = "CON Enter candidate name to register:"
    elif text.startswith("2*"):
        candidate_name = text.split('*')[1]
        if candidate_name.strip():
            if candidate_name not in candidates:
                candidates[candidate_name] = 0  # Register candidate with 0 votes
                response = f"END Candidate {candidate_name} registered successfully."
            else:
                response = "END Candidate already registered."
        else:
            response = "END Candidate name cannot be empty."
    elif text == "3":
        response = "CON Enter candidate name to vote for:"
    elif text.startswith("3*"):
        candidate_name = text.split('*')[1]
        if candidate_name in candidates:
            if phone_number in votes:
                response = "END You have already voted."
            else:
                votes[phone_number] = candidate_name  # Record vote
                candidates[candidate_name] += 1  # Increment vote count
                response = f"END Thank you for voting for {candidate_name}."
        else:
            response = "END Candidate not found."
    elif text == "4":
        if candidates:
            results = "\n".join([f"{name}: {count} votes" for name, count in candidates.items()])
            response = "END Voting Results:\n" + results
        else:
            response = "END No candidates registered yet."
    else:
        response = "END Invalid option."

    return response

@app.route('/callback', methods=['POST'])
def callback():
    data = request.json
    # Process the data here
    # For example, you can log the data or handle different status codes
    message_id = data['entry']['messageId']
    status = data['entry']['status']
    status_code = data['entry']['statusCode']
    
    # Log or handle the message status update
    print(f"Message ID: {message_id}, Status: {status}, Status Code: {status_code}")
    
    return jsonify(success=True), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
