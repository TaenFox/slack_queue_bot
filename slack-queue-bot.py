import json, requests, random, socket, os
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
        queue = create_queue(payload["message"])

        # Do something based on the action type and value
        if action_type == "button":
            uid = payload["user"]["id"]
            uname = payload["user"]["username"]
            if action_id == "next-order":
                queue.next()
                send_message_with_blocks(payload["container"]["channel_id"],queue.mes_payload())
                delete_message(payload["container"]["channel_id"], payload["container"]["message_ts"])
                return f"User {uname} is next at {queue.name}"


            elif action_id == "enter-order":
                queue.add(User(uid,uname))
                send_message_with_blocks(payload["container"]["channel_id"],queue.mes_payload())
                delete_message(payload["container"]["channel_id"], payload["container"]["message_ts"])
                return f"User {uname} enter to order at {queue.name}"

            elif action_id == "exit-order":
                queue.delete(User(uid,uname))
                send_message_with_blocks(payload["container"]["channel_id"],queue.mes_payload())
                delete_message(payload["container"]["channel_id"], payload["container"]["message_ts"])
                return f"User {uname} is out of order {queue.name}"

        elif action_type == "static_select":
            uid = action["selected_option"]["value"]
            uname = action["selected_option"]["text"]["text"]
            send_message_with_blocks(payload["container"]["channel_id"],queue.mes_payload())
            delete_message(payload["container"]["channel_id"], payload["container"]["message_ts"])
            return f"User {uname} has been choosen in {queue.name}"

def process_queue(channel_id, title):
    queue = Queue(title)
    send_message_with_blocks(channel_id,queue.mes_payload())

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
    for user in message["blocks"][5]["elements"][0]["options"]:
        queue.add(User(user["value"], user["text"]["text"]))
    return queue

def queue_label():
    label = [
        "Идёт вне очереди",
        "Отстаёт от очереди",
        "Не следует очереди",
        "Обходит очередь",
        "Не следует правилам",
        "Пренебрегает очередью",
        "Не уважает очередь",
        "Идёт вразрез",
        "Нарушает порядок",
        "Не уступает место",
        "Не учитывает очередь",
        "Не дожидается",
        "Не следует закону",
        "Игнорирует стариков и детей",
        "Не уступает путь",
        "Не соблюдает правила",
        "Не учитывает других",
        "Обходит стариков и детей",
        "Шеф, а я вас вижу!",
        "Не учитывает законные права",
        "Мне только спросить...",
        "Отталкивает инвалидов ногами",
        "Гадает на ромашке кто потом",
        "Женщина, я опаздываю!",
        "Я ветеран, пропустите!",
        "Кто последний, тот..."
        ]
    return random.choice(label)

