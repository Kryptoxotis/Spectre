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
        print(f"[SPECTRE]: Table '{table_name}' created.")
    except Exception as e:
        print(f"[SPECTRE]: Failed to create table - {e}")

def insert_quote(table: str, quote: str, context: str = ""):
    return supabase.table(table).insert({"quote": quote, "context": context}).execute()

def get_all_quotes(table: str):
    return supabase.table(table).select("*").execute().data

def delete_quote(table: str, quote_id: str):
    return supabase.table(table).delete().eq("id", quote_id).execute()
