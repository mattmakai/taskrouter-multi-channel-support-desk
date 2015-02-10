import os
from flask import Flask
from twilio import twiml
from twilio.rest import TwilioTaskRouterClient


app = Flask(__name__)


@app.route('/')
def working():
    return "Web application up and running!"


if __name__ == '__main__':
    # first attempt to get the PORT environment variable because it will be 
    # exposed if we're deploying on Heroku, otherwise default to port 5000
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
