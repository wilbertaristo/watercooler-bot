# Watercooler Bot

Automation bot originally created to post watercooler questions in my company's `#watercooler-chats` slack channel  :)

You can setup this bot for your own slack channel. Full walkthrough here --> https://aristo.hashnode.dev/homemade-watercooler-chat-bot

General instructions below 👇

## Setup
- Create your Slack App and take note of the API keys (look up Slack documentation for this)
- Make sure you have configured a Google Spreadsheet Application in Google Cloud Console and get the Google Secrets JSON file (lots of tutorials on this on youtube)
- Create `.env` file (you can follow the template in `.env.sample`) and put in the necessary API keys and Google Secrets (copy the Google Secrets JSON content over)
- Install Python & pip
- Run `pip install -r requirements.txt`
- Run `python post_question.py`
