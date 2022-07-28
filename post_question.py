import gspread
import subprocess

# API Documentations => https://docs.gspread.org/en/latest/api/models/worksheet.html

#----------------------   Setups   ----------------------
service_account = gspread.service_account(filename="watercooler-trivia-bot.json")
spreadsheet = service_account.open("Ascenda Watercooler Trivias")

pending_ws = spreadsheet.worksheet("Pending")
done_ws = spreadsheet.worksheet("Done")

# ---------------------- Super Basic Implementation ----------------------

oldest_question = pending_ws.row_values(2) # Get oldest question which is second row of pending worksheet
[question, image_url] = oldest_question # Destructuring (optional)

if question not in done_ws.col_values(1): # Check that the question has never been asked before in Done worksheet
  
  # --- Execute peepo bot command ---

  # subprocess.run(f"curl peepo_post question='{question}' url='{image_url}'") 
  
  # ---------------------------------

  pending_ws.delete_rows(2) # Delete posted question from Pending worksheet
  done_ws.insert_row(oldest_question, len(done_ws.get_values()) + 1) # Add posted question to Done worksheet
