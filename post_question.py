import gspread
import requests
import random

# API Documentations => https://docs.gspread.org/en/latest/api/models/worksheet.html

#----------------------   Setups   ----------------------
service_account = gspread.service_account(filename="watercooler-trivia-bot.json")
spreadsheet = service_account.open("Ascenda Watercooler Trivias")

pending_ws = spreadsheet.worksheet("Pending")
done_ws = spreadsheet.worksheet("Done")

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

try:
  [question, image_url, random_index] = get_random_qn()

  # --- Execute peepo bot command ---

  # requests.post("PEEPO_API_URL", json = { "question": question, "url": image_url })

  # ---------------------------------

  pending_ws.delete_rows(random_index) # Delete posted question from `Pending` worksheet
  done_ws.insert_row([question, image_url], len(done_ws.get_values()) + 1) # Add posted question to `Done` worksheet

except ValueError:
  print("Out of Questions!")
