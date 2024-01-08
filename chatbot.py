import os
import datetime
from dotenv import load_dotenv
import sys
import streamlit as st
from llama_index.llms import OpenAI as LlamaOpenAI
import openai 
from system_prompt import system_prompt
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.agent import OpenAIAgent
from llama_index import SimpleDirectoryReader
from llama_index import Document

sys.path.append("utils")

# importing utils
from sentence_window_retrieval import build_sentence_window_index, get_sentence_window_query_engine
from automerging_retrieval import build_automerging_index, get_automerging_query_engine
from trulens_recorder import load_trulens, get_tru

load_dotenv()

st.set_page_config(
    page_title="Chat with Sample Agent",
    page_icon="",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

# Load the OpenAI key from the environment variable
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    st.error("No OpenAI key found. Please set the OPENAI_API_KEY environment variable.")

openai.api_key = openai_key

llm = LlamaOpenAI(model="gpt-4", temperature=0.1, system_prompt=system_prompt)

@st.cache_data
def load_data():
    print("loading documents")
    documents = SimpleDirectoryReader(
        input_files=["./data/eBook-How-to-Build-a-Career-in-AI.pdf"]
    ).load_data()

    document = Document(text="\n\n".join([doc.text for doc in documents]))
    return document, documents

document, documents = load_data()

# import advanced RAG techniques
@st.cache_resource
def load_sentence_retrieval():
    print("loading sentence retrieval")
    sentence_index = build_sentence_window_index(
        document,
        llm,
        embed_model="local:BAAI/bge-small-en-v1.5",
        save_dir="sentence_index"
    )
    sentence_window_engine = get_sentence_window_query_engine(sentence_index)
    app_id = "Sentence Retrieval"
    return sentence_window_engine, app_id

@st.cache_resource
def load_automerging_retrieval():
    print("loading automerging retrieval")
    automerging_index = build_automerging_index(
        documents,
        llm,
        embed_model="local:BAAI/bge-small-en-v1.5",
        save_dir="merging_index"
    )
    automerging_engine = get_automerging_query_engine(automerging_index)
    app_id = "Automerging Retrieval" 
    return automerging_engine, app_id


# Pick which retrieval method to use
query_engine, app_id = load_automerging_retrieval() #load_sentence_retrieval() 

# Load the trulens recorder and object for dashboard
tru_recorder = load_trulens(query_engine, app_id)
tru = get_tru()

tools = [
    QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name="query_engine_tool",
            description="Query the supplied documents",
        ),
    ),
]

agent = OpenAIAgent.from_tools(
    llm=llm,
    tools=tools,
    system_prompt=system_prompt,
)


# CHAT 

st.title("Sample Agent")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello there. How can I help you today?",
        },
    ]

if st.button("Launch Dashboard"):
    tru.run_dashboard()


if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
    st.session_state.chat_engine: OpenAIAgent = agent
if prompt := st.chat_input(" "):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])



# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.spinner("The agent is thinking..."):
         with tru_recorder as recording:
            # Use query_engine to process the prompt
            vector_response = st.session_state.chat_engine(prompt)
       

    with st.chat_message("assistant"):
        response_string = vector_response.response
      
        # Display the full response in the chat
        st.markdown(response_string)

        # Append the response to the session state messages
        st.session_state.messages.append(
            {"role": "assistant", "content": response_string}
        )


