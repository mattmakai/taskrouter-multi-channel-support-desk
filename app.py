import json
import os
from flask import Flask, Response, request
from twilio import twiml


ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
SUPPORT_DESK_NUMBER = os.environ.get('SUPPORT_DESK_NUMBER', '')
WORKFLOW_SID = os.environ.get('WORKFLOW_SID', '')

app = Flask(__name__)


@app.route('/')
def working():
    return "Support desk up and running!"


@app.route('/call', methods=['GET', 'POST'])
def call():
    r = twiml.Response()
    r.enqueue('', workflowSid=WORKFLOW_SID)
    return Response(str(r), content_type='application/xml')


@app.route('/call-assign', methods=['POST'])
def call_assign():
    number = json.loads(request.form['WorkerAttributes'])['phone_number']
    instruction = {
        "instruction": "dequeue",
        "to": number,
        "from": SUPPORT_DESK_NUMBER
    }
    return Response(json.dumps(instruction), content_type='application/json')



if __name__ == '__main__':
    # first attempt to get the PORT environment variable because it will be 
    # exposed if we're deploying on Heroku, otherwise default to port 5000
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)

