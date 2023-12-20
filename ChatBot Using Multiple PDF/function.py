from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import HuggingFaceHub
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

load_dotenv()

## Read Multiple PDF files
def read_multiple_pdf(files):
    if type(files) == str:
        files = list("document\yolo.pdf".split(" "))
    texts = ""
    for file in files:
        docs = PdfReader(file)
        for text in docs.pages:
            texts += (text.extract_text())
        return texts
    

## Split PDF into chunks
def chunk_docs(document, chunk_size = 500, chunk_overlap = 50, separators="\n"):
    """
    Split a document into smaller chunks of text.

    Args:
        document (str): The document to be chunked.
        chunk_size (int, optional): The size of each chunk in characters. Defaults to 500.
        chunk_overlap (int, optional): The overlap between adjacent chunks in characters. Defaults to 50.
        separators (str, optional): The separators used to split the document into chunks. Defaults to "\\n".

    Returns:
        str: The chunked document.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        separators=separators,
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap
    )
    chunk = text_splitter.split_text(document)
    return chunk

## Embeds the Data
def embedding_chunks(chunk, model_name = "sentence-transformers/all-MiniLM-L12-v2"):
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    vector_stores = FAISS.from_texts(chunk, embeddings)
    return vector_stores


## setup conversational chain
def chain_conversation(vector_stores,config = {'max_new_tokens': 256, 'temperature': 0.1},model_repo = "mistralai/Mixtral-8x7B-Instruct-v0.1"):
    llm = HuggingFaceHub(repo_id = model_repo, model_kwargs = config)
    memory = ConversationBufferMemory(memory_key= "chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(llm= llm, 
                                                               retriever= vector_stores.as_retriever(search_kwargs={"k": 10}),
                                                               memory= memory)
    return conversation_chain