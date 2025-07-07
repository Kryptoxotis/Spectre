import os
from dotenv import load_dotenv
from langchain_community.llms import OpenAI
from autogen import AssistantAgent
from autogen.oai.client import OpenAIWrapper

from supabaseCRUD import insert_quote, get_all_quotes, create_table

load_dotenv()

class Spectre:
    def __init__(self):
        # Use OpenRouter key for OpenAI-compatible access
        self.llm = OpenAIWrapper(
            config={
                "api_key": os.getenv("OPENROUTER_API_KEY"),
                "api_base": "https://openrouter.ai/api/v1",
                "model": "gpt-4",
            }
        )


        # Option A: positional arguments (name first, client second)
        self.agent = AssistantAgent("Spectre", self.llm)

        self.table_name = "quotes"
        self.setup()

    def setup(self):
        create_table(self.table_name)

    def ask(self, prompt: str):
        similar = self.find_similar(prompt)
        if similar:
            print(f"[SPECTRE]: Similar quote found:\n{similar['quote']}")
        else:
            print(f"[SPECTRE]: No similar quote found. Storing...")
            insert_quote(self.table_name, prompt)

    def find_similar(self, quote: str):
        all_quotes = get_all_quotes(self.table_name)
        for q in all_quotes:
            if quote.lower().strip() in q["quote"].lower():
                return q
        return None

    def run(self):
        print("[SPECTRE]: Awaiting input...")
        while True:
            prompt = input("> ")
            if prompt.strip().lower() == "exit":
                break
            self.ask(prompt)
