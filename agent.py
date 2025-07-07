import os
from dotenv import load_dotenv
from autogen.agentchat import AssistantAgent
from autogen import tools
from autogen.oai.client import OpenAIWrapper
from supabaseCRUD import create_table, insert_quote, get_all_quotes

load_dotenv()

llm = OpenAIWrapper(
    config={
        "api_key": os.getenv("OPENROUTER_API_KEY"),
        "api_base": "https://openrouter.ai/api/v1",
        "model": "gpt-4",
    }
)

tools = [
    create_db_tool = tools.Tool(
        name="create_database",
        func=create_database,
        description="Create a new database table with given name and schema. schema is a dict of column_name->type",
    )
    
    read_tool = tools.Tool(
        name="read_records",
        func=get_all_quotes,
        description="Read all records from the specified database table",
    )

]

agent = AssistantAgent(name="Spectre", llm=llm, tools=tools)

async def chat(prompt: str) -> str:
    result = await agent.run(input=prompt)
    return str(result)
