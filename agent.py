import os
from dotenv import load_dotenv
from autogen.agentchat import AssistantAgent
from autogen import tools as ag_tools  # Avoid conflict with variable name
from autogen.oai.client import OpenAIWrapper
from supabaseCRUD import create_table, insert_quote, get_all_quotes

load_dotenv()

# Initialize LLM
llm = OpenAIWrapper(
    config={
        "api_key": os.getenv("OPENROUTER_API_KEY"),
        "api_base": "https://openrouter.ai/api/v1",
        "model": "gpt-4",
    }
)

# Define tools
create_db_tool = ag_tools.Tool(
    name="create_database",
    func=create_table,
    description="Create a new database table with given name and schema. Schema is a dict of column_name->type.",
)

read_tool = ag_tools.Tool(
    name="read_records",
    func=get_all_quotes,
    description="Read all records from the specified database table.",
)

# For now, include insert_quote as a tool so Spectre can at least log quotes
# Later, you can remove this and have it learn when/how to call it dynamically
insert_tool = ag_tools.Tool(
    name="insert_quote",
    func=insert_quote,
    description="Insert a quote into the specified table. Args: table name, quote, context (optional).",
)

# Tool list
tool_list = [create_db_tool, read_tool, insert_tool]

# Create the AssistantAgent
agent = AssistantAgent(name="Spectre", llm=llm, tools=tool_list)

# Chat handler
async def chat(prompt: str) -> str:
    result = await agent.run(input=prompt)
    return str(result)
