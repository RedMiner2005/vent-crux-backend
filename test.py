import requests
import json

# Define the URL and payload
url = 'http://localhost:5000/process'
payload = {'prompt': input("Prompt: ")}

# Convert the payload to JSON
json_payload = json.dumps(payload)

# Set the headers
headers = {'Content-Type': 'application/json'}

# Make the POST request
response = requests.post(url, data=json_payload, headers=headers)

# Print the response
print(response.json())