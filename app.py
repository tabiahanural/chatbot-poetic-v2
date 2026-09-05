import time

import streamlit as st
from bot import build_agent # Mengimpor fungsi build_agen

# set_page_config harus menjadi perintah Streamlit pertama yang dipanggil.
st.set_page_config(
    page_title="Cermin Aksara Senja",
    page_icon="🌙", # Atau 🌅 / 🌙
    layout="centered"
)

# Jumlah percobaan ulang saat model mengembalikan error sementara
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2

# --- 1. Inisialisasi Agen (Hanya Sekali) ---
# Menggunakan st.cache_resource untuk memastikan agen (termasuk model & memori)
# dibuat hanya sekali, mempertahankan memori di seluruh sesi.
@st.cache_resource
def get_agent():
    # Model Google Gemini memerlukan variabel lingkungan GOOGLE_API_KEY.
    # Pastikan file .env (yang dimuat oleh load_dotenv di bot.py) sudah tersedia
    # dan berisi API key yang valid, atau sudah diatur sebagai Secret di Streamlit Cloud.
    return build_agent()

agent_executor = get_agent()

st.title("🕯️ Cermin Aksara Senja 🌅")
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
        icon = "🖋️"
    else:
        icon = "📜" # Ikon Bot Puitis

    with st.chat_message(message["role"], avatar=icon):
        st.markdown(message["content"])

# --- 4. Memproses Input Pengguna (Puitis) ---
# Ubah placeholder chat_input menjadi puitis
if prompt := st.chat_input("Bisikkan apa yang hatimu rasakan..."):
    # Tambahkan pesan pengguna ke riwayat dan tampilkan
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Avatar Pengguna: Ganti 'user' dengan ikon puitis (pena)
    with st.chat_message("user", avatar="🖋️"):
        st.markdown(prompt)

    # Panggil Agen dan tampilkan respons
    # Avatar Bot: Ikon puitis (gulungan aksara)
    with st.chat_message("assistant", avatar="📜"):

        # Pesan Spinner: Merangkai aksara dari keheningan senja...
        with st.spinner("Merangkai aksara dari keheningan senja..."):
            last_error = None
            full_response = None

            # Coba beberapa kali karena backend model kadang mengembalikan
            # error sementara (mis. rate limit atau gangguan jaringan).
            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    # Panggil agen dengan input pengguna
                    # Note: 'agent_executor.invoke' adalah fungsi teknis, tidak perlu diganti
                    response = agent_executor.invoke({"input": prompt})

                    # Ambil output teks dari respons agen
                    full_response = response.get('output', 'Aksara senja tak terangkai sempurna. Ada jeda yang tak terduga.')
                    last_error = None
                    break

                except Exception as e:
                    last_error = e
                    # Cetak traceback asli ke log server (terlihat di Streamlit Cloud logs)
                    # supaya mudah didiagnosis, tanpa menampilkannya ke pengguna.
                    print(f"[agent_executor.invoke] percobaan {attempt}/{MAX_RETRIES} gagal: {e}")
                    if attempt < MAX_RETRIES:
                        time.sleep(RETRY_DELAY_SECONDS)

            if last_error is not None:
                # Tangani kesalahan dengan bahasa puitis, setelah semua percobaan gagal
                full_response = f"Sayang sekali, hening ini terpecah. Ada badai tak terlihat yang mengganggu alunan kata: {last_error}"

        # Tambahkan respons bot ke riwayat
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.markdown(full_response)
