import os
from dotenv import load_dotenv
from autogen import AssistantAgent, Tool
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
    Tool(
        name="create_table",
        func=create_table,
        description="Create a new table in Supabase with specified name and predefined quote schema."
    ),
    Tool(
        name="read_records",
        func=get_all_quotes,
        description="Read all records from a given table."
    ),
    Tool(
        name="insert_quote",
        func=insert_quote,
        description="Insert a new quote with optional context into a given table."
    )
]

agent = AssistantAgent(name="Spectre", llm=llm, tools=tools)

async def chat(prompt: str) -> str:
    result = await agent.run(input=prompt)
    return str(result)
