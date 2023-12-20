from function import *
import streamlit as st
from htmlTemplate import css, bot_template, user_template

def handle_user_input(user_question):
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    response = st.session_state.conversation({'question': user_question, 'chat_history': st.session_state.chat_history})
    st.session_state.chat_history = response['chat_history']
    
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.markdown(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.markdown(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="ChatBot with Multiple PDF", layout="wide", page_icon=":robot_face:")  # Set layout to wide
    st.write(css, unsafe_allow_html=True)

    # Improved sidebar layout
    with st.sidebar:
        st.title("ChatBot Settings 🛠️")
        pdf_docs = st.file_uploader("Upload PDF documents", accept_multiple_files=True)
        if st.button("Process or Reset Conversation 🔄"):
            with st.spinner("Processing..."):
                if pdf_docs:
                    # get pdf text
                    documents = read_multiple_pdf(pdf_docs)
                    # get the text chunks
                    chunks = chunk_docs(documents, chunk_size=500, chunk_overlap=50)
                    # create vector store
                    vector_db = embedding_chunks(chunks)
                    # create conversation chain
                    st.session_state.conversation = chain_conversation(vector_db)
                else:
                    st.warning("Please upload at least one PDF before processing.")

    # Improved main content layout
    st.title("ChatBot with Multiple PDF 🤖")
    st.markdown("---")

    user_question = st.text_input("Ask a question about your documents:", key="user_input_key", value="", disabled=not pdf_docs)
    if st.button("Ask 🤔") or user_question:
        if not pdf_docs:
            st.warning("Please upload PDFs and click 'Process' before asking questions.")
        else:
            handle_user_input(user_question)


if __name__ == "__main__":
    main()
