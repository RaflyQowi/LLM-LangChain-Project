from function import scraping_pipeline
import os
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from dotenv import load_dotenv
import pickle
from htmlTemplate import css, bot_template, user_template

load_dotenv()

def data_pipeline(urls):
    documents = scraping_pipeline(urls)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 50
    )
    chunks_text = text_splitter.split_documents(documents)
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_stores = FAISS.from_documents(chunks_text, embeddings)
    return vector_stores


def main():
    
    st.set_page_config(
        page_title= "News Article QnA using LLM",
        page_icon= "🌏",
        layout="wide"
    )

    st.write(css, unsafe_allow_html=True)

    st.title('News Article QnA using LLM 📰')
    # process_links = False
    # file_name = "faiss_store_openai.pkl"  # Provide a filename
    # file_path = os.path.join("vectordb", file_name)  # Join the directory and filename

    # if not os.path.exists("vectordb"):
    #     os.makedirs("vectordb")

    if 'vector_stores' not in st.session_state:
        st.session_state.vector_stores = None

    llm = ChatGoogleGenerativeAI(model="gemini-pro",
                                 temperature=0.8)

    with st.sidebar:
        st.subheader("Input Indonesian News Article Link🔗")
        num_link = st.number_input(
            'How many article you want to input', 
            min_value= 0,
            max_value= 5,
            value = 1
        )
        urls = []
        for i in range(1,num_link+1):
            url = st.text_input(f"Indonesian News Article [CNN, Kompas, Detik] No {i}")
            urls.append(url)
        
        process_links = False
        if "" not in urls:
            process_links = st.button("Process URL")

    if process_links:
        with st.spinner("Processing..."):
            st.session_state.vector_stores = data_pipeline(urls)
            
            # # Save the FAISS index to a pickle file
            # with open(file_path, "wb") as f:
            #     pickle.dump(vector_stores_gemini, f)
            st.success("Data has been process", icon="✅")
        
            
    user_question = st.chat_input("Ask a question about your documents")
    
    if user_question:
        with st.spinner("Doraemon Searching for Answer🔎"):
            st.write(user_template.replace("{{MSG}}",user_question), unsafe_allow_html= True)
            # if os.path.exists(file_path):
            #     with open(file_path, 'rb') as f:
            #         vector_stores = pickle.load(f)

            vector_stores = st.session_state.vector_stores
            
            chain = RetrievalQAWithSourcesChain.from_chain_type(
                llm = llm,
                retriever = vector_stores.as_retriever(),
                chain_type= 'map_reduce'
            )
            result = chain(
                {"question": user_question},
                return_only_outputs= True
            )
            # result will be a dictionary of this format --> {"answer": "", "sources": [] }
            # Display sources, if available
            sources = result.get("sources", "")
            if sources:
                response = f"{result['answer']} \n\nsource: {sources}"
                st.write(bot_template.replace("{{MSG}}",response), unsafe_allow_html= True)
            else:
                response = str(result['answer']).strip()
                st.write(bot_template.replace("{{MSG}}",response), unsafe_allow_html= True)
 
if __name__ == '__main__':
    main()