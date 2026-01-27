# Grupp-Levent-Apti-Umit-Selma
AI Teacher

### Installera

cd "Grupp-Levent-Apti-Umit-Selma"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


## Konfigurera token

Skapa filen `Grupp-Levent-Apti-Umit-Selma/.env`:

```env
HUGGINGFACE_API_TOKEN=din_token_här
# valfritt:
HUGGINGFACE_MODEL=meta-llama/Meta-Llama-3.1-8B-Instruct
```

## Kör appen

```bash
cd "Grupp-Levent-Apti-Umit-Selma"
python3 -m streamlit run main.py
```