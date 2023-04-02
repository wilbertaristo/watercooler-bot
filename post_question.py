import gspread
import requests
import random
import os
import json
from dotenv import load_dotenv
import datetime

# API Documentations => https://docs.gspread.org/en/latest/api/models/worksheet.html

# ----------------------   Setups   ----------------------
load_dotenv()

API_URL = os.getenv("API_URL")
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
TESTING_CHANNEL_ID = os.getenv('WATERCOOLER_DEV_CHANNEL_ID')
CHANNEL_ID = os.getenv('WATERCOOLER_PRODUCTION_CHANNEL_ID')
GOOGLE_SECRETS = os.getenv('GOOGLE_SECRETS')

service_account = gspread.service_account_from_dict(json.loads(GOOGLE_SECRETS))
spreadsheet = service_account.open("Ascenda Watercooler Trivias")

pending_ws = spreadsheet.worksheet("Pending Bot Pickup")
done_ws = spreadsheet.worksheet("Done (Already asked by Bot)")

# ---------------------- Super Basic Implementation ----------------------

def get_random_qn():
  random_index = random.randint(2, len(pending_ws.get_values()))
  random_question = pending_ws.row_values(random_index)

  [question, image_url] = [i.strip() for i in random_question] # Destructuring + strip check

  if question in done_ws.col_values(1): # If question has been asked before in `Done` worksheet
    pending_ws.delete_rows(random_index) # Delete from `Pending` worksheet
    get_random_qn() # Find a new question
  else:
    return [question, image_url, random_index] # Return valid random question

def send_attachment(channel_id, text, image_url):
  return requests.post(API_URL, headers={
      "Content-type": "application/json",
      "Authorization": f"Bearer {AUTH_TOKEN}",
  }, json={
      "channel": channel_id,
      "attachments": [{"text": text, "image_url": image_url}]
  })

def send_message(channel_id, text):
  return requests.post(API_URL, headers={
      "Content-type": "application/json",
      "Authorization": f"Bearer {AUTH_TOKEN}",
  }, json={
      "channel": channel_id,
      "text": text
  })

def send_trivia():
  weekno = datetime.datetime.today().weekday()
  # 0 Monday
  # 1 Tuesday
  # 2 Wednesday
  # 3 Thursday
  # 4 Friday
  # 5 Saturday
  # 6 Sunday
  # Only send trivias on Monday, Wednesday, and Friday
  return weekno in [0, 2, 4]

if send_trivia():
  try:
    [question, image_url, random_index] = get_random_qn()

    post_request = send_attachment(CHANNEL_ID, question, image_url)

    # Optional: Send custom messages
    # post_reqeust = send_message(CHANNEL_ID, "Hello, this is Watercooler Bot :)")

    # Delete posted question from `Pending` worksheet
    pending_ws.delete_rows(random_index)
    # Add posted question to `Done` worksheet
    done_ws.insert_row([question, image_url], len(done_ws.get_values()) + 1)

  except ValueError:
    requests.post(API_URL, headers={
        "Content-type": "application/json",
        "Authorization": f"Bearer {AUTH_TOKEN}",
    }, json={
        "channel": CHANNEL_ID,
        "attachments": [{
          "text": "Water depleted. Please ping the bonding agents to refill water :sadge:", "image_url": "https://media.giphy.com/media/PjfByFswbz7w5jRJ6e/giphy-downsized.gif"
        }]
    })
