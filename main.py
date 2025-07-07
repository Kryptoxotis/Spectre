from fastapi import FastAPI, Request
from spectre import Spectre

app = FastAPI()
spectre = Spectre()

@app.get("/")
def root():
    return {"message": "Spectre backend is alive."}

@app.post("/ask")
async def ask(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "")
    spectre.ask(prompt)
    return {"message": f"Processed: {prompt}"}
