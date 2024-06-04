from os import getenv
from random import random, seed
from flask import Flask, request
from groq import Groq
import json
import firebase_admin
from dotenv import load_dotenv
from pathlib import Path
from consts import *


app = Flask("VENT-Backend")

env_path = Path.cwd().joinpath(f"{ENV_FILE}")
load_dotenv(dotenv_path=env_path)

client = Groq(api_key=getenv("GROQ_API_KEY"))
firebase = firebase_admin.initialize_app()
seed(SEED)


# Process the prompt data
with open('llm/converted.json', 'r') as file:
    converted_data = json.load(file)
trimmed_data = [converted_data[0]]

for i in range(1, len(converted_data), 2):
    if random() < PROMPT_PROPORTION:
        trimmed_data.append(converted_data[i])
        trimmed_data.append(converted_data[i+1])


@app.route('/')
def home():
    return "V.E.N.T. by Pratyush - Backend. <br/><b>Usage:</b> POST to /process, /send"


@app.route('/process', methods=['POST'])
def process():
    try:
        input_string = request.get_json(force=True)[INPUT_KEY]
        assert input_string is not None
    except AssertionError as e:
        return {"error": "Please pass the prompt as an argument (JSON, with the key 'prompt')."}, 400
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
            max_tokens=1024,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
            stop=None,
        )
        return json.loads(json.loads(completion.choices[0].message.model_dump_json())["content"])
    except Exception as e:
        return {"error": str(e)}, 500


app.run(port=getenv("PORT"), debug=IS_DEBUG)
