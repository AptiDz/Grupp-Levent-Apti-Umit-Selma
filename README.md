# Grupp-Levent-Apti-Umit-Selma

# AI Teacher

## Installera

### bash terminal
- cd "Grupp-Levent-Apti-Umit-Selma"
- python3 -m venv .venv alt python -m venv .venv
- source .venv/bin/activate alt source .venv/Scripts/activate
- pip3 install -r requirements.txt alt pip install -r requirements.txt

### Konfiguera API och dess privat token

Skapa filen ".env" i roten

Insida av .env filen

Lägg till nedan två variablar

- HUGGINGFACE_API_TOKEN=din_token_här  <---- klistra in din privata token

- HUGGINGFACE_MODEL=ServiceNow-AI/Apriel-1.6-15b-Thinker


## Starta appen

### bash Terminalen

- cd "Grupp-Levent-Apti-Umit-Selma"

- streamlit run main.py

- Gå in på Local URL för att testa appen.

### Innehåll
Egen AI Lärare som hjälper assisterar med läxor välj din ämne, svårighetsgrad och temperatur som motsvarar kreativitet ha det lågt om du vill att den ska vara med fokuserad.