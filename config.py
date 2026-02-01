# Importerar os för att läsa miljövariabler
import os
# Importerar load_dotenv för att läsa in hemliga nycklar från .env-fil
from dotenv import load_dotenv
# Importerar pathlib för att hantera filsökvägar på ett säkert sätt
import pathlib
# Skapar sökväg till .env-filen i samma mapp som denna fil
env_path = pathlib.Path(__file__).parent / ".env"
# Laddar in miljövariabler API-nyckel från .env-filen
load_dotenv(dotenv_path=env_path)
# Konfigurationsklass som innehåller alla inställningar för applikationen
class Config:
    # Hämtar Hugging Face API-token från miljövariabler
    HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
    # Modell som används för AI-svaren
    DEFAULT_MODEL = os.getenv("HUGGINGFACE_MODEL")
    # Standardtemperatur för AI-svaren går från 0.0 motsvarar fokus, 1.0 motsvarar kreativ
    DEFAULT_TEMPERATURE = 0.7