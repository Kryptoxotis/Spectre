import os
from dotenv import load_dotenv
from autogen.agentchat import AssistantAgent
from autogen import tools as ag_tools
from autogen.oai.client import OpenAIWrapper
from supabaseCRUD import (
    create_table,
    insert_record,
    get_all_records,
    update_record,
    delete_record,
)

load_dotenv()

# Initialize LLM via OpenRouter
llm = OpenAIWrapper(
    config={
        "api_key": os.getenv("OPENROUTER_API_KEY"),
        "api_base": "https://openrouter.ai/api/v1",
        "model": "openai/gpt-4",
    }
)

# Define generic CRUD tools
tool_list = [
    ag_tools.Tool(
        name="create_table",
        callable=create_table,
        description="Create a Supabase table. Args: table_name (str), schema (dict of column_name -> type)."
    ),
    ag_tools.Tool(
        name="insert_record",
        callable=insert_record,
        description="Insert a record into a Supabase table. Args: table_name (str), record (dict of column_name -> value)."
    ),
    ag_tools.Tool(
        name="get_all_records",
        callable=get_all_records,
        description="Get all records from a Supabase table. Args: table_name (str)."
    ),
    ag_tools.Tool(
        name="update_record",
        callable=update_record,
        description="Update records in a Supabase table. Args: table_name (str), conditions (dict), updates (dict)."
    ),
    ag_tools.Tool(
        name="delete_record",
        callable=delete_record,
        description="Delete records in a Supabase table. Args: table_name (str), conditions (dict)."
    )
]

# Define the Spectre assistant
agent = AssistantAgent(
    name="Spectre",
    llm=llm,
    tools=tool_list,
)

# Chat function to be used in the main loop or FastAPI
async def chat(prompt: str) -> str:
    result = await agent.run(input=prompt)
    return str(result)
