''' This program is the bot to forward message to MS Teams channel.
FLEX.team service is not supported by the python library, so we need to
make a bot to forward Slack message to MS Teams channel.
'''
import os
from slack_bolt import App
from pathlib import Path
from dotenv import load_dotenv
from pymsteams import connectorcard
import emoji_data_python

# function to convert colon emoji to unicode
def convert_emoji(emoji):
    return emoji_data_python.replace_colons(emoji)

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

port = int(os.environ.get('FLEXBOT_PORT', 5080))
token = os.environ.get('SLACK_BOT_TOKEN')
signing_secret = os.environ.get('SLACK_SIGNING_SECRET')
app = App(token=token, signing_secret=signing_secret)

@app.message("hello")
def say_hello(message, say):
    user = message['user']
    say(f"Hi there, <@{user}>!")
    print(message)

@app.message("휴가")
def say_vacation(message, say):
    text = convert_emoji(message['text'])
    teamsMessage.text(text)
    teamsMessage.send()
    print(message)

@app.message("Calendar")
def say_calendar(message, say):
    print("Calendar")
    print(message)
    text = convert_emoji(message['text'])
    teamsMessage.text(text)
    teamsMessage.send()
    print(message)


@app.event("message")
def message_event_handler(event, say):
    print("message_event_handler")
    attachment = event['attachments'][0]
    # text = convert_emoji(attachment['text'])
    pretext = convert_emoji(attachment['pretext'])
    title = convert_emoji(attachment['title'])
    #fallback = convert_emoji(attachment['fallback'])
    teamsMessage.text(pretext)
    # markdown to plain text
    teamsMessage.title(title)
    teamsMessage.send()
    print(event)

if __name__ == "__main__":
    print("FLEX Bot has started!")
    # teams webhook
    teamsMessage = connectorcard(os.environ['TEAMS_WEBHOOK_URL'])

    app.start(port=port)
    
