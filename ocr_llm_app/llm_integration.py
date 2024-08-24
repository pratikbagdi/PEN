import requests
import streamlit as st

def correct_text(text, language):
    api_key = '5HXBCMonEmt9YhE03iPMVZcaUGRU6Hwv0bcyWFNf'
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}

    if language == 'English':
        prompt = f"Correct the given text understanding the context for spelling and grammar: {text}"
        tokens = 300
    else:  # For Hindi and Marathi, use a similar prompt with the correct language focus
        prompt = f"Correct the following text for spelling and grammar without changing the original meaning or structure: {text}"
        tokens = 600

    data = {
        "model": "command-nightly",
        "prompt": prompt,
        "max_tokens": tokens,  # Adjusted to keep response concise
        "temperature": 0.5,
        "k": 0,
        "p": 0.75,  # More deterministic results
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
