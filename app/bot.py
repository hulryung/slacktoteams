''' This program is the bot to forward message to MS Teams channel.
FLEX.team service is not supported by the python library, so we need to
make a bot to forward Slack message to MS Teams channel.
'''
import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from pymsteams import connectorcard
import emoji_data_python

# function to convert colon emoji to unicode
def convert_emoji(emoji):
    return emoji_data_python.replace_colons(emoji)

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

port = int(os.environ.get('FLEXBOT_PORT', 5080))
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)
client = slack.web.client.WebClient(token=os.environ['SLACK_TOKEN'])

client.chat_postMessage(channel='#'+os.environ['SLACK_CHANNEL'], text="FLEX Bot has started!")
BOT_ID = client.api_call("auth.test")['user_id']

# teams webhook
teamsMessage = connectorcard(os.environ['TEAMS_WEBHOOK_URL'])

# slack event
@slack_event_adapter.on('message')
def message(payload):
    print(payload)
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    if BOT_ID != user_id:
        if '휴가' in text:
            # convert colon emoji to unicode
            text = convert_emoji(text)
            teamsMessage.text(text)
            # send message to teams channel
            teamsMessage.send()
        else:
            print(text)

if __name__ == "__main__":
    app.run(debug=True, port=port)