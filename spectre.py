import os
from dotenv import load_dotenv

# Import the autogen chat function
from agent import chat  # This will be the AutoGen chat loop
# Optionally keep legacy quote logic if you want to use it in tools later
from supabaseCRUD import insert_quote, get_all_quotes

load_dotenv()

class Spectre:
    def __init__(self):
        print("[SPECTRE]: Initialized.")

    def run(self):
        print("[SPECTRE]: Starting autonomous chat session...")
        chat()
