import streamlit as st
import time 
import PyPDF2
import io
import docx 
from gtts import gTTS
import os
from deep_translator import GoogleTranslator
import glob

st.title("Audio Book App")
st.subheader("Convert your documents to speech in multiple languages!")

# 1. Language Selection (Local to this page so it disappears on 'About')
st.sidebar.header("Voice Settings")



# if st.sidebar.button("🗑️ Clear Audio Cache"):
#     files = glob.glob("Audio_Voice_*.mp3")
#     # deleted_count = len(files)
#     for f in files:
#         os.remove(f)
#     st.sidebar.success(f"🧹 Cleanup complete: {len(files)} old audio files deleted.")
#     # st.sidebar.success(f"Deleted {len(files)} files!")
#     # 4. Wait for 5 seconds
#     time.sleep(5)



lang_options = {
    # --- Indian Regional Languages ---
    "Bengali": {"lang": "bn", "tld": "com"},
    "Gujarati": {"lang": "gu", "tld": "com"},
    "Hindi": {"lang": "hi", "tld": "com"},
    "Kannada": {"lang": "kn", "tld": "com"},
    "Kashmiri": {"lang": "ks", "tld": "com"},
    "Konkani": {"lang": "kok", "tld": "com"},
    "Maithili": {"lang": "mai", "tld": "com"},
    "Malayalam": {"lang": "ml", "tld": "com"},
    "Manipuri": {"lang": "mni", "tld": "com"},
    "Marathi": {"lang": "mr", "tld": "com"},
    "Nepali": {"lang": "ne", "tld": "com"},
    "Odia": {"lang": "or", "tld": "com"},
    "Punjabi": {"lang": "pa", "tld": "com"},
    "Sanskrit": {"lang": "sa", "tld": "com"},
    "Santali": {"lang": "sat", "tld": "com"},
    "Sindhi": {"lang": "sd", "tld": "com"},
    "Tamil": {"lang": "ta", "tld": "com"},
    "Telugu": {"lang": "te", "tld": "com"},
    "Urdu": {"lang": "ur", "tld": "com"},

    # --- Major International Languages ---
    "English (US)": {"lang": "en", "tld": "com"},
    "English (UK)": {"lang": "en", "tld": "co.uk"},
    "English (India)": {"lang": "en", "tld": "co.in"},
    "English (Australia)": {"lang": "en", "tld": "com.au"},
    "French (France)": {"lang": "fr", "tld": "fr"},
    "French (Canada)": {"lang": "fr", "tld": "ca"},
    "German": {"lang": "de", "tld": "de"},
    "Spanish (Spain)": {"lang": "es", "tld": "es"},
    "Spanish (Mexico)": {"lang": "es", "tld": "com.mx"},
    "Portuguese (Brazil)": {"lang": "pt", "tld": "com.br"},
    "Portuguese (Portugal)": {"lang": "pt", "tld": "pt"},
    "Chinese (Mandarin)": {"lang": "zh-CN", "tld": "com"},
    "Japanese": {"lang": "ja", "tld": "co.jp"},
    "Korean": {"lang": "ko", "tld": "co.kr"},
    "Russian": {"lang": "ru", "tld": "ru"},
    "Arabic": {"lang": "ar", "tld": "com"},
    "Italian": {"lang": "it", "tld": "it"},
    "Turkish": {"lang": "tr", "tld": "com.tr"},
    "Vietnamese": {"lang": "vi", "tld": "com"},
    "Thai": {"lang": "th", "tld": "com"}
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
            st.error("No readable text found in the file!")
            return

        # Show the text to the user
        st.text_area("Extracted Text Content", text_to_convert, height=300)

        with st.spinner(f"Converting to {choice} voice..."):
            # Generate Speech - Using the selected language and TLD
            speech = gTTS(text=text_to_convert[:5000], lang=selected_lang, slow=False, tld=selected_tld)
            
            # Use a unique filename using timestamp to avoid 'File in use' errors
            audio_file = f"Audio_Voice_{int(time.time())}.mp3"
            speech.save(audio_file)
            
            # Play Audio
            st.audio(audio_file)
            st.success("Conversion successful!")

            # Add Download Button
            with open(audio_file, "rb") as f:
                st.download_button(
                    label="📥 Download Audio File",
                    data=f,
                    file_name="my_audiobook.mp3",
                    mime="audio/mpeg",
                    type="primary"
                )
            # if st.download_button:
            #       files = glob.glob("Audio_Voice_*.mp3")
            #       # deleted_count = len(files)
            #       for f in files:
            #           os.remove(f)
            #       time.sleep(5)
            #       st.sidebar.success(f"🧹 Cleanup complete: {len(files)} old audio files deleted.")
            #       # st.sidebar.success(f"Deleted {len(files)} files!")
            #       # 4. Wait for 5 seconds

    except Exception as e:
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
                        # We limit to 4500 chars because translation APIs have limits
                        # 'source=auto' detects if you uploaded English, Hindi, etc.
                        translator = GoogleTranslator(source='auto', target=selected_lang)
                        extracted_text = translator.translate(extracted_text[:4500])
                        st.success("Translation successful!")
                    except Exception as e:
                        st.error(f"Translation Error: {e}")

            # Now send the TEXT (string) to the processing function
            process_and_play(extracted_text)

        except Exception as e:
            st.error(f"Error reading file: {e}")