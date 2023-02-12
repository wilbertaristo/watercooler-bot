# Ascenda Watercooler Bot

Automation bot to post watercooler questions in Ascenda's `#water-cooler` slack channel  :)

## Setup
- Create your Slack App and take note of the API keys (look up Slack documentation for this)
- Make sure you have configured a Google Spreadsheet Application in Google Cloud Console and get the Google Secrets JSON file (lots of tutorials on this on youtube)
- Create `.env` file (you can follow the template in `.env.sample`) and put in the necessary API keys and Google Secrets (copy the Google Secrets JSON content over)
- Install Python & pip
- Run `pip install -r requirements.txt`
- Run `python post_question.py`
