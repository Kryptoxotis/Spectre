import os
from dotenv import load_dotenv
from agent import chat
load_dotenv()

class Spectre:
    def __init__(self):
        print("[SPECTRE]: Initialized.")

    async def ask(self, prompt):
        print(f"[You]: {prompt}")
        response = await chat(prompt)
        print(f"[Spectre]: {response}")
        return response

    def run(self):
        print("[SPECTRE]: Starting autonomous chat session...")
        import asyncio
        while True:
            prompt = input("> ")
            if prompt.lower().strip() in ["exit", "quit"]:
                break
            asyncio.run(self.ask(prompt))
