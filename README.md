# Vent Backend - by Pratyush
Voice Every Nagging Thought - A project for CRUx R3, 2023-24 Sem 2. The task is to create a semi-social mobile app with Flutter that lets users share their thoughts about other users anonymously.

This repo manages the backend of the main project, which you can find [here](https://github.com/RedMiner2005/vent-crux).
The Flask server will manage all calls to the LLM in use, which makes it easier for improvements to the model being used. Moreover, messages being sent to users, extracting registered users from the contact list

## Usage
* `GET /`: Can be used for testing if the server is up
* `POST /process`: JSON Request parameters: 'prompt': The input to be processed by the LLM. The response will be in JSON, with the parameters 'toSend', 'contact', 'isValid'
* `POST /send`: JSON Request parameters: 'toUser': The SHA256 hash of an e164 formatted phone number to which the message will be sent, 'message': The message to be sent. This is what is used to send the message to the recipient's inbox and also for the notification to be sent by Firebase Messaging

## Running locally
To run this locally, ensure the following environment variables are set: `GROQ_API_KEY` (Groq API key, for the LLM requests), `PORT` (by default, set it to 5000), `GOOGLE_APPLICATION_CREDENTIALS` (path to service_account.json), `IS_DEBUG` (1 or 0)