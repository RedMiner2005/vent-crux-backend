from groq import Groq
from random import random, seed
import json

client = Groq(api_key="<API_KEY_HERE>")
# Read the converted.json file
with open('converted.json', 'r') as file:
    converted_data = json.load(file)
trimmed_data = [converted_data[0]]

seed(20102005)

for i in range(1, len(converted_data), 2):
    if random() < 0.7:
        trimmed_data.append(converted_data[i])
        trimmed_data.append(converted_data[i+1])

# Pass the converted data to messages in the completion
completion = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=trimmed_data + [{
        "role": "user",
        "content": input("Enter your prompt: ")
    }],
    temperature=0,
    max_tokens=1024,
    top_p=1,
    stream=False,
    response_format={"type": "json_object"},
    stop=None,
)

print(completion.choices[0].message.model_dump_json())
