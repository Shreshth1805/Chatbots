import os
from dotenv import load_dotenv
load_dotenv()
import openai
import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="TRUE"
os.environ["LANGCHAIN_PROJECT"]="Q&A Chatbot with OPENAI"

prompt=ChatPromptTemplate.from_messages([("system","You are a helpful chat assistant"),
                                         ("user","Question:{question}")])

def generate_response(question,api_key,llm,temperature,max_tokens):
    openai.api_key=api_key
    llm=ChatOpenAI(model=llm)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke("{'question': question}")
    return answer

st.title("This is Q&A OPENAI chatbot ")
api_key=st.sidebar.text_input("Enter the API KEY")
llm=st.sidebar.selectbox("Choose the model",["gpt-4o","gpt-4o-mini"])
temperature=st.sidebar.slider("Temperature",min_value=0,max_value=1,value=.7)
max_tokens=st.sidebar.slider("max_tokens",min_value=50,max_value=300,value=150)

st.write("GO and ASK:")

user_input=st.text_input("YOU:")
if user_input:
    response=generate_response(user_input,api_key,llm,temperature,max_tokens)
    st.write(response)
else:
    st.write("Please enter the question")    