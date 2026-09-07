import time

import streamlit as st
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from bot import build_agent, SYSTEM_MESSAGE, TOOLS_BY_NAME # Mengimpor fungsi build_agen

# set_page_config harus menjadi perintah Streamlit pertama yang dipanggil.
st.set_page_config(
    page_title="Cermin Aksara Senja",
    page_icon="ð", # Atau ð / ð
    layout="centered"
)

# Jumlah percobaan ulang saat model mengembalikan error sementara
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2

# --- 1. Inisialisasi Model (Hanya Sekali) ---
# Menggunakan st.cache_resource untuk memastikan model (dengan tools yang sudah di-bind)
# dibuat hanya sekali, dipakai ulang di seluruh sesi.
@st.cache_resource
def get_agent():
    # Model Google Gemini memerlukan variabel lingkungan GOOGLE_API_KEY.
    # Pastikan file .env (yang dimuat oleh load_dotenv di bot.py) sudah tersedia
    # dan berisi API key yang valid, atau sudah diatur sebagai Secret di Streamlit Cloud.
    return build_agent()

llm = get_agent()

st.title("ð¯ï¸ Cermin Aksara Senja ð")
st.subheader("Tempat Hening bagi Jiwa yang Mencari Jawaban")
st.markdown("---")

# --- 2. Inisialisasi Riwayat Pesan ---
# st.session_state digunakan untuk menyimpan riwayat pesan antar interaksi.
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Berikan pesan sambutan awal dari bot
    initial_message = "Di penghujung hari, di bawah naungan Senja, aku menantimu. Aku adalah aksara yang siap merangkai bait-bait motivasi. Apa kabar hatimu? Mari bercerita tanpa perlu tergesa."
    st.session_state.messages.append({"role": "assistant", "content": initial_message})

# --- 3. Tampilkan Riwayat Pesan dengan Ikon Kustom ---
for message in st.session_state.messages:
    # Atur ikon berdasarkan peran
    if message["role"] == "user":
        icon = "ðï¸"
    else:
        icon = "ð" # Ikon Bot Puitis

    with st.chat_message(message["role"], avatar=icon):
        st.markdown(message["content"])


def to_lc_messages(session_messages):
    """Ubah riwayat chat (list of dict) jadi list message LangChain untuk dikirim ke model."""
    lc_messages = [SystemMessage(content=SYSTEM_MESSAGE)]
    for m in session_messages:
        if m["role"] == "user":
            lc_messages.append(HumanMessage(content=m["content"]))
        else:
            lc_messages.append(AIMessage(content=m["content"]))
    return lc_messages


def stream_answer(llm, messages):
    """Streaming jawaban token-per-token, dengan satu putaran tool-calling bila diperlukan."""
    full = None
    for chunk in llm.stream(messages):
        full = chunk if full is None else full + chunk
        if chunk.content:
            yield chunk.content

    # Jika model minta memanggil salah satu tool (multiply/cat_fact/get_weather),
    # jalankan tool-nya lalu lanjutkan streaming jawaban akhir yang sudah puitis.
    if full is not None and getattr(full, "tool_calls", None):
        messages.append(full)
        for call in full.tool_calls:
            tool_fn = TOOLS_BY_NAME.get(call["name"])
            if tool_fn is not None:
                try:
                    result = tool_fn.invoke(call["args"])
                except Exception as e:
                    result = f"Something went wrong with the tool: {e}"
            else:
                result = f"Tool {call['name']} tidak ditemukan."
            messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

        for chunk in llm.stream(messages):
            if chunk.content:
                yield chunk.content


def resume_stream(first_chunk, rest):
    """Sambungkan potongan pertama (yang sudah diambil untuk cek konten) dengan sisa stream."""
    if first_chunk:
        yield first_chunk
    yield from rest


# --- 4. Memproses Input Pengguna (Puitis) ---
# Ubah placeholder chat_input menjadi puitis
if prompt := st.chat_input("Bisikkan apa yang hatimu rasakan..."):
    # Tambahkan pesan pengguna ke riwayat dan tampilkan
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Avatar Pengguna: Ganti 'user' dengan ikon puitis (pena)
    with st.chat_message("user", avatar="ðï¸"):
        st.markdown(prompt)

    # Panggil Model dan tampilkan respons secara streaming
    # Avatar Bot: Ikon puitis (gulungan aksara)
    with st.chat_message("assistant", avatar="ð"):
        last_error = None
        full_response = None

        # Coba beberapa kali karena backend model kadang mengembalikan
        # error sementara (mis. rate limit atao gangguan jaringan).
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                messages = to_lc_messages(st.session_state.messages)
                gen = stream_answer(llm, messages)

                # Pesan Spinner: Merangkai aksara dari keheningan senja...
                # Tampil selagi menunggu token pertama, lalu digantikan oleh
                # teks yang mengalir (streaming) begitu jawaban mulai datang.
                with st.spinner("Merangkai aksara dari keheningan senja..."):
                    first_chunk = next(gen, "")

                full_response = st.write_stream(resume_stream(first_chunk, gen))
                last_error = None
                break

            except Exception as e:
                last_error = e
                # Cetak traceback asli ke log server (terlihat di Streamlit Cloud logs)
                # supaya mudah didiagnosis, tanpa menampilkannya ke pengguna.
                print(f"[stream_answer] percobaan {attempt}/{MAX_RETRIES} gagal: {e}")
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY_SECONDS)

        if last_error is not None:
            # Tangani kesalahan dengan bahasa puitis, setelah semua percobaan gagal
            full_response = f"Sayang sekali, hening ini terpecah. Ada badai tak terlihat yang mengganggu alunan kata: {last_error}"
            st.markdown(full_response)

    # Tambahkan respons bot ke riwayat
    st.session_state.messages.append({"role": "assistant", "content": full_response})
