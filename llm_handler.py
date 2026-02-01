# Importerar requests för att göra HTTP-anrop till API:et
import requests
# Importerar Config-klassen som innehåller alla inställningar
from config import Config

# Klass som hanterar all kommunikation med Hugging Face AI-modellen
class LLMHandler:
    
    # Startar LLM-hanteraren med API-token
    def __init__(self):
        # Hämtar API-token för att autentisera mot Hugging Face
        self.api_token = Config.HUGGINGFACE_API_TOKEN
        # URL till Hugging Face Router API
        self.chat_completions_url = "https://router.huggingface.co/v1/chat/completions"

    # Formaterar meddelanden till chat-format
    def _format_messages_for_chat(self, messages, system_message=None):
        chat_messages = []

        # Lägger till systemprompt om den finns
        if system_message:
            # Instruerar AI:n att inte visa sin tankegång i svaret
            system_message = (
                system_message
                + "\n\nVIKTIGT: Svara utan att visa dina resonemang/tankegång. "
                  "Ge bara svaret."
            )
            chat_messages.append({"role": "system", "content": system_message})

        # Loopar igenom alla meddelanden och formaterar dem
        for msg in messages or []:
            role = (msg.get("role") or "user").strip().lower()
            content = msg.get("content", "")

            # Hoppar över meddelanden som inte är från user eller assistant
            if role not in ("user", "assistant"):
                continue

            chat_messages.append({"role": role, "content": content})

        return chat_messages

    # Skickar meddelanden till AI:n och strömmar tillbaka svaret
    def stream(self, messages, model_name=None, temperature=None, system_message=None):
        try:
            # Använder standardvärden om inget anges
            model = model_name or Config.DEFAULT_MODEL
            temp = temperature if temperature is not None else Config.DEFAULT_TEMPERATURE
            
            # Formaterar meddelanden till rätt format
            chat_messages = self._format_messages_for_chat(messages, system_message)

            # Skapar headers för API-anropet med autentisering
            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json"
            }

            # Skapar payload med alla inställningar för AI-anropet
            payload = {
                "model": model,
                "messages": chat_messages,
                "temperature": temp,
                "max_tokens": 512,
                "stream": False,
            }

            # Skickar POST-request till Hugging Face API:et
            response = requests.post(self.chat_completions_url, headers=headers, json=payload, timeout=120)
            
            # Kontrollerar om API-anropet lyckades
            if response.status_code != 200:
                if response.status_code == 503:
                    raise Exception(f"Modellen laddas fortfarande. Försök igen om en stund.")
                if response.status_code == 400 and "model_not_supported" in response.text:
                    raise Exception(
                        "Modellen stöds inte för din token/provider. "
                        "Välj en modell som finns i `https://router.huggingface.co/v1/models`."
                    )
                raise Exception(f"API error: {response.status_code} - {response.text}")
            
            # Konverterar API-svaret till JSON och extraherar texten
            result = response.json()
            try:
                text = result["choices"][0]["message"]["content"]
            except Exception:
                text = str(result)
            
            # Strömmar ut texten i små delar (chunks) för att simulera streaming
            chunk_size = 25
            for i in range(0, len(text), chunk_size):    
                yield {"type": "token", "text": text[i:i+chunk_size]}
            
            # Skickar det kompletta svaret när allt är klart
            yield {"type": "done", "text": text}
            
        # Fångar upp eventuella fel och skickar felmeddelande
        except Exception as e:
            yield {"type": "error", "text": str(e)}
