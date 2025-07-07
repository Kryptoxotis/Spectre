from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from spectre import Spectre

app = FastAPI()
spectre = Spectre()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "messages": []})

@app.post("/chat", response_class=HTMLResponse)
async def post_chat(request: Request):
    form = await request.form()
    user_input = form.get("message")
    response = await spectre.ask(user_input)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "messages": [{"user": user_input, "bot": response}]}
    )
