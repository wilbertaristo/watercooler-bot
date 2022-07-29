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

random_question = pending_ws.row_values(random.randint(2, len(pending_ws.get_values()))) # Get random question
[question, image_url] = [i.strip() for i in random_question] # Destructuring + strip check

if question not in done_ws.col_values(1): # Check that the question has never been asked before in Done worksheet
  
  # --- Execute peepo bot command ---

  # requests.post("PEEPO_API_URL", json = { "question": question, "url": image_url })
  
  # ---------------------------------

  pending_ws.delete_rows(2) # Delete posted question from Pending worksheet
  done_ws.insert_row(random_question, len(done_ws.get_values()) + 1) # Add posted question to Done worksheet
