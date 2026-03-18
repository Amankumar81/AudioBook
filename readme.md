# 🎙️ Multilingual Audiobook Generator
> **Transforming Static Documents into High-Fidelity Audio Experiences.**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![AI-Powered](https://img.shields.io/badge/AI-Powered-blue?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com/text-to-speech)
[![Demo](https://img.shields.io/badge/Live-Demo-brightgreen?style=for-the-badge&logo=vercel)](https://audio-book-3q5b.onrender.com)

---

## 🌟 Overview
Modern lifestyles demand efficiency, yet vast amounts of valuable information remain locked in static text. This **Multilingual Audiobook Web Application** bridges the gap between busy schedules and personal growth. 

By leveraging **AI-driven translation** and **Neural Text-to-Speech (TTS)**, this tool democratizes knowledge for non-native speakers, provides critical accessibility for users with visual impairments, and turns "dead time" (commutes/workouts) into high-value learning.

---

## ⚠️ The Problem
1. **Language Barriers:** Valuable information remains inaccessible to non-native speakers, limiting global collaboration.
2. **Accessibility Needs:** Individuals with visual impairments or dyslexia are often underserved by static text formats.
3. **Time Constraints:** Reading lengthy documents is time-consuming; audio offers a multitasking alternative.

## ✅ The Solution
1. **Real-Time Translation:** Integrates AI engines to convert documents into native languages instantly.
2. **Inclusive Audio-First Design:** High-fidelity speech with customizable tones and pacing for all learner types.
3. **"Dead Time" Productivity:** Converts PDF, DOCX, and TXT into portable audio for learning on the go.

---

## 🚀 Key Features

* **Multi-Format Processing:** Seamlessly upload **PDF, DOCX, and TXT** files. The intelligent parser strips away "junk" data like page numbers and headers.
* **AI Translation:** Powered by `deep-translator` to break language barriers instantly.
* **High-Fidelity TTS:** Utilizes `gTTS` for natural-sounding intonation to reduce "listening fatigue."
* **Precision Speed Control:** Variable playback speeds from **0.5x to 3.0x** for deep-diving or skimming.
* **Offline Ready:** Integrated **Download Option** to save audio for any-time listening.

---

## 🛠️ Technical Stack

| Component | Technology | Use Case |
| :--- | :--- | :--- |
| **Language** | Python | Core logic and data processing |
| **UI Framework** | Streamlit | Interactive, responsive web interface |
| **Document Parsing** | PyPDF2 & python-docx | High-precision text extraction |
| **AI Engines** | gTTS & Deep-Translator | Speech synthesis and machine translation |
| **Memory Management** | io.BytesIO | RAM-efficient chunking for large-scale word counts |

---

## 🏗️ Architecture & Logic
To ensure **"Bulletproof Infrastructure"**, this application utilizes:
* **In-Memory Processing:** Uses the `io` module to handle conversion in RAM buffers, avoiding slow Disk I/O.
* **Stateless Execution:** Designed to be lightweight and easily deployable via Docker or Cloud platforms like AWS/Render.

---
