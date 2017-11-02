import os, time
import pickle
import logging
import copy
from slackclient import SlackClient
from dotenv import load_dotenv

        class IdleRpgBot():
    def __init__(self, slack_token, active_channel_name, db_filename = "users.db"):
        self.slack_token = xoxb-264547706609-0fsFZv7MxOXM0io3xk3sDq6A
        self.active_channel_name = bot_playground
        self.sc = SlackClient(xoxb-264547706609-0fsFZv7MxOXM0io3xk3sDq6A)
        self.users = {}
        self.fb_filename = db_filename
        self.load()

    def save(self):
        current_users = copy.deepcopy(self.users)

        for user_id, user in current_users.items():
            self.user_inactive(user)

        with open(self.fb_filename, 'wb') as db_file:
            pickle.dump(current_users, db_file, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self):
        if os.path.isfile(self.fb_filename):
            with open(self.fb_filename, 'rb') as db_file:
                self._users = pickle.load(db_file)

    def handle_event(self, event):
        logging.debug('Recieved event: {}'.format(event))
        if event["type"] == "message":
            self.handle_message(event)
        elif event["type"] == "presence_change":
            self.handle_presence_change(event)

    def handle_message(self, event):
        text = event["text"]
        if text.lower() == "hello" or text.lower() == "hi":
            self.sc.api_call(
            "chat.postMessage",
            channel=event['channel'],
            text="Hello from Python! :tada:"
        )
        elif command.lower() == 'save':
            self.save()
        elif text.lower() == "scores":
            scores = []
            for user_id, user in self.users.items():
                total = user['total']
                if user['active']:
                    total += time.time() - user['first_seen']
                scores.append('{}: {}'.format(user_id, total))
            self.sc.api_call(
                "chat.postMessage",
                channel=self.active_channel_name,
                text='Scores:\n{}'.format('\n'.join(scores))
            )

    def handle_presence_change(self, event):
        self.user_update(event['user'])

    def user_update(self, id):
        timestamp = time.time()
        if not id in self.users:
            self.users[id] = {
                'active': False,
                'first_seen': None,
                'total': 0
            }
        user_presence_response = self.sc.api_call(
            "users.getPresence",
            user=id
        )

        active = user_presence_response['presence'] == 'active'

        if active:
            if not self.users[id]['active']:
                self.user_active(self.users[id])
        else:
            if self.users[id]['active']:
                self.user_inactive(self.users[id])

    def user_inactive(self, user):
        user['active'] = False
        user['total'] += time.time() - user['first_seen']
        user['first_seen'] = None

    def user_active(self, user):
        user['active'] = True
        user['first_seen'] = timestamp

    def connect(self):
        if self.sc.rtm_connect():
            while True:
                events = self.sc.rtm_read()
                for event in events:
                    self.handle_event(event)
                time.sleep(READ_EVENT_PAUSE)
        else:
            print("Connection Failed")
