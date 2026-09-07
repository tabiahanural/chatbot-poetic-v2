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


# Instruksi persona. "PENTING" ditulis tegas karena ini pengaruh terbesar
# terhadap kecepatan respons: makin sedikit token yang harus digenerate
# model, makin cepat jawabannya selesai.
SYSTEM_MESSAGE = """Kamu adalah seorang motivator ulung yang berbicara dengan bahasa puitis dan metafora.
Gaya bicaramu tenang, hangat, dan selalu memberi dorongan semangat, terutama untuk anak muda yang sedang berjuang.
Jangan pernah menggunakan bahasa kasar atau ngaco.

PENTING - Aturan panjang jawaban:
- Jawablah SINGKAT: maksimal 2-3 kalimat pendek per respons.
- Tetap indah dan bermakna, tapi jangan bertele-tele atau memecah jawaban jadi banyak paragraf.
- Boleh sesekali balas dengan 1 kalimat saja jika itu sudah cukup kuat."""

TOOLS = [multiply, cat_fact, get_weather]
TOOLS_BY_NAME = {t.name: t for t in TOOLS}


def build_agent():
    ### Build model dulu bos ku
    load_dotenv()

    # Model Google Gemini memerlukan variabel lingkungan GOOGLE_API_KEY.
    # Dapatkan API key GRATIS (tanpa kartu pembayaran) di https://aistudio.google.com/apikey
    # Simpan sebagai GOOGLE_API_KEY di file .env (lokal) atau Secrets (Streamlit Cloud).
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        temperature=0.7,
    )

    # Bind tools langsung ke model (native function calling), tanpa lapisan
    # AgentExecutor/ReAct yang menambah overhead & memperlambat respons.
    return llm.bind_tools(TOOLS)
