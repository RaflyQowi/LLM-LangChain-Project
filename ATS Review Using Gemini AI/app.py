import streamlit as st
from prompt import PROMPT_RESUME_ABOUT, PROMPT_ACCEPTANCE_PERCENTAGE, PROMPT_SKILL_IMPROVEMENTS
from utils import *


def main():
    st.set_page_config(
        page_title="Resume (ATS) Review Using Gemini AI",
        page_icon="📋",
        layout="wide"
    )

    # st.write(css, unsafe_allow_html=True)
    st.title("Resume (ATS) Review Using Gemini AI 📋")

    col1, col2 = st.columns([1, 3])
    
    with col1:
        uploaded_file = st.file_uploader("Please Upload your Resume", type=["pdf"])

        if uploaded_file is None:
            st.warning("Please upload your image")
        else:
            st.success("PDF Uploaded Successfully")

        submit1 = st.button("Tell Me About the Resume")

        submit2 = st.button("How can I Improvise my Skills")

        submit3 = st.button("Percentage match")

    with col2:
        input_text = st.text_area("Job Description:", key= "input")
        with st.spinner('Wait for it...'):
            if submit1:
                if uploaded_file is not None:
                    pdf_content = input_pdf_setup(uploaded_file)
                    response = get_gemini_response(PROMPT_RESUME_ABOUT, pdf_content, input_text)
                    st.subheader("Resume Evaluation:")
                    st.write(response)
            elif submit2:
                if uploaded_file is not None:
                    pdf_content = input_pdf_setup(uploaded_file)
                    response = get_gemini_response(PROMPT_SKILL_IMPROVEMENTS, pdf_content, input_text)
                    st.subheader("Skill Improvement Recommendations:")
                    st.write(response)
            elif submit3:
                if uploaded_file is not None:
                    pdf_content = input_pdf_setup(uploaded_file)
                    response = get_gemini_response(PROMPT_ACCEPTANCE_PERCENTAGE, pdf_content, input_text)
                    st.subheader("ATS System Evaluation:")
                    st.write(response)
            st.success('Done!')

if __name__ == "__main__":
    main()
