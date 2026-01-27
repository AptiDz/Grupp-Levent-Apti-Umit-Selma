# Grupp-Levent-Apti-Umit-Selma

# AI Teacher

## Installera

cd "Grupp-Levent-Apti-Umit-Selma"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

### Konfiguera API och dess privat token

Skapa filen ".env" i roten

Insida av .env filen

lägg till nedan två variablar

- HUGGINGFACE_API_TOKEN=din_token_här  <---- klistra in din privata token

- HUGGINGFACE_MODEL=ServiceNow-AI/Apriel-1.6-15b-Thinker


## Starta appen

### Terminalen

cd "Grupp-Levent-Apti-Umit-Selma"

python3 -m streamlit run main.py