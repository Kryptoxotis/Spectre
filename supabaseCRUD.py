import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_table(table_name: str):
    query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
        quote text,
        context text,
        created_at timestamp with time zone DEFAULT timezone('utc', now())
    );
    """
    try:
        supabase.postgrest.rpc("execute_sql", {"query": query}).execute()
        return f"Table '{table_name}' created."
    except Exception as e:
        return f"Error creating table '{table_name}': {e}"

def insert_quote(table: str, quote: str, context: str = ""):
    try:
        result = supabase.table(table).insert({"quote": quote, "context": context}).execute()
        return result.data
    except Exception as e:
        return f"Insert failed: {e}"

def get_all_quotes(table: str):
    try:
        return supabase.table(table).select("*").execute().data
    except Exception as e:
        return f"Read failed: {e}"

def delete_quote(table: str, quote_id: str):
    try:
        return supabase.table(table).delete().eq("id", quote_id).execute()
    except Exception as e:
        return f"Delete failed: {e}"
