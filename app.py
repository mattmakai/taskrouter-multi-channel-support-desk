import os
from flask import Flask, Response
from twilio import twiml
from twilio.rest import TwilioTaskRouterClient


ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
WORKSPACE_SID = os.environ.get('WORKSPACE_SID', '')

app = Flask(__name__)

tr_client = TwilioTaskRouterClient(base='https://wds.twilio.com',
                                   account=ACCOUNT_SID, token=AUTH_TOKEN)

@app.route('/')
def working():
    return "Service desk up and running!"


@app.route('/call', methods=['GET', 'POST'])
def call():
    r = twiml.Response()
    r.enqueue('', workflowSid=WORKSPACE_SID)
    return Response(str(r), content_type='application/xml')


if __name__ == '__main__':
    # first attempt to get the PORT environment variable because it will be 
    # exposed if we're deploying on Heroku, otherwise default to port 5000
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
