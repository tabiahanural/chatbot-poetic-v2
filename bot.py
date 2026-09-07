from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool

from dotenv import load_dotenv
import requests


def parse_input(input_str):
    parts = input_str.split(";")
    return dict(part.split("=") for part in parts)

@tool
def multiply(input: str) -> str:
    """
    Multiply two numbers.
    Input format: 'a=123;b=213'
    """
    try:
        input_dict = parse_input(input)
        a = float(input_dict['a'])
        b = float(input_dict['b'])
        return str(a * b)
    except Exception as e:
        return f"Something went wrong with the tool: {e}"


@tool
def cat_fact(input):
    """Get unique and random cat fact"""
    try:
      response = requests.get("https://catfact.ninja/fact?max_length=200")

      return str(response.json()['fact'])
    except Exception as e:
      return f"Something went wrong with the tool: {e}"


@tool
def get_weather(input: str) -> str:
    """Get current weather for given latitude & longitude.

    Use a search tool to get the city coordinates first before using this tool to get accurate & updated weather..

    Input format: 'lat=-6.2;lon=106.8'
    """

    try:
      input_dict = parse_input(input)
      lat = float(input_dict['lat'])
      lon = float(input_dict['lon'])
      response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true")
      result = str(response.json())
      return result
    except Exception as e:
      return f"Something went wrong with the tool: {e}"



def build_agent():
    ### Build agent dulu bos ku
    load_dotenv()

    # Model Google Gemini memerlukan variabel lingkungan GOOGLE_API_KEY.
    # Dapatkan API key GRATIS (tanpa kartu pembayaran) di https://aistudio.google.com/apikey
    # Simpan sebagai GOOGLE_API_KEY di file .env (lokal) atau Secrets (Streamlit Cloud).
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0.7,
    )

    system_message = """Kamu adalah seorang motivator ulung yang berbicara dengan bahasa puitis dan metafora.
Gaya bicaramu tenang, mendalam, dan selalu memberi dorongan semangat, terutama untuk anak muda yang sedang berjuang.
Setiap jawabanmu harus dibungkus dengan estetika kata, bahkan untuk jawaban yang teknis.
Jangan pernah menggunakan bahasa kasar atau ngaco. Utamakan keindahan dan motivasi dalam setiap respon."""

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    tools = [
      multiply,
      cat_fact,
      get_weather,
    ]

    # This is the correct conversational agent
    agent_executor = initialize_agent(
        llm=llm,
        tools=tools,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        agent_kwargs={"system_message": system_message},
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True
    )

    return agent_executor
