import requests

url = 'http://localhost:5000/process'
data = {'prompt': 'I like her'}

response = requests.post(url, json=data)

print(response.text)