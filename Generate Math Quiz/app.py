import streamlit as st
from function import GetLLMResponse
import pandas as pd

# List of math topics and difficulty levels
math_topics = {
    "Elementary School Level": ["Basic Arithmetic", "Place Value", "Fraction", "Decimals", "Geomerty"],
    "Middle School Level": ["Algebra", "Ratio and Proportion", "Percentages", "Geometry", "Integers and Rational Numbers"],
    "High School Level": ["Algebra II", "Trigonometry", "Pre-Calculus", "Calculus", "Statistics and Probability"]
}

# Page configuration
st.set_page_config(page_title="Generate Math Quizzes",
                   page_icon="🧮",
                   layout="centered",
                   initial_sidebar_state="collapsed")

# Header and description
st.title("Generate Math Quizzes 🧮")
st.text("Choose the difficulty level and topic for your math quizzes.")

# User input for quiz generation
## Layout in columns
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    selected_topic_level = st.selectbox('Select Topic Level', list(math_topics.keys()))

with col2:
    selected_topic = st.selectbox('Select Topic', math_topics[selected_topic_level])

with col3:
    num_quizzes = st.slider('Number Quizzes', min_value=1, max_value= 5, value=1)

submit = st.button('Generate Quizzes')


# Final Response
if submit:
    with st.spinner("Generating Quizzes..."):
        response = GetLLMResponse(selected_topic_level, selected_topic, num_quizzes)
        st.success("Quizzes Generated!")
        
        # Display questions and answers in a table
        if response:
            st.subheader("Quiz Questions and Answers:")
            # Prepare data for the table
            result_df = pd.DataFrame(response)
            st.table(result_df)
        else:
            st.warning("No Quiz Questions and Answers")
            
else:
    st.warning("Click the 'Generate Quizzes' button to create quizzes.")
