import os
from flask import Flask, Response
from twilio import twiml


ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
SUPPORT_AGENT_NUMBER = os.environ.get('SUPPORT_AGENT_NUMBER', '')

app = Flask(__name__)


@app.route('/')
def working():
    return "Service desk up and running!"


@app.route('/call', methods=['GET', 'POST'])
def call():
    r = twiml.Response()
    r.dial(SUPPORT_AGENT_NUMBER)
    return Response(str(r), content_type='application/xml')


if __name__ == '__main__':
    # first attempt to get the PORT environment variable because it will be 
    # exposed if we're deploying on Heroku, otherwise default to port 5000
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
