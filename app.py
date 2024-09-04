from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from dateutil.parser import parse
from dateutil.tz import UTC
from datetime import datetime, timedelta

app = Flask(__name__)

# MongoDB Connection URI
MONGO_URI = "mongodb+srv://visheshyadav2001:9ONswN3l9tDjw2ez@chat00.xwawjcr.mongodb.net/chat-app-db?"
DB_NAME = 'action'

# MongoDB Client
client = MongoClient(MONGO_URI)
db = client.get_database(DB_NAME)
events_collection = db.events

# Enumeration of GitHub events
enum_github_event = ["PUSH", "PULL_REQUEST", "MERGE"]

# Helper function to parse timestamp and adjust to IST
def convert_to_ist(timestamp):
    ts = parse(str(timestamp)).astimezone(UTC)
    return ts + timedelta(hours=5, minutes=30)

# Helper function to format date with suffix
def suffix(d):
    return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

# Route to display the data
@app.route('/')
def index():
    events = list(events_collection.find().sort([("timestamp", -1)]))  # Sort by latest first
    events.append({'datet': datetime.now()})  # Placeholder for current time
    return render_template('index.html', datalist=events)

# Webhook route to process GitHub events
@app.route('/action', methods=['POST'])
def new_change():
    data = request.json
    new_event = {}

    if 'pull_request' in data:

        ts = convert_to_ist(data['pull_request']['created_at'])
        if data['action'] == 'opened':  # Process opened pull requests
            new_event = {
                "request_id": data["pull_request"]["id"],
                "author": data["pull_request"]["user"]["login"],
                "action": enum_github_event[1],
                "from_branch": data["pull_request"]["head"]["ref"],
                "to_branch": data["pull_request"]["base"]["ref"],
                "timestamp": ts.strftime('%I:%M %p %d %B, %Y')
            }
        elif data['action'] == 'closed' and data['pull_request']['merged']:
            new_event = {
                "request_id": data["pull_request"]["merge_commit_sha"],
                "author": data["pull_request"]["merged_by"]["login"],
                "action": enum_github_event[2],
                "from_branch": data["pull_request"]["head"]["ref"],
                "to_branch": data["pull_request"]["base"]["ref"],
                "timestamp": ts.strftime('%I:%M %p %d %B, %Y')
            }

    if 'pusher' in data:
        ts = convert_to_ist(data['head_commit']['timestamp'])
        new_event = {
            "request_id": data["after"],
            "author": data["head_commit"]["author"]["name"],
            "action": enum_github_event[0],
            "from_branch": data["repository"]["default_branch"],
            "to_branch": data["repository"]["default_branch"],
            "timestamp": ts.strftime('%I:%M %p %d %B, %Y')
        }

    # Insert new event if valid
    if new_event:
        events_collection.insert_one(new_event)

    return jsonify({"status": "success"}), 201

if __name__ == '__main__':
    app.run(debug=True)
