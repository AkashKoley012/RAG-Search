import streamlit as st
import requests
import uuid
import json
from datetime import datetime

# Streamlit page configuration
st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="wide")

# Load custom CSS
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'messages' not in st.session_state:
    # Interactive welcome message
    st.session_state.messages = [{
        "role": "assistant",
        "content": "<h3>👋 Welcome to the RAG Chatbot!</h3><p>I'm powered by DuckDuckGo Search and Google Gemini 1.5 Flash to provide concise, sourced answers. Try asking me something like 'What is AI?' or 'Tell me about space exploration'!</p>",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }]

# Page title and description
st.title("🌟 Web-Powered RAG Chatbot")
st.markdown("Chat with our AI powered by DuckDuckGo Search and Google Gemini 1.5 Flash. Ask anything and get concise, structured, sourced answers!")

# Clear chat button
if st.button("Clear Chat 🗑️"):
    st.session_state.messages = [{
        "role": "assistant",
        "content": "<h2>👋 Welcome to the RAG Chatbot!</h2><p>I'm powered by DuckDuckGo Search and Google Gemini 1.5 Flash to provide concise, sourced answers. Try asking me something like 'What is AI?' or 'Tell me about space exploration'!</p>",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }]
    st.session_state.session_id = str(uuid.uuid4())

# Chat container
chat_container = st.container()

# Input form at the bottom
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("Your Message:", placeholder="Type your question here...", key="user_input")
    submit_button = st.form_submit_button(label="Send 🚀")

# Handle query submission
if submit_button and user_input:
    with st.spinner("Thinking..."):
        try:
            # Add user message to chat history
            st.session_state.messages.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # Send query to backend
            response = requests.post(
                "http://localhost:5000/query",
                json={"query": user_input, "session_id": st.session_state.session_id}
            )
            response.raise_for_status()
            
            # Parse response content
            response_content = response.json()
            try:
                parsed = json.loads(response_content)
            except (TypeError, json.JSONDecodeError):
                parsed = response_content

            # Format structured output using h2, h3, p in ul, and source links
            title = parsed.get("title", "Untitled")
            sections = parsed.get("sections", [])

            formatted = f"<h2>{title}</h2>\n"
            for section in sections:
                formatted += f"<h3>{section['subtitle']}</h3>\n"
                formatted += "<ul>\n"
                for para in section['summary'].split(". "):
                    if para.strip():
                        formatted += f"<li><p>{para.strip()}.</p></li>\n"
                formatted += "</ul>\n"
                formatted += f'<p class="source-link"><a href="{section["source_url"]}" target="_blank">Source</a></p>\n'

            # Add assistant message with raw text for copying
            st.session_state.messages.append({
                "role": "assistant",
                "content": formatted,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "raw_text": sections[0]['summary'] if sections else "No summary available"
            })

        except requests.RequestException as e:
            st.error(f"Failed to connect to the backend. Please ensure the Flask server is running at http://localhost:5000. Error: {e}")
        except Exception as e:
            st.error(f"An error occurred while processing the response: {e}")

# Display chat history with auto-scroll
with chat_container:
    for idx, message in enumerate(st.session_state.messages):
        timestamp = message.get("timestamp", "")
        raw_text = message.get("raw_text", "")
        if message["role"] == "user":
            st.markdown(
                f"""
                <div class="chat-message user-message">
                    <div class="avatar user-avatar">👤</div>
                    <div class="message-wrapper">
                        <div class="message-content">{message['content']}</div>
                        <div class="timestamp">{timestamp}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            # Display assistant message with a copy button
            st.markdown(
                f"""
                <div class="chat-message assistant-message">
                    <div class="avatar assistant-avatar">🤖</div>
                    <div class="message-wrapper">
                        <div class="message-content typing">{message['content']}</div>
                        <div class="message-actions">
                            <div class="timestamp">{timestamp}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            # Add a Streamlit button to show text area for copying
            # if st.button("Copy 📋", key=f"copy_{idx}"):
            #     st.text_area("Copy the text below:", raw_text, height=100, key=f"copy_text_{idx}")
