import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import easyocr
import numpy as np
import requests


# Function to improve image quality
def preprocess_image(image):
    image = image.convert('L')  # Convert to grayscale
    image = ImageOps.invert(image)  # Invert image to improve contrast
    image = image.filter(ImageFilter.MedianFilter())  # Apply median filter
    image = ImageOps.autocontrast(image)  # Apply autocontrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Increase contrast
    return image


# Function to extract text using EasyOCR
def extract_text(image, reader):
    image_np = np.array(image)
    results = reader.readtext(image_np, detail=0, paragraph=True)
    return '\n'.join(results)


# Function to correct text using Cohere API
# Function to correct text using Cohere API
def correct_text(text, lang_code):
    api_key = '5HXBCMonEmt9YhE03iPMVZcaUGRU6Hwv0bcyWFNf'
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}

    # Adjust the prompt to handle noisy input
    if lang_code == 'en':
        prompt = f"Correct the given text understanding the context: {text}"
    else:  # Use the same prompt for both Hindi and Marathi
        prompt = f"Correct the given text understanding the context without changing the original meaning: {text}"

    data = {
        "model": "command-nightly",
        "prompt": prompt,
        "max_tokens": 500,
        "temperature": 0.5,
        "k": 0,
        "p": 0.75,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "stop_sequences": [],
        "return_likelihoods": "NONE"
    }

    response = requests.post('https://api.cohere.ai/v1/generate', headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['generations'][0]['text'].strip()
    else:
        st.error("Error with the Cohere API: " + response.text)
        return text


# Streamlit app
st.title('Handwritten Text Extraction and Correction')

uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Language selection
    lang_choice = st.selectbox("Select the language for OCR and correction", ["English", "Hindi", "Marathi"])
    lang_code = 'en' if lang_choice == "English" else 'hi' if lang_choice == "Hindi" else 'mr'

    # Initialize the EasyOCR reader with the selected language
    reader = easyocr.Reader([lang_code])

    # Preprocess the image before extracting text
    processed_image = preprocess_image(image)

    st.write("Extracting text...")
    extracted_text = extract_text(processed_image, reader)
    extracted_text_area = st.text_area("Extracted Text", extracted_text, height=300)

    # Button to copy the extracted text to the clipboard
    if st.button("Copy Extracted Text"):
        st.markdown(f"""
            <script>
            function copyToClipboard(text) {{
                var dummy = document.createElement("textarea");
                document.body.appendChild(dummy);
                dummy.value = text;
                dummy.select();
                document.execCommand("copy");
                document.body.removeChild(dummy);
                alert("Extracted text copied to clipboard");
            }}
            copyToClipboard(`{extracted_text}`);
            </script>
        """, unsafe_allow_html=True)

    st.write("Correcting text using Cohere API...")
    corrected_text = correct_text(extracted_text, lang_code)
    corrected_text_area = st.text_area("Corrected Text", corrected_text, height=300)

    # Button to copy the corrected text to the clipboard
    if st.button("Copy Corrected Text"):
        st.markdown(f"""
            <script>
            function copyToClipboard(text) {{
                var dummy = document.createElement("textarea");
                document.body.appendChild(dummy);
                dummy.value = text;
                dummy.select();
                document.execCommand("copy");
                document.body.removeChild(dummy);
                alert("Corrected text copied to clipboard");
            }}
            copyToClipboard(`{corrected_text}`);
            </script>
        """, unsafe_allow_html=True)
