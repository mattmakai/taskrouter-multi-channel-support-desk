import json
import os
from flask import Flask, Response, request
from twilio import twiml
from twilio.rest import TwilioRestClient, TwilioTaskRouterClient


ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
SUPPORT_DESK_NUMBER = os.environ.get('SUPPORT_DESK_NUMBER', '')
WORKSPACE_SID = os.environ.get('WORKSPACE_SID', '')
WORKFLOW_SID = os.environ.get('WORKFLOW_SID', '')

client = TwilioRestClient(account=ACCOUNT_SID, token=AUTH_TOKEN)
tr_client = TwilioTaskRouterClient(account=ACCOUNT_SID, token=AUTH_TOKEN,
                                   base='https://wds.twilio.com')
app = Flask(__name__)


@app.route('/')
def working():
    return "Support desk up and running!"


@app.route('/call', methods=['GET', 'POST'])
def call():
    r = twiml.Response()
    r.enqueue('', workflowSid=WORKFLOW_SID)
    return Response(str(r), content_type='application/xml')


@app.route('/assign', methods=['POST'])
def assign():
    task_attrs = json.loads(request.form['TaskAttributes'])
    if 'task_type' in task_attrs and task_attrs['task_type'] == 'sms':
        number = json.loads(request.form['WorkerAttributes'])['phone_number']
        instruction = {"instruction": "accept"}
        client.messages.create(from_=SUPPORT_DESK_NUMBER, to=number,
            body='Text {0} asking "{1}"'.format(task_attrs['phone_number'],
                                                task_attrs['body']))
        return Response(json.dumps(instruction),
                        content_type='application/json')
    # defaults to voice call
    number = json.loads(request.form['WorkerAttributes'])['phone_number']
    instruction = {
        "instruction": "dequeue",
        "to": number,
        "from": SUPPORT_DESK_NUMBER
    }
    return Response(json.dumps(instruction),
                    content_type='application/json')


@app.route('/message', methods=['POST'])
def message():
    # check if one of our workers is completing a task
    if request.form['Body'] == 'DONE':
        from_number = request.form['From']
        for w in tr_client.workers(WORKSPACE_SID).list():
            if from_number == json.loads(w.attributes)['phone_number']:
                r = twiml.Response()
                r.message("Ticket closed.")
                return Response(str(r), content_type='application/xml')
    task_attributes = {
        "task_type" : "sms",
        "phone_number" : request.form['From'],
        "body": request.form['Body']
    }
    tasks = tr_client.tasks(WORKSPACE_SID).create(json.dumps(task_attributes),
                                                  WORKFLOW_SID)
    r = twiml.Response()
    r.message("Thanks. You'll hear back from us soon.")
    return Response(str(r), content_type='application/xml')


if __name__ == '__main__':
    # first attempt to get the PORT environment variable because it will be 
    # exposed if we're deploying on Heroku, otherwise default to port 5000
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)

