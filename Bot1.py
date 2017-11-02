import os
  2. from slackclient import SlackClient
  3. from dotenv import load_dotenv
  4. 
  5. load_dotenv('.env')
  6. 
  7. slack_token = os.environ["SLACK_API_TOKEN"]
  8. sc = SlackClient(slack_token)
  9. 
 10. sc.api_call(
 11.   "chat.postMessage",
 12.   channel="#general"


export SLACK_API_TOKEN=Bot1
python bot.py