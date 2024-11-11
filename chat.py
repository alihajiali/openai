#! /usr/local/bin/python3.11
import requests, sys, subprocess
headers = {'accept': 'application/json','HTTP-AUTHORIZATION': 'Bearer openai','Content-Type': 'application/json'}
json_data = {'message': sys.argv[-1]}
print(json_data)
response = requests.post('http://195.158.230.79:1313/v1/chat/gemini', headers=headers, json=json_data).json()
print(response)
with open("./response.md", "w") as file: file.write(response)
subprocess.run(["zed", "./response.md"])
# cp ./chat.py /usr/local/bin/chat
# use by : chat "question"