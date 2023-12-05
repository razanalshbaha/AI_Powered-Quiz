import os
import streamlit as st 
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate 
from langchain.chains import LLMChain
from apikey import apikey


os.environ['OPENAI_API_KEY'] = apikey

st.title('AI Powered Quiz Generator')
prompt = st.text_input('Enter your topic here')
q_num = st.number_input('Number of questions', min_value=1, max_value=20, value=10)

if 'questions' not in st.session_state:
    if prompt:
        topic_template = PromptTemplate(
            input_variables=['topic', 'q_num'],
            template='write me a {q_num}-question multiple choice quiz in the {topic} topic (make sure each question has 4 choices) and show the correct answers at the end of each question'
        )

        llm = OpenAI(temperature=0.9)
        topic_chain = LLMChain(llm=llm, prompt=topic_template, verbose=True)

        response = topic_chain.run(topic=prompt, q_num=q_num)
        questions = response.split("\n\n")  # Splitting the response into individual questions

        st.session_state.questions = questions

if 'questions' in st.session_state:
    score = 0
    for i, question in enumerate(st.session_state.questions):
        question_parts = question.split("\n")  # Splitting question and choices
        if len(question_parts) >= 5:
            st.write(question_parts[0])  # Displaying the question
            choices = [choice.strip() for choice in question_parts[1:-1]]

            radio_key = f"question_{i}_radio"
            answer = st.radio(label="Choose an answer", options=choices, key=radio_key)

            if answer == question_parts[-1].split(': ', 1)[-1]:
                score += 1

    if st.button("Submit"):
        for i, question in enumerate(st.session_state.questions):
            question_parts = question.split("\n")
            st.write(question_parts[0])
            st.write(question_parts[-1].split(': ', 1)[-1])
        st.write(f"Your score is {score}")