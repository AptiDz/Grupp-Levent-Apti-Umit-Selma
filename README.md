# Grupp-Levent-Apti-Umit-Selma

## AI Teacher

### Installera

cd "Grupp-Levent-Apti-Umit-Selma"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

### Konfiguera API och dess privat token

Skapa filen ".env" i roten

insida av .env filen
HUGGINGFACE_API_TOKEN=din_token_här  <---- klistra in din privata token

### Starta appen

### Terminalen
cd "Grupp-Levent-Apti-Umit-Selma"
python3 -m streamlit run main.py