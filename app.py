import streamlit as st
from chatbot_logic import qa_chain

st.title("Company Doc Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question about the documentation..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = qa_chain.invoke({"query": prompt})
        st.markdown(response["result"])
        if "source_documents" in response:
            st.write("\nSources:")
            for doc in response["source_documents"]:
                st.write(f"- {doc.metadata.get('source', 'Unknown source')}") # Assuming 'source' metadata
        st.session_state.messages.append({"role": "assistant", "content": response["result"]})
