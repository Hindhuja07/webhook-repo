from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import pytz

app = Flask(__name__)
client = MongoClient("mongodb+srv://hindhujaya:UobPado5pRimZomC@cluster0.fp1b47a.mongodb.net/webhookDB?retryWrites=true&w=majority")
db = client["webhookDB"]
events_col = db["events"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    event_type = request.headers.get('X-GitHub-Event')
    payload = request.json
    now_utc = datetime.utcnow().replace(tzinfo=pytz.UTC).isoformat()

    data = {"timestamp": now_utc, "action": event_type}

    if event_type == "push":
        data.update({
            "author": payload["pusher"]["name"],
            "to_branch": payload["ref"].split('/')[-1]
        })
    elif event_type == "pull_request":
        pr = payload["pull_request"]
        data.update({
            "author": pr["user"]["login"],
            "from_branch": pr["head"]["ref"],
            "to_branch": pr["base"]["ref"]
        })

    events_col.insert_one(data)
    return jsonify({"message": "Event recorded"}), 200

@app.route('/get_events')
def get_events():
    events = list(events_col.find().sort("timestamp", -1).limit(10))
    for e in events:
        e["_id"] = str(e["_id"])
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True)
