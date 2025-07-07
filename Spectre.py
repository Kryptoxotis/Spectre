import os
from langchain.llms import OpenAI
from autogen import AssistantAgent
from supabase import insert_quote, get_all_quotes, create_table
from dotenv import load_dotenv

load_dotenv()

class Spectre:
    def __init__(self):
        self.llm = OpenAI(openai_api_key=os.getenv("OPENROUTER_API_KEY"))
        self.agent = AssistantAgent("Spectre", llm_config={"config_list": [{"model": "gpt-4"}]})
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
