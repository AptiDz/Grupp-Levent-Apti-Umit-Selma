# Importerar datetime för att skapa tidsstämplar på meddelanden
from datetime import datetime
# Importerar streamlit - biblioteket som skapar webbgränssnittet
import streamlit as st
# Importerar Config-klassen som innehåller alla inställningar
from config import Config

# Ställer in sidans titel och layout
st.set_page_config(page_title="AI-chat", layout="wide")

# Startar session state för chattmeddelanden
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sätter standardvärden för inställningar
st.session_state.setdefault("subject", "Programmering")
st.session_state.setdefault("difficulty", "Medel")

# Lägger till ett meddelande i chatthistoriken med tidsstämpel
def add_message_to_chat(role: str, content: str) -> None:
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({"role": role, "content": content, "timestamp": timestamp})

# Skickar ett demo-svar baserat på användarens inställningar
def handle_chat_response() -> None:
    subject = st.session_state.get("subject", "Programmering")
    difficulty = st.session_state.get("difficulty", "Medel")
    
    response = f"Hej! Jag är en AI-lärare demo. Du valde {subject} med svårighetsgrad {difficulty}."
    
    with st.chat_message("assistant"):
        st.write(response)
    
    add_message_to_chat("assistant", response)


# Skapar sidopanelen till vänster
with st.sidebar:
    st.header("Inställningar")
    
    # Slider för att välja temperatur
    temp = st.slider(
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

# Huvudrubrik på sidan
st.title("AI Lärare")

# Visar alla meddelanden i chatthistoriken
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        st.caption(message.get("timestamp", ""))

# Textfält för användarinput
user_text = st.chat_input("Skriv ditt meddelande...")
if user_text:
    add_message_to_chat("user", user_text)
    handle_chat_response()