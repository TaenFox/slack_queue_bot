import json, requests
from flask import Flask, request, jsonify
import myconf

SLACK_TOKEN = myconf.SLACK_TOKEN 
#просто токен бота, можно заменить строкой со своим токеном

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle_slack_request():
    command = request.form.get("command")
    if command == "/queue":
        process_queue(request.form.get("channel_id"),request.form.get("text"))
        return "Command done."
    return "Invalid command."

@app.route("/slack/actions", methods=["POST"])
def handle_slack_actions():
    payload = request.form.get("payload")
    payload = json.loads(payload)

    # Check the type of action
    if payload["type"] == "block_actions":
        # Get the action and values from the payload
        action = payload["actions"][0]
        action_id = action["action_id"]
        action_type = action["type"]
        queue = create_queue(payload["message"]["ts"])

        # Do something based on the action type and value
        if action_type == "button":
            if action_id == "next-order":
                queue.next()
                send_message_with_blocks(payload["container"]["channel_id"],queue.mes_payload)
                delete_message(payload["container"]["channel_id"], payload["container"]["message_ts"])


            elif action_id == "enter-order":
                queue.add(User(payload["user"]["id"],payload["user"]["username"]))
                send_message_with_blocks(payload["container"]["channel_id"],queue.mes_payload)
                delete_message(payload["container"]["channel_id"], payload["container"]["message_ts"])

            elif action_id == "exit-order":
                queue.delete(User(payload["user"]["id"],payload["user"]["username"]))
                send_message_with_blocks(payload["container"]["channel_id"],queue.mes_payload)
                delete_message(payload["container"]["channel_id"], payload["container"]["message_ts"])

        elif action_type == "static_select":
            uid = action["selected_option"]["value"]
            uname = action["selected_option"]["text"]["text"]
            queue.cur(User(uid, uname))
            send_message_with_blocks(payload["container"]["channel_id"],queue.mes_payload)
            delete_message(payload["container"]["channel_id"], payload["container"]["message_ts"])

def process_queue(channel_id, title):
    queue = Queue(title)
    send_message_with_blocks(channel_id,queue.mes_payload())

def get_message_by_ts(channel, ts):
    headers = {
        'Authorization': 'Bearer ' + SLACK_TOKEN,
        'Content-Type': 'application/json;charset=utf-8'
    }
    url = "https://slack.com/api/conversations.history?channel={}&oldest={}&inclusive=true&limit=1".format(channel, ts)
    response = requests.get(url, headers=headers)
    message = json.loads(response.text)
    return message['messages'][0]

def send_message_with_blocks(channel, blocks):
    headers = {
        'Authorization': 'Bearer ' + SLACK_TOKEN,
        'Content-Type': 'application/json;charset=utf-8'
    }
    url = "https://slack.com/api/chat.postMessage"
    payload = {
        "token": SLACK_TOKEN,
        "channel": channel,
        "blocks": blocks["blocks"]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.text

def delete_message(channel, ts):
    headers = {
        'Authorization': 'Bearer ' + SLACK_TOKEN,
        'Content-Type': 'application/json;charset=utf-8'
    }
    url = "https://slack.com/api/chat.delete"
    payload = {
        "token": SLACK_TOKEN,
        "channel": channel,
        "ts": ts
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.text

def create_queue (message):
    queue = Queue(message["blocks"][0]["text"]["text"])
    for user in message["blocks"][3]["elements"][0]["options"]:
        queue.add(User(user["value"], user["text"]["text"]))
    return queue

class User:
    def __init__(self, id, name):
        self.id = str(id)
        self.name = name

class Queue:
    def __init__(self, name):
        self.name = name
        self.users = []

    def next(self):
        first = self.users.pop(0)
        self.users.append(first)
        return self.users

    def add(self, user):
        self.users.append(user)

    def delete(self, user: User):
        if user.id in [user.id for user in self.users]:
            for e in self.users:
                if e.id == user.id:
                    self.users.remove(e)
                    return

    def cur(self, user):
        if user.id in [user.id for user in self.users]:
            for e in self.users:
                if e.id == user.id:
                    self.users.remove(e)
                    self.users.insert(0,e)
                    return

    def mes_order(self):
        if len(self.users) == 0:
            return {"type": "plain_text", "text": "Очередь пуста", "emoji": True}
        else:
            order_str = "Очередь: \n"
            for i, user in enumerate(self.users):
                order_str += f"{i+1}. {user.name}\n"
            return {"type": "plain_text", "text": order_str, "emoji": True}

    def mes_options(self):
        options = []
        if len(self.users) == 0:
            options.append({"text": {"type": "plain_text", "text": "Никого нет", "emoji": True},
                            "value": str(0)})
        for user in self.users:
            options.append({"text": {"type": "plain_text", "text": f"{user.name}", "emoji": True},
                            "value": str(user.id)})
        return options

    def mes_top(self):
        if len(self.users) > 0:
            top = self.users[0]
            return {"type": "section",
                    "text": {"type": "mrkdwn",
                            "text": f"*Сейчас: <@{top.id}>*"},
                    "accessory": {"type": "button",
                                "text": {"type": "plain_text", "text": "Следующий", "emoji": True},
                                "action_id": "next-order"}}
        else:
            return {"type": "section",
                    "text": {"type": "mrkdwn",
                            "text": f"*Сейчас: очередь пуста*"},
                    "accessory": {"type": "button",
                                "text": {"type": "plain_text", "text": "Следующий", "emoji": True},
                                "action_id": "next-order"}}

    def mes_footer(self):
        return {"type": "actions",
                "elements": [{"type": "button",
                              "text": {"type": "plain_text", "text": "Занять", "emoji": True},
                              "action_id": "enter-order"},
                             {"type": "button",
                              "text": {"type": "plain_text", "text": "Покинуть", "emoji": True},
                              "action_id": "exit-order"}]}

    def mes_payload(self):
        return {"blocks": [{"type": "header",
                            "text": {"type": "plain_text", "text": self.name, "emoji": True}},
                           self.mes_top(),
                           {"type": "section",
                            "text": self.mes_order()},
                           {"type": "actions",
                            "elements": [{"type": "static_select",
                                          "placeholder": {"type": "plain_text",
                                                         "text": "Идёт без очереди", "emoji": True},
                                          "options": self.mes_options(),
                                          "action_id": "out-of-order"}]},
                           {"type": "divider"},
                           self.mes_footer()]}

if __name__ == "__main__":
    app.run()


#users = [User("U04LRV6HF36","Admin Here"),  User(3, "Jane"), User(2, "John"),User(4, "Jim")]
#john = User(2, "John")
#queue = Queue("test")
#for user in users:
#    queue.add(user)
#queue.cur(john)
#print(json.dumps(queue.mes_payload("test")))


# channel = "C04LPC6T52P"
# ts = "1675944894.372669"
# message = get_message_by_ts(channel, ts)
# queue = create_queue(message)
# process_queue(channel, "test")