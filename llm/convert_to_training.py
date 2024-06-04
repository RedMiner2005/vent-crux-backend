import csv
import json


csv_file = 'llm_training_data_init.csv'
json_file = 'converted.json'
data = []

with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    next(reader)
    
    for row in reader:
        user_input = row[0]
        to_send = row[1] if row[1] != '' else None
        contact = row[2] if row[2] != '' else None
        is_valid = True if row[3] == "TRUE" else False
        
        user_message = {
            "role": "user",
            "content": user_input
        }
        
        assistant_message = {
            "role": "assistant",
            "content": json.dumps({"toSend": to_send, "contact": contact, "isValid": is_valid})
        }
        
        data.append(user_message)
        data.append(assistant_message)


with open(json_file, 'w') as file:
    json.dump(data, file)