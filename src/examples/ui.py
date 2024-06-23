import streamlit as st
import datetime

def get_bot_response(user_message):
    return f"Echo back: {user_message}"

# Sidebar
with st.sidebar:
    st.title("AI Settings")
    ready = True;
    if ready:
        st.success("Model is ready to chat!")
    else:
        st.warning("Model is not ready to chat!")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.header("Chat Settings")
    st.slider("Temperature", 0.0, 1.0, 0.5, 0.1)
    st.slider("Top P", 0.0, 1.0, 0.9, 0.1)
    st.slider("Frequency Penalty", 0.0, 2.0, 1.0, 0.1)
    st.slider("Top K", 1, 100, 50, 1)

# Main app
st.header("ArchNetAI NetNode Chat")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate response using the get_bot_response function
    response = get_bot_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()