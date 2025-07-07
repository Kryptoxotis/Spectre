import os
from dotenv import load_dotenv
from autogen import AssistantAgent, ChatPrompt, Tool
from autogen.oai.client import OpenAIWrapper
from supabaseCRUD import create_database, insert_quote, get_all_quotes

load_dotenv()

# 1. Initialize LLM (OpenRouter)
llm = OpenAIWrapper(
    config={
        "api_key": os.getenv("OPENROUTER_API_KEY"),
        "api_base": "https://openrouter.ai/api/v1",
        "model": "gpt-4",
    }
)

# 2. Define Tools
create_db_tool = Tool(
    name="create_database",
    func=create_database,
    description="Create a new database table with given name and schema. schema is a dict of column_name->type",
)
read_tool = Tool(
    name="read_records",
    func=get_all_quotes,
    description="Read all records from the specified database table",
)
insert_tool = Tool(
    name="insert_quote",
    func=insert_quote,
    description="Insert a new quote into the specified database table",
)

# 3. Build Agent
agent = AssistantAgent(
    name="Spectre", 
    llm=llm,
    tools=[create_db_tool, read_tool, insert_tool],
)

# 4. Chat function
async def chat(prompt: str) -> str:
    # Pass user prompt through agent to plan and invoke tools
    response = await agent.run(input=prompt)
    return response

# Example usage in FastAPI
# from fastapi import FastAPI, Request
# app = FastAPI()
#
# @app.post("/chat")
# async def chat_endpoint(request: Request):
#     data = await request.json()\#     msg = data.get("prompt")
#     reply = await chat(msg)
#     return {"reply": reply}
