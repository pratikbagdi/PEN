# gui.py
import streamlit as st
from PIL import Image
from preprocessing import preprocess_image
from ocr import extract_text
from llm_integration import correct_text
from chatbot import start_chatbot

def show_gui():
    # Inject custom CSS
    st.markdown("""
        <style>
        .css-18e3th9 {
            padding-top: 2rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 1rem;
        }
        .css-1d391kg {
            font-size: 18px;
            font-weight: bold;
            color: #6C63FF;
        }
        .stButton>button {
            background-color: #6C63FF;
            color: white;
            border-radius: 5px;
        }
        .stTextInput>div>input {
            border: 2px solid #6C63FF;
        }
        </style>
        """, unsafe_allow_html=True)

    uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    ocr_language = st.selectbox("Select OCR Language", options=["en", "hi", "mr"])
    llm_language = st.selectbox("Select LLM Correction Language", options=["English", "Hindi", "Marathi"])

    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        processed_image = preprocess_image(image)

        st.write("Extracting text...")
        extracted_text = extract_text(processed_image, [ocr_language])
        extracted_text_area = st.text_area("Extracted Text", extracted_text, height=150)

        st.write("Correcting text using Cohere API...")
        corrected_text = correct_text(extracted_text, llm_language)
        corrected_text_area = st.text_area("Corrected Text", corrected_text, height=150)

        if st.button("Copy Corrected Text"):
            st.write("Corrected text copied to clipboard.")
            st.code(corrected_text, language='')

        st.write("## Chat with Corrected Text")
        start_chatbot(corrected_text, llm_language)
