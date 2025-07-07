import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def create_table(table_name: str, schema: dict):
    columns = ",\n".join([f"{col} {dtype}" for col, dtype in schema.items()])
    query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
        {columns},
        created_at timestamp with time zone DEFAULT timezone('utc', now())
    );
    """
    try:
        supabase.postgrest.rpc("execute_sql", {"query": query}).execute()
        return f"Table '{table_name}' created."
    except Exception as e:
        return f"Error creating table '{table_name}': {e}"


def insert_record(table: str, record: dict):
    try:
        result = supabase.table(table).insert(record).execute()
        return result.data
    except Exception as e:
        return f"Insert failed: {e}"


def get_all_records(table: str):
    try:
        return supabase.table(table).select("*").execute().data
    except Exception as e:
        return f"Read failed: {e}"


def update_record(table: str, conditions: dict, updates: dict):
    try:
        query = supabase.table(table)
        for key, value in conditions.items():
            query = query.eq(key, value)
        return query.update(updates).execute().data
    except Exception as e:
        return f"Update failed: {e}"


def delete_record(table: str, conditions: dict):
    try:
        query = supabase.table(table)
        for key, value in conditions.items():
            query = query.eq(key, value)
        return query.delete().execute().data
    except Exception as e:
        return f"Delete failed: {e}"
