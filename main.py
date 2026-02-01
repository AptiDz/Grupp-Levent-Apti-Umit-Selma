# Importerar datetime för att skapa tidsstämplar på meddelanden
from datetime import datetime
# Importerar streamlit - biblioteket som skapar webbgränssnittet
import streamlit as st
# Importerar Config-klassen som innehåller alla inställningar
from config import Config
# Importerar LLMHandler som hanterar AI-anrop
from llm_handler import LLMHandler

# Ställer in sidans titel och layout
st.set_page_config(page_title="AI-chat", layout="wide")

# Startar session state för chattmeddelanden
if "messages" not in st.session_state:
    st.session_state.messages = []

# Skapar LLM-hanterare för AI-anrop 
if "llm_handler" not in st.session_state:
    st.session_state.llm_handler = LLMHandler()

# Sätter standardvärden för inställningar
st.session_state.setdefault("subject", "Programmering")
st.session_state.setdefault("difficulty", "Medel")

# Lägger till ett meddelande i chatthistoriken med tidsstämpel
def add_message_to_chat(role, content):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({"role": role, "content": content, "timestamp": timestamp})

# Skapar systemprompt baserat på ämne och svårighetsgrad
def get_system_prompt(subject, difficulty):
    difficulty_text = {
        "Lätt": "nybörjare med enkla förklaringar och exempel",
        "Medel": "någon med grundläggande kunskaper",
        "Svår": "avancerad nivå med djupgående förklaringar"
    }
    
    return f"""Du är en hjälpsam AI-lärare som undervisar i {subject}.
Anpassa ditt svar för {difficulty_text[difficulty]} nivå.
Var pedagogisk, tydlig och ge konkreta exempel när det är lämpligt."""

# Skickar meddelande till AI och tar emot svar
def handle_chat_response(temperature):
    subject = st.session_state["subject"]
    difficulty = st.session_state["difficulty"]
    system_prompt = get_system_prompt(subject, difficulty)
    # Hämtar konversationshistorik för AI-anropet
    conversation_history =  [
        {"role": msg["role"], "content": msg["content"]}
        for msg in st.session_state.messages
    ]
    
    # Skapar en chattbubbla för assistentens svar
    with st.chat_message("assistant"):
        placeholder = st.empty()
        accumulated = ""
        
        # Strömmar svar från AI:n
        with st.spinner("Laddar"):
            for event in st.session_state.llm_handler.stream(
                messages=conversation_history,
                temperature=temperature,
                system_message=system_prompt
            ):
                if event.get("type") == "token":
                    accumulated += event.get("text", "")
                    placeholder.write(accumulated)
                elif event.get("type") == "done":
                    accumulated = event.get("text", accumulated)
                    placeholder.write(accumulated)
                elif event.get("type") == "error":
                    st.error(f"Fel vid AI-anrop: {event.get('text')}")
                    return
    
    # Sparar AI:ns svar i chatthistoriken
    if accumulated:
        add_message_to_chat("assistant", accumulated)


# Skapar sidopanelen till vänster
with st.sidebar:
    st.header("Inställningar")
    
    # Slider för att välja temperatur (kreativitet)
    temperature = st.slider(
        "Temperatur",
        min_value=0.0,
        max_value=1.0,
        value=Config.DEFAULT_TEMPERATURE,
        step=0.1,
        help="Lägre = mer fokuserat, högre = mer kreativt.",
    )
    
    # Dropdown-meny för att välja ämne
    st.selectbox(
        "Ämne",
        ["Programmering", "Språk", "Matematik", "Design", "Dataanalys", "Projektledning"],
        key="subject",
    )
    
    # Slider för att välja svårighetsgrad
    st.select_slider("Svårighetsgrad", options=["Lätt", "Medel", "Svår"], key="difficulty")

    st.markdown("---")

    # Knapp för att rensa chatten
    if st.button("Rensa chatt"):
        st.session_state.messages = []
        st.rerun()

# Tar bort bara ikonen i status-widgeten uppe till höger
st.markdown(
    """<style>
div[data-testid="stStatusWidget"] svg{display:none!important;}
</style>""",
    unsafe_allow_html=True
)


# Huvudrubrik på sidan
st.title("AI Lärare")

# Visar alla meddelanden i chatthistoriken
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        st.caption(message["timestamp"])

# Textfält för användarinput
user_text = st.chat_input("Skriv ditt meddelande...")
if user_text:
    add_message_to_chat("user", user_text)
    
    # visa direkt i samma run
    with st.chat_message("user"):
        st.write(user_text)
        st.caption(st.session_state.messages[-1]["timestamp"])
    handle_chat_response(temperature)