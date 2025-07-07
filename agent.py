import os
from dotenv import load_dotenv
from autogen.agentchat import AssistantAgent
from autogen import tools as ag_tools
from autogen.oai.client import OpenAIWrapper
from supabaseCRUD import create_table, insert_quote, get_all_quotes

load_dotenv()

# Initialize LLM via OpenRouter
llm = OpenAIWrapper(
    config={
        "api_key": os.getenv("OPENROUTER_API_KEY"),
        "api_base": "https://openrouter.ai/api/v1",
        "model": "openai/gpt-4",  # ✅ Make sure this matches an actual OpenRouter model
    }
)

# Define tools
create_db_tool = ag_tools.Tool(
    name="create_database",
    function=create_table,
    description="Create a new database table with the given name and schema (a dict of column_name->type)."
)

read_tool = ag_tools.Tool(
    name="read_records",
    function=get_all_quotes,
    description="Read all records from the specified Supabase table."
)

insert_tool = ag_tools.Tool(
    name="insert_quote",
    function=insert_quote,
    description="Insert a quote into a Supabase table. Args: table name, quote, and optional context."
)

# Tool list
tool_list = [create_db_tool, read_tool, insert_tool]

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
