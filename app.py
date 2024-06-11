from random import random, seed
from hashlib import sha256
import base64
from time import time_ns
from flask import Flask, request
from groq import Groq
import json
import firebase_admin
from firebase_admin import firestore, messaging
from consts import Consts


app = Flask("VENT-Backend")

consts = Consts()
client = Groq(api_key=consts.GROQ_API_KEY)
firebase = firebase_admin.initialize_app()
seed(consts.SEED)


# Process the prompt data
with open('llm/converted.json', 'r', encoding='utf-8') as file:
    converted_data = json.load(file)
trimmed_data = [converted_data[0]]

for i in range(1, len(converted_data), 2):
    if random() < consts.PROMPT_PROPORTION:
        trimmed_data.append(converted_data[i])
        trimmed_data.append(converted_data[i+1])


def get_sha256_hash(text):
    hash_object = sha256(text.encode())
    return hash_object.hexdigest()

@app.route('/')
def home():
    return "V.E.N.T. by Pratyush - Backend. <br/><b>Usage:</b> POST to /process, /send"


@app.route('/process', methods=['POST'])
def process():
    try:
        input_string = request.get_json(force=True)[consts.PROCESS_INPUT_KEY]
        assert input_string is not None and len(input_string) < 300
    except AssertionError as e:
        return {"error": f"Please pass the prompt as an argument (JSON, with the key '{consts.PROCESS_INPUT_KEY}')."}, 400
    except Exception as e:
        return {"error": "Prompt issue: " + str(e)}, 400

    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=trimmed_data + [{
                "role": "user",
                "content": input_string
            }],
            temperature=0,
            max_tokens=8192,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
            stop=None,
        )
        return json.loads(json.loads(completion.choices[0].message.model_dump_json())["content"])
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/send', methods=['POST'])
def send():
    try:
        to_user = request.get_json(force=True)[consts.SEND_USER_KEY]
        message = request.get_json(force=True)[consts.SEND_MSG_KEY]
        assert to_user is not None
        assert message is not None
        db = firestore.client()
        doc_ref = db.collection('users').document(to_user)  # to_user is now the sha256 hash of the contact
        current_time = str(time_ns() // 1000000).encode('utf-8')
        encoded_time = base64.b64encode(current_time).decode('utf-8')
        doc_ref.update({
            'inbox': firestore.ArrayUnion([{'time': encoded_time, 'message': message}]),
            'unreadCount': firestore.Increment(1)
        })
        # Construct the message
        doc = doc_ref.get()
        notification_token = doc.get('notification_token')
        message = messaging.Message(
            notification=messaging.Notification(
                title='Someone vented about you',
                body=message
            ),
            token=notification_token
        )
        response = messaging.send(message)
        return {"status": "success"}
    except AssertionError as e:
        return {"error": f"Please pass the correct args (JSON, '{consts.SEND_USER_KEY}' (SHA256 hash of an e164 number), '{consts.SEND_MSG_KEY}')."}, 400
    except Exception as e:
        if str(e) == "Message.token must be a non-empty string.":
            return {"status": "success"}
        return {"error": "Send message issue (Try checking if you are sending the hash of the number): " + str(e)}, 400


if consts.IS_DEBUG == '1':
    app.run(port=consts.PORT, debug=consts.IS_DEBUG)
else:
    from waitress import serve
    serve(app, host="0.0.0.0", port=consts.PORT)
