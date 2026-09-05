# 🕯️ Cermin Aksara Senja: A Poetic & Motivational Chatbot 🌅

Sebuah Agen AI yang dirancang untuk memberikan motivasi dan inspirasi melalui respons yang puitis, mendalam, dan kaya metafora.

Versi ini menggunakan **Google Gemini** (gratis, tanpa perlu kartu pembayaran) sebagai model bahasa, menggantikan versi sebelumnya yang memakai Claude 3.5 Haiku via Replicate.

---

## 🌟 Tentang Proyek

**Cermin Aksara Senja** adalah *chatbot* yang dibangun menggunakan LangChain dan Streamlit. Berbeda dari *chatbot* konvensional, proyek ini berfokus pada **persona** yang kuat: seorang sahabat bijaksana yang berbicara dengan bahasa indah untuk menemani dan memberi semangat, terutama bagi anak muda yang sedang mencari arah.

### 🎭 Poetic Chatbot
* **Gaya Bahasa:** Puitis, tenang, bijaksana, dan penuh metafora.
* **Misi:** Memberikan motivasi, refleksi, dan pandangan yang mendalam atas setiap keresahan pengguna.
* **Judul Aplikasi:** Cermin Aksara Senja

---

## ⚙️ Fitur Utama

Meskipun fokus pada puisi, bot ini juga memiliki kemampuan fungsional yang unik:

1.  **Motivasi Puitis:** Memberikan nasihat dan dorongan semangat dalam bait-bait yang indah.
2.  **Kalkulasi Metaforis:** Mampu melakukan perkalian (**multiply**) dan menyajikan hasilnya dalam narasi puitis.
3.  **Ramalan Alam:** Mampu mendapatkan data cuaca (`get_weather`) dan menginterpretasikannya secara metaforis.
4.  **Fakta Estetis:** Mampu mengambil fakta acak (misalnya, fakta kucing) dan mengubahnya menjadi pengamatan puitis.
5.  **Tahan Gangguan:** Otomatis mencoba ulang (retry) saat model sempat mengembalikan error sementara.

---

## 🛠️ Teknologi yang Digunakan

* **LLM Framework:** [LangChain](https://www.langchain.com/) (Untuk agen, memori, dan tools)
* **LLM Model:** Google Gemini 2.0 Flash (via `langchain-google-genai`)
* **Antarmuka Pengguna (UI):** [Streamlit](https://streamlit.io/)
* **Manajemen Paket:** `requirements.txt`

---

## 🚀 Setup & Menjalankan Secara Lokal

1.  **Dapatkan API Key Google Gemini (gratis, tanpa kartu):**
    Buka [aistudio.google.com/apikey](https://aistudio.google.com/apikey), login dengan akun Google, lalu klik "Create API key".

2.  **Buat file `.env`** di root proyek (lihat `.env.example`):
    ```
    GOOGLE_API_KEY=isi_dengan_api_key_kamu
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan aplikasi:**
    ```bash
    streamlit run app.py
    ```

---

## ☁️ Deploy ke Streamlit Community Cloud

1.  Push repo ini ke akun GitHub kamu.
2.  Buka [share.streamlit.io](https://share.streamlit.io), hubungkan ke repo ini, pilih `app.py` sebagai entry point.
3.  Di menu **Settings → Secrets**, tambahkan:
    ```
    GOOGLE_API_KEY = "isi_dengan_api_key_kamu"
    ```
4.  Deploy — aplikasi akan otomatis redeploy setiap kali kamu push perubahan baru.

---
