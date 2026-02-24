import streamlit as st

st.title("🎧 About Audio Book App")

st.markdown("""
### Turn your documents into speech!
This application uses Advanced Text-to-Speech technology to help you listen to your documents on the go. 
Whether you are commuting, exercising, or just prefer listening over reading, we've got you covered.

---

### 🚀 Features:
* **Multi-Format Support:** Upload PDF, Word (.docx), or Text (.txt) files.
* **Global Voices:** Choose from various accents including US, UK, Indian English, Hindi, Spanish, and more.
* **Downloadable Audio:** Save your generated audio as an MP3 file to listen later.

---

### 📖 How to use:
1. **Navigate to the Home page.**
2. **Select your preferred language** from the sidebar.
3. **Upload your document** (Ensure it contains selectable text, not just images).
4. **Click 'Generate Audio'** and wait for the magic to happen!
5. **Listen** directly in the app or **Download** the file.

---

### ⚠️ Important Note:
Currently, the app processes the first **5,000 characters** of your document to ensure fast conversion. Please ensure your PDF is not "scanned" (image-only), as the app requires actual text to read.
            """)

st.info("Built with ❤️ using Streamlit and gTTS")