def queue_desc():
    desc = []
    desc.append("В магазине жираф вылез из своей клетки и прошел вперед всех в очереди к кассе. Все покупатели пораженно глядели, как жираф беспрепятственно оплачивает свой товар.")
    desc.append("В кинотеатре группа ведьм игнорировала очередь и вошла в зал первыми, несмотря на протесты других зрителей.")
    desc.append("В парке кот не ждал своей очереди и прыгнул на весло перед детьми. Он уселся там и начал смеяться, когда дети пытались вернуть весло.")
    desc.append("В ресторане пришелец из далекой галактики вошел в зал и прошел вперед всех в очереди. Он заказал необычные блюда и исчез, не дожидаясь своего заказа.")
    desc.append("В музее крыса выбежала из своей клетки и прошла вперед всех в очереди к экспонату.")
    desc.append("В кинотеатре мужчина встал в очередь к кассе, но вдруг он услышал знакомый голос. Он повернулся и увидел свою бывшую.")
    desc.append("В магазине покупатель пришел с собакой и встал в очередь. Но собака начала жаловаться и вдруг убежала.")
    desc.append("В ресторане женщина стояла в очереди и вдруг начала плакать. Остальные люди в очереди начали уступать ей место, но она продолжала плакать и не могла прийти в себя.")
    desc.append("Однажды в магазине все покупатели стояли в очереди к кассе, а один мужчина решил пройти мимо всех и подошел к кассе, где была свободна кассирша. Все вокруг недоумевали, почему он так делает, но он просто ответил: \"Я же кассир\".")
    desc.append("На автобусной остановке все ждали свой автобус, когда вдруг один пенсионер прошел мимо всех и сел в первый попавшийся автобус. Когда его упрекнули в нарушении очереди, он ответил: \"Я уже ждал свой автобус целый день, я не могу ждать еще\"")
    desc.append("В музее все ждали своей очереди, чтобы посмотреть выставку, когда вдруг один ребенок решил пройти мимо всех и зашел в зал. Его мама упрекнула его в нарушении очереди, но он ответил: \"Я же маленький, у меня нет времени ждать\"")
    desc.append("В метро была очередь к кассе, и вдруг вошел пожилой мужчина с тележкой. Он спокойно прошел мимо всех и просто сказал: \"У меня экстренный выход\". Но когда он дошел до кассы, оказалось, что он просто не хотел стоять в очереди.")
    desc.append("В кинотеатре очередь к кассе была нереально длинной, и вдруг вошла женщина с маленьким ребенком. Она прошла мимо всех и просто сказала: \"У нас срочный вход\". Но когда они дошли до кассы, она просто забрала билеты на фильм, который начинался через час.")
    desc.append("На пляже была очередь к вездеходу, который вез людей на остров. И вдруг появился жираф, который просто прошел мимо всех и уселся в вездеход")
    return random.choice(desc)
    
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def random_image():
    path = "./pic"
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    random_file = random.choice(files)

    #две строки ниже следует перекомментировать наоборот, чтобы использовать локальную папку ./pic/, а не тестовый хост
    #return "http://" + get_local_ip() + "/pic/" + random_file
    return "http://slack-queue-bot.host1814471.ru.host1814471.serv76.hostland.pro/" + random_file + "?w=250"

class User:
    def __init__(self, id, name):
        self.id = str(id)
        self.name = name

class Queue:
    def __init__(self, name):
        self.name = name
        self.users = []

    def next(self):
        if len(self.users) == 0: return
        first = self.users.pop(0)
        self.users.append(first)
        for user in self.users:
            if user.id == 0: self.users.remove(user)
        return self.users

    def add(self, user):
        if user.id == "0": return
        self.users.append(user)
        for user in self.users:
            if user.id == 0: self.users.remove(user)

    def delete(self, user: User):
        if user.id in [user.id for user in self.users]:
            for e in self.users:
                if e.id == user.id:
                    self.users.remove(e)
                    break
        for user in self.users:
            if user.id == 0: self.users.remove(user)
        return

    def cur(self, user):
        if user.id in [user.id for user in self.users]:
            for e in self.users:
                if e.id == user.id:
                    self.users.remove(e)
                    self.users.insert(0,e)
        for user in self.users:
            if user.id == 0: self.users.remove(user)
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
        if len(self.users) > 0 and self.users[0].id != "0":
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
                           {"type": "image",
                            "image_url": random_image(),
                            "alt_text": "Очередь"},
                            {"type": "context",
                             "elements": [
                                {"type": "plain_text",
                                    "text": queue_desc(),
                                    "emoji": True}
                            ]
                            },
                           self.mes_top(),
                           {"type": "section",
                            "text": self.mes_order()},
                           {"type": "actions",
                            "elements": [{"type": "static_select",
                                          "placeholder": {"type": "plain_text",
                                                         "text": queue_label(), "emoji": True},
                                          "options": self.mes_options(),
                                          "action_id": "out-of-order"}]},
                           {"type": "divider"},
                           self.mes_footer()]}

if __name__ == "__main__":
    app.run()