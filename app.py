import streamlit as st
from chatbot_logic import qa_chain

st.set_page_config(page_title="Company Doc Chatbot", page_icon="🤖")

st.title("🤖 Company Doc Chatbot")

with st.sidebar:
    st.header("Controls")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question about the documentation..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            response = qa_chain.invoke({"query": prompt})
            result = response.get("result", "I am sorry, I could not find an answer.")
            message_placeholder.markdown(result)

            if "source_documents" in response:
                with st.expander("Sources"):
                    for doc in response["source_documents"]:
                        source = doc.metadata.get('source', 'Unknown source')
                        st.write(f"- {source}")
            
            # Store the full response including sources for history
            st.session_state.messages.append({"role": "assistant", "content": result, "sources": response.get("source_documents")})
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.session_state.messages.append({"role": "assistant", "content": "Sorry, I ran into an issue while processing your request."})
