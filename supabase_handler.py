import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_TABLE = os.getenv("SUPABASE_TABLE", "quotes")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_quote(quote: str, context: str = ""):
    data = {"quote": quote, "context": context}
    result = supabase.table(SUPABASE_TABLE).insert(data).execute()
    return result

def get_all_quotes():
    result = supabase.table(SUPABASE_TABLE).select("*").execute()
    return result.data

def find_similar_quote(quote: str):
    all_quotes = get_all_quotes()
    for row in all_quotes:
        if quote.lower().strip() in row["quote"].lower():
            return row
    return None
