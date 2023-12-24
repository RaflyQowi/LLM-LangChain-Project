import streamlit as st
from PIL import Image
from function import bounding_box
from tempfile import NamedTemporaryFile
import os
from function import ImageCaptionTools, ObjectDetectionTool
from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferWindowMemory
from htmlTemplate import css, bot_template, user_template
import random

DIR = './temp'
if not os.path.exists(DIR):
    os.mkdir(DIR)

if "image_processed" not in st.session_state:
    DIR_PATH = os.path.join(DIR, str(random.randint(1,999999999)))
    st.session_state.dirpath = DIR_PATH
    if not os.path.exists(DIR_PATH):
        os.mkdir(DIR_PATH)

def delete_temp_files():
    for filename in os.listdir(st.session_state.dirpath):
        file_path = os.path.join(st.session_state.dirpath, filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)



# initialize Agent
def agent_init():
    tools = [ImageCaptionTools(), ObjectDetectionTool()]
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    memory = ConversationBufferWindowMemory(memory_key='chat_history',
                                            k=5,
                                            return_messages=True)
    agents = initialize_agent(
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        llm=llm,
        tools=tools,
        max_iterations=5,
        verbose=True,
        memory=memory
    )
    return agents



def main():
    st.set_page_config(
        page_title="Chat with an Image",
        page_icon="🖼️",
        layout="wide"
    )
    st.write(css, unsafe_allow_html=True)
    st.title("Chat with an Image 🖼️")
    agent = agent_init()

    # Check if the page has been reloaded
    if 'reloaded' not in st.session_state:
        st.session_state.reloaded = False
    else:
        st.session_state.reloaded = True

    if "image_processed" not in st.session_state:
        st.session_state.image_processed = None

    if "result_bounding" not in st.session_state:
        st.session_state.result_bounding = None

    # image_path = 'documentation\photo_1.jpg'

    col1, col2 = st.columns([1, 1])
    with col1:
        image_upload = st.file_uploader(label="Please Upload Your Image", type=['jpg', 'png', 'jpeg'])
        if not image_upload:
            st.warning("Please upload your image")
        else:
            st.image(
                image_upload,
                use_column_width=True
            )
        click_process = st.button("Process Image", disabled=not image_upload)
        if click_process:
            delete_temp_files()
            with NamedTemporaryFile(dir=st.session_state.dirpath, delete=False) as f:
                f.write(image_upload.getbuffer())
                st.session_state.image_path = f.name
                st.session_state.image_processed = True

        if (st.session_state.image_processed and st.session_state.result_bounding is None) or click_process:
            with st.spinner("Please Wait"):
                result_bounding = bounding_box(st.session_state.image_path)
                st.session_state.result_bounding = result_bounding

        # Expander to show/hide image
        if st.session_state.result_bounding is not None:
            with st.expander("Show Image (Bounding Box)"):
                st.image(st.session_state.result_bounding)

    with col2:
        user_question = st.text_area("Ask About your image",
                                     disabled=not st.session_state.image_processed,
                                     max_chars=150)
        click_ask = st.button("Ask Question", disabled=not st.session_state.image_processed)
        if click_ask:
            st.write(user_template.replace("{{MSG}}", user_question), unsafe_allow_html=True)
            with st.spinner("Doraemon Searching for Answer🔎"):
                chat_history = agent.invoke({"input": f"{user_question}, this is the image path: {st.session_state.image_path}"})
                response = chat_history['output']
                st.write(bot_template.replace("{{MSG}}", response), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
