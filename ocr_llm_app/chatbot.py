# chatbot.py
import requests
import streamlit as st

def get_cohere_response(corrected_text, user_input, language):
    api_key = '5HXBCMonEmt9YhE03iPMVZcaUGRU6Hwv0bcyWFNf'
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    data = {
        "model": "command-nightly",
        "prompt": f"The following text is a corrected version of a handwritten document:\n\n{corrected_text}\n\n"
                  f"Based on the above text, {language} answer the following question: {user_input}",
        "max_tokens": 150,
        "temperature": 0.7,
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
        return "Sorry, I couldn't process your request at the moment."

def start_chatbot(corrected_text, language):
    st.write("### Chatbot")
    user_input = st.text_input("Ask anything about the corrected text:")

    if st.button("Submit"):
        if user_input:
            with st.spinner("Generating response..."):
                response = get_cohere_response(corrected_text, user_input, language)
            st.write(f"**You:** {user_input}")
            st.write(f"**Bot:** {response}")
        else:
            st.error("Please enter a question.")
