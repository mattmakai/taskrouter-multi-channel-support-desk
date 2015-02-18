# Multi Channel Call Center with Twilio TaskRouter
A call center that supports both inbound voice calls and SMS messages through
Twilio's TaskRouter API.


## Deploy to Heroku
Press the big ol' purple button below. Input your credentials into the Heroku
set up page and click deploy.

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/makaimc/taskrouter-multi-channel-support-desk)


## Environment variables
Ensure you've set the following environment variables locally or via the
Heroku deploy button:

* ``TWILIO_ACCOUNT_SID``: Account SID found on 
  [Twilio dashboard](https://www.twilio.com/user/account/voice-messaging) 
  under API credentials

* ``TWILIO_AUTH_TOKEN``: Secret authentication token also found on 
  [Twilio dashboard](https://www.twilio.com/user/account/voice-messaging) 
  under API credentials

* ``WORKSPACE_SID``: Found on the 
  [TaskRouter workspaces dashboard](https://www.twilio.com/user/account/taskrouter/workspaces)
  after [creating a workspace](https://www.twilio.com/user/account/taskrouter/workspaces/create)

* ``WORKFLOW_SID``: Found on the TaskRouter workflow page for a given 
  workspace

* ``SUPPORT_DESK_NUMBER``: Twilio phone number used for the support desk,
  in the +12025551234 format
