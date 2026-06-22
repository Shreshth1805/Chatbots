import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain,LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool,initialize_agent
from langchain.callbacks import StreamlitCallbackHandler
from dotenv import load_dotenv

## Setup Streamlit App:
st.set_page_config(page_title="Text To MATH Problem Solver")
st.title("Text To MATH Problem Solver")
groq_api_key=st.sidebar.text_input(label="GROQ_API_KEY",type="password")

if not groq_api_key:
    st.info("Please add Groq API KEY to continue")
    st.stop()

llm=ChatGroq(model="llama-3.3-70b-versatile",groq_api_key=groq_api_key)


## Tools:
wikipedia_wrapper=WikipediaAPIWrapper()
wikipedia_tool=Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool for searching internet and solving Math problem"

)
## Initialize Math Problem:
math_chain=LLMMathChain.from_llm(llm=llm)
calculator=Tool(
    name="Calculator",
    func=math_chain.run,
    description="A Tool for answering Math related problem"
)
prompt="""You are an agent tasked for solving users mathematical questions.Logically arrive at the Solution and display it point wisefor question below
Question:{question}
Answer:
"""
prompt_template=PromptTemplate(input_variables=["question"],template=prompt)

## Combine all the tools into Chain:
chain=LLMChain(llm=llm,prompt=prompt_template)

reasoning_tool=Tool(
    name="Reasoning Tool",
    func=chain.run,
    description="A Tool for answering logic based and reasoning questions"
)

## Initialize the agent:

assistant_agent=initialize_agent(tools=[wikipedia_tool,calculator,reasoning_tool],llm=llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=True,handle_parsing_errors=True)

if "messages" not in st.session_state:
    st.session_state["messages"]=[{"role":"assistant","content":"Hi,I'm Math Chatbot to answer all the maths question"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"]) 



## Let's Start the interaction:
user_question=st.text_input("Enter Your Question")
if st.button("Find Answer"):
    if user_question:
        with st.spinner("Generate Response"):
            st.session_state.messages.append({"role":"user","content":user_question})
            st.chat_message("user").write(user_question)

            st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
            response=assistant_agent.run(user_question,callbacks=[st_cb])
            st.session_state.messages.append({"role":"assistant","content":response})

            st.write('### Response:')
            st.success(response)
    else:
        st.warning("Please enter question")        