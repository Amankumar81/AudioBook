import streamlit as st
import time 
import PyPDF2
import io
import docx 
from gtts import gTTS
import os
from deep_translator import GoogleTranslator

st.title("Audio Book App")
st.subheader("Convert your documents to speech in multiple languages!")

# 1. Language Selection (Local to this page so it disappears on 'About')
st.sidebar.header("Voice Settings")

lang_options = {
   "Arabic": {"lang": "ar", "tld": "com"},
    "Bengali": {"lang": "bn", "tld": "com"},
    "Chinese (Mandarin)": {"lang": "zh-CN", "tld": "com"},
    "Czech": {"lang": "cs", "tld": "cz"},
    "Danish": {"lang": "da", "tld": "dk"},
    "Dutch": {"lang": "nl", "tld": "nl"},
    "English (Australia)": {"lang": "en", "tld": "com.au"},
    "English (India)": {"lang": "en", "tld": "co.in"},
    "English (UK)": {"lang": "en", "tld": "co.uk"},
    "English (US)": {"lang": "en", "tld": "com"},
    "Finnish": {"lang": "fi", "tld": "fi"},
    "French (Canada)": {"lang": "fr", "tld": "ca"},
    "French (France)": {"lang": "fr", "tld": "fr"},
    "German": {"lang": "de", "tld": "de"},
    "Greek": {"lang": "el", "tld": "gr"},
    "Gujarati": {"lang": "gu", "tld": "com"},
    "Hindi": {"lang": "hi", "tld": "com"},
    "Hungarian": {"lang": "hu", "tld": "hu"},
    "Indonesian": {"lang": "id", "tld": "co.id"},
    "Italian": {"lang": "it", "tld": "it"},
    "Japanese": {"lang": "ja", "tld": "co.jp"},
    "Kannada": {"lang": "kn", "tld": "com"},
    "Konkani": {"lang": "kok", "tld": "com"},
    "Korean": {"lang": "ko", "tld": "co.kr"},
    "Marathi": {"lang": "mr", "tld": "com"},
    "Nepali": {"lang": "ne", "tld": "com"},
    "Norwegian": {"lang": "no", "tld": "no"},
    "Polish": {"lang": "pl", "tld": "pl"},
    "Portuguese (Brazil)": {"lang": "pt", "tld": "com.br"},
    "Portuguese (Portugal)": {"lang": "pt", "tld": "pt"},
    "Punjabi": {"lang": "pa", "tld": "com"},
    "Romanian": {"lang": "ro", "tld": "ro"},
    "Russian": {"lang": "ru", "tld": "ru"},
    "Spanish (Mexico)": {"lang": "es", "tld": "com.mx"},
    "Spanish (Spain)": {"lang": "es", "tld": "es"},
    "Swedish": {"lang": "sv", "tld": "se"},
    "Tamil": {"lang": "ta", "tld": "com"},
    "Telugu": {"lang": "te", "tld": "com"},
    "Thai": {"lang": "th", "tld": "com"},
    "Turkish": {"lang": "tr", "tld": "com.tr"},
    "Urdu": {"lang": "ur", "tld": "com"},
    "Vietnamese": {"lang": "vi", "tld": "com"}
}
choice = st.sidebar.selectbox("Select Language/Accent", list(lang_options.keys()))
selected_lang = lang_options[choice]["lang"]
selected_tld = lang_options[choice]["tld"]

file = st.file_uploader(label="Upload your file here", type=['pdf', 'docx', 'txt'])
if file is not None: 
   if file.type == "application/pdf":
       st.success("Your PDF file is uploaded")
   elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
       st.success("Your WORD file is uploaded")
   elif file.type == "text/plain":
       st.success("Your TEXT file is uploaded")

def process_and_play(text_to_convert):
    try:
        if not text_to_convert.strip():
            st.error("No readable text found!")
            return
        
        st.text_area("Extracted Text Content", text_to_convert, height=400)

        with st.spinner(f"Converting to {choice} voice..."):
            # 1. Chunking for gTTS (Google GTTS also has limits per request)
            audio_chunk_size = 4000 
            text_chunks = [text_to_convert[i:i + audio_chunk_size] for i in range(0, len(text_to_convert), audio_chunk_size)]
            
            final_audio = io.BytesIO()
            
            # 2. Loop through chunks and write them into the same memory buffer
            for chunk in text_chunks:
                tts = gTTS(text=chunk, lang=selected_lang, tld=selected_tld)
                tts.write_to_fp(final_audio)
                time.sleep(1)
            
            final_audio.seek(0)
            
            # 3. Output
            st.audio(final_audio)
            st.success("Conversion successful!.")

            st.download_button(
                label="📥 Download Audiobook",
                data=final_audio,
                file_name="Audio_book.mp3",
                mime="audio/mpeg")
    except Exception as e:
        if "429" in str(e):
            st.error("Rate Limit Hit (429): Google is blocking requests. Please wait 2 minutes before trying again.")
        else:
            st.error(f"Error during audio generation: {e}")

if file:

    button = st.button("Generate Audio", type="primary")
    
    if button:
        extracted_text = ""
        try:
            # 1. PDF Logic
            if file.type == "application/pdf":
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.getvalue()))
                for page in pdf_reader.pages:
                    content = page.extract_text()
                    if content:
                        extracted_text += content + "\n"
            
            # 2. DOCX Logic
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = docx.Document(io.BytesIO(file.getvalue()))
                extracted_text = "\n".join([para.text for para in doc.paragraphs])
            
            # 3. TXT Logic
            elif file.type == "text/plain":
                extracted_text = file.getvalue().decode("utf-8")

            if extracted_text.strip():
               with st.spinner(f"Translating text to {choice}..."):
                   try:
                       translator = GoogleTranslator(source='auto', target=selected_lang)
                       
                       # 1. Define chunk size (4000 characters is safe)
                       chunk_size = 4000
                       # 2. Split the text into a list of chunks
                       chunks = [extracted_text[i:i + chunk_size] for i in range(0, len(extracted_text), chunk_size)]
                       
                       translated_chunks = []
                       
                       # 3. Create a progress bar for long documents
                       progress_bar = st.progress(0)
                       for index, chunk in enumerate(chunks):
                           translated_chunks.append(translator.translate(chunk))
                           # Update progress
                           progress_bar.progress((index + 1) / len(chunks))
                           time.sleep(1)
                       
                       # 4. Join all translated parts back into one string
                       extracted_text = " ".join(translated_chunks)
                       
                       st.success(f"Translation successful!")
                       
                   except Exception as e:
                       st.error(f"Translation Error: {e}")

            # Now send the TEXT (string) to the processing function
            process_and_play(extracted_text)

        except Exception as e:
            st.error(f"Error reading file: {e}")