import os
from dotenv import load_dotenv
from flask import Flask, request

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# In-memory databases
users = {}
candidates = {}
votes = {}

@app.route('/')
def index():
    return "Welcome to the College Voting System API!"

@app.route('/ussd', methods=['POST'])
def ussd():
    session_id = request.form['sessionId']
    service_code = request.form['serviceCode']
    phone_number = request.form['phoneNumber']
    text = request.form['text']

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
        users[phone_number] = name  # Register user
        response = "END Registration successful for " + name
    elif text == "2":
        response = "CON Enter candidate name to register:"
    elif text.startswith("2*"):
        candidate_name = text.split('*')[1]
        candidates[candidate_name] = 0  # Register candidate with 0 votes
        response = "END Candidate " + candidate_name + " registered successfully."
    elif text == "3":
        response = "CON Enter candidate name to vote for:"
    elif text.startswith("3*"):
        candidate_name = text.split('*')[1]
        if candidate_name in candidates:
            votes[phone_number] = candidate_name  # Record vote
            candidates[candidate_name] += 1  # Increment vote count
            response = "END Thank you for voting for " + candidate_name
        else:
            response = "END Candidate not found."
    elif text == "4":
        results = "\n".join([f"{name}: {count} votes" for name, count in candidates.items()])
        response = "END Voting Results:\n" + results if results else "END No votes cast yet."

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
