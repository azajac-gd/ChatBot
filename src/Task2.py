import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Chatbot")
input_container = st.container()
chat_container = st.container()
clear_container = st.container()


if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    

with chat_container:
    for msg in st.session_state.messages[1:]:  
        st.chat_message(msg["role"]).write(msg["content"])


with input_container:
    st.title("ChatBot")

    with st.form("chat_form", clear_on_submit=True):
        col = st.columns([11,2])
        with col[0]:
            user_input = st.text_input("input_label", key="input", label_visibility="collapsed", placeholder="Type your message here...")
        with col[1]:
            submitted = st.form_submit_button("Send", icon=":material/send:", use_container_width=True)


    if submitted and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with chat_container:
            st.chat_message("user").write(user_input)

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=150        
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with chat_container:
            st.chat_message("assistant").write(reply)


with clear_container:
    col = st.columns([11, 5, 11])
    with col[0]:
        pass
    with col[1]:
        if st.button("Clear chat"):
            st.session_state.messages = [
                {"role": "system", "content": "You are a helpful assistant."}
            ]
            st.rerun()
    with col[2]:
        pass
