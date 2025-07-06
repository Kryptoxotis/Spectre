# Spectre AI (Quote Memory Assistant)

This is a minimal prototype of an AI assistant (Spectre) that:
- Accepts natural language input (CLI for now)
- Searches a quote database (via Supabase)
- Saves new quotes, avoids duplicates
- Talks via OpenRouter AI (Claude or GPT-4)

---

## Setup Instructions

### 1. Create Supabase Project
- Add a table called `quotes`
- Columns: `id (uuid)`, `quote (text)`, `context (text)`, `created_at (timestamp)`

### 2. Environment Variables
- Copy `.env.example` ➝ `.env`
- Fill in your OpenRouter + Supabase keys

### 3. Run Locally

```bash
pip install -r requirements.txt
python main.py
