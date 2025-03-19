import streamlit as st
from translate import Translator
from gtts import gTTS
import os
from docx2python import docx2python  # Changed from python-docx to docx2python
import pypdf
from io import BytesIO
import pyperclip  # Add pyperclip for clipboard functionality
from PIL import Image
import numpy as np
import easyocr
import speech_recognition as sr

# Initialize session state for persistent storage
if 'text' not in st.session_state:
    st.session_state.text = ""
if 'translation' not in st.session_state:
    st.session_state.translation = ""
if 'voice_text' not in st.session_state:
    st.session_state.voice_text = ""
if 'voice_captured' not in st.session_state:
    st.session_state.voice_captured = False
if 'target_lang' not in st.session_state:
    st.session_state.target_lang = "en"

# Define languages dictionary at the top level
languages = {
    "Auto Detect": "auto",
    "English": "en", 
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh",
    "Japanese": "ja",
    "Korean": "ko",
    "Hindi": "hi",
    "Arabic": "ar",
    "Russian": "ru",
    "Urdu": "ur",
    "Punjabi": "pa",
    "Bengali": "bn",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Pashto": "ps",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Odia": "or",
    "Assamese": "as",
    "Bhojpuri": "bh",
}

# Custom CSS for glassmorphism effect and colorful design
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://img.freepik.com/free-vector/realistic-glass-effect-background_52683-74487.jpg?ga=GA1.1.690664293.1741270361&semt=ais_');
        background-size: cover;
        background-position: center;
    }
    .main-container {
        background: rgba(21, 14, 14, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.8);
        color: #333;
        border-radius: 10px;
    }
    .stButton button {
        background-color: rgb(7, 80, 10);
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .stSelectbox div {
        background-color: rgba(255, 255, 255, 0.8);
        color: #333;
        border-radius: 10px;
    }
    .stSuccess {
        color: #28a745;
        font-size: 18px;
    }
    .stWarning {
        color: #ffc107;
        font-size: 18px;
    }
    .stError {
        color: rgb(173, 18, 34);
        font-size: 18px;
    }
    .translation-box {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌍 All-in-One Translator")

# Add tabs for different input methods
tab1, tab2, tab3, tab4 = st.tabs(["Text", "Voice", "Document Upload", "Image"])

with tab1:
    # Text translation
    st.session_state.text = st.text_area("Enter text to translate:", "Hello, how are you?", height=130)

with tab2:
    # Voice input
    st.write("Voice Translation Instructions:")
    st.write("1. Click the 'Record Voice' button and speak")
    st.write("2. Your speech will be converted to text")
    st.write("3. The text will be ready for translation")

    if st.button("🎤 Record Voice"):
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                st.info("Listening... Speak now")
                audio = r.listen(source)
                voice_text = r.recognize_google(audio)
                st.session_state.voice_text = voice_text
                st.session_state.text = voice_text
                st.session_state.voice_captured = True
                st.success("✅ Voice captured successfully!")
                st.write("Captured text:", voice_text)
        except Exception as e:
            st.error(f"❌ Error recording voice: {str(e)}")
            st.info("💡 Tip: Make sure your microphone is working and speak clearly")

    # Show captured text persistently
    if st.session_state.voice_captured and st.session_state.voice_text:
        st.write("Current voice text:", st.session_state.voice_text)
        
        # Add language selection and translation button for voice
        st.markdown("### 🎯 Select Languages for Voice Translation")
        col1, col2 = st.columns(2)
        with col1:
            voice_source_lang = st.selectbox("Voice Source language:", list(languages.keys()), key="voice_source")
        with col2:
            voice_target_lang = st.selectbox("Voice Target language:", list(languages.keys()), key="voice_target")
            st.session_state.target_lang = languages[voice_target_lang]

        if st.button("🚀 Translate Voice Text"):
            try:
                translator = Translator(from_lang=languages[voice_source_lang], to_lang=languages[voice_target_lang])
                voice_translation = translator.translate(st.session_state.voice_text)
                st.session_state.translation = voice_translation
                st.success("✅ Voice Translation:")
                st.markdown(
                    f'<div class="translation-box"><strong>{voice_translation}</strong></div>',
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.error(f"❌ Translation error: {str(e)}")

with tab3:
    # Document upload
    uploaded_file = st.file_uploader("Upload Document (PDF/DOCX)", type=['pdf', 'docx'])
    if uploaded_file:
        try:
            if uploaded_file.type == "application/pdf":
                pdf_reader = pypdf.PdfReader(uploaded_file)
                st.session_state.text = ""
                for page in pdf_reader.pages:
                    st.session_state.text += page.extract_text()
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = docx2python(uploaded_file)
                st.session_state.text = doc.text
            st.write("Extracted text:", st.session_state.text)
        except Exception as e:
            st.error(f"Error processing document: {str(e)}")

with tab4:
    # Image translation
    st.write("Image Translation Instructions:")
    st.write("1. Upload an image containing text or take a photo")
    st.write("2. The system will extract text from the image")
    st.write("3. The extracted text will be ready for translation")

    image_source = st.radio("Choose image source:", ["Upload Image", "Take Photo"])
    
    if image_source == "Upload Image":
        uploaded_image = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])
        if uploaded_image:
            image_for_ocr = uploaded_image
    else:
        camera_image = st.camera_input("Take a photo of text")
        if camera_image:
            image_for_ocr = camera_image

    if 'image_for_ocr' in locals() and image_for_ocr is not None:
        try:
            # Display progress
            progress_bar = st.progress(0)
            st.info("Processing image...")

            # Convert image to PIL Image
            image = Image.open(image_for_ocr)
            
            # Initialize EasyOCR reader
            reader = easyocr.Reader(['en'])  # Initialize for English
            
            # Update progress
            progress_bar.progress(30)
            st.info("Extracting text from image...")
            
            # Convert PIL Image to numpy array
            image_np = np.array(image)
            
            # Perform OCR
            results = reader.readtext(image_np)
            
            # Update progress
            progress_bar.progress(70)
            
            # Extract text from results
            extracted_text = " ".join([text[1] for text in results])
            
            if extracted_text.strip():
                st.session_state.text = extracted_text
                st.success("✅ Text extracted successfully!")
                st.write("Extracted text:", extracted_text)
            else:
                st.warning("⚠️ No text detected in image. Please try with a clearer image.")
            
            # Complete progress
            progress_bar.progress(100)
            
        except Exception as e:
            st.error(f"❌ Error processing image: {str(e)}")
            st.info("💡 Tip: Make sure the image is clear and text is readable")

# Language selection for text and document
if st.session_state.text and not st.session_state.voice_captured:
    st.markdown("### 🎯 Select Source and Target Languages")

    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox("Source language:", list(languages.keys()))
    with col2:
        target_lang = st.selectbox("Target language:", list(languages.keys()))
        st.session_state.target_lang = languages[target_lang]

    # Translation
    if st.button("🚀 Translate"):
        try:
            # Split text into chunks of 500 characters
            text_chunks = [st.session_state.text[i:i+500] for i in range(0, len(st.session_state.text), 500)]
            translator = Translator(from_lang=languages[source_lang], to_lang=languages[target_lang])
            
            # Translate each chunk and combine
            translated_chunks = []
            for chunk in text_chunks:
                translated_chunk = translator.translate(chunk)
                translated_chunks.append(translated_chunk)
            
            st.session_state.translation = ' '.join(translated_chunks) 
            st.success("✅ Translation:")
            st.markdown(
                f'<div class="translation-box"><strong>{st.session_state.translation}</strong></div>',
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.error(f"❌ Translation error: {str(e)}")

# Text-to-Speech
if st.session_state.translation:
    if st.button("🔊 Listen to Translation"):
        try:
            tts = gTTS(text=st.session_state.translation, lang=st.session_state.target_lang)
            audio_file = BytesIO()
            tts.write_to_fp(audio_file)
            audio_file.seek(0)
            st.audio(audio_file)
        except Exception as e:
            st.error(f"❌ Text-to-speech error: {str(e)}")

# Additional features
st.markdown("### 📝 Additional Features")
col3, col4 = st.columns(2)
with col3:
    if st.button("📋 Copy to Clipboard"):
        if st.session_state.translation:
            try:
                pyperclip.copy(st.session_state.translation)
                st.success("Translation copied to clipboard!")
            except Exception as e:
                st.error("Could not copy to clipboard. Please try again.")

with col4:
    if st.button("💾 Save Translation"):
        if st.session_state.translation:
            try:
                st.download_button(
                    label="Download translation",
                    data=st.session_state.translation,
                    file_name="translation.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error("Could not save translation. Please try again.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Zakia Bashir")
st.markdown('</div>', unsafe_allow_html=True)
