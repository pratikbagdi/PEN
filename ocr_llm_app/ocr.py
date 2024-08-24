import easyocr
import numpy as np
import streamlit as st  # Add this line to import Streamlit

@st.cache_resource  # Cache the OCR reader to improve performance
def get_ocr_reader(languages):
    return easyocr.Reader(languages)

def extract_text(image, languages):
    reader = get_ocr_reader(languages)
    image_np = np.array(image)
    results = reader.readtext(image_np, detail=0, paragraph=True)  # Extract text without bounding boxes
    return '\n'.join(results)