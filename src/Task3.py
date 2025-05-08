import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Chatbot")

#Layout
title_container = st.container(border=False)
chat_container = st.container(height=400, border=False)
input_container = st.container()
clear_container = st.container()


if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

#Title    
with title_container:
    st.title("ChatBot")


#Chat container
with chat_container:  
    for msg in st.session_state.messages[1:]:  
        st.chat_message(msg["role"]).write(msg["content"])


#Input container
with input_container:
    with st.form("chat_form", clear_on_submit=True):
        col = st.columns([11,2]) #Layout
        with col[0]:
            user_input = st.text_input("input_label", key="input", label_visibility="collapsed", placeholder="Type your message here...")
        with col[1]:
            submitted = st.form_submit_button("Send", icon=":material/send:", use_container_width=True)

    if submitted and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with chat_container:
            st.chat_message("user").write(user_input)
            assistant_message = st.chat_message("assistant").empty()

            full_reply = ""
            stream = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=150,
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content: #Checking if content is not None
                    token = chunk.choices[0].delta.content
                    full_reply += token
                    assistant_message.write(full_reply)  

            assistant_message.write(full_reply)
            st.session_state.messages.append({"role": "assistant", "content": full_reply})


#Clear chat container
with clear_container:
    col = st.columns([11, 5, 11]) #Layout
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
