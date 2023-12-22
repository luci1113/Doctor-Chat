import streamlit as st
from dataclasses import dataclass
from typing import Literal

from langchain.chat_models import ChatGooglePalm
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryMemory


st.set_page_config(
    page_title="Doctor AI",
    page_icon="👨‍⚕️",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get help' : 'https://github.com/luci1113',
        'Report a bug' : 'https://github.com/luci1113',
        'About':"# Buddy, You are not alone."
    }
)
#--------------- Back end ---------

@dataclass
class Message : 
    origin: Literal["human","ai"]
    message: str

def load_css():
    with open('static/style.css',"r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)
    
# Behavior after click

def on_click_callback():
    human_prompt = st.session_state.human_prompt
    llm_response = st.session_state.conversation.run(
        human_prompt
    )
    st.session_state.history.append(
        Message('human',human_prompt)
    )
    st.session_state.history.append(
        Message("ai",llm_response)
    )

    st.session_state.human_prompt = " "

# API LOAD PALM CHATBOT
def api():
    llm = ChatGooglePalm(
            google_api_key=st.secrets["palm_api_key"],
            temperature=0.4
            )
    return llm

#history show up 
def initilize_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    
    if "conversation" not in st.session_state:
        llm = api()
        st.session_state.conversation = ConversationChain(
            llm=llm)
        
#--------------- Front end-------------------
load_css()
initilize_session_state()

# This is the title and the initialisation of the containers 

st.title("Doctor AI this is your  assistant")
chat_placeholder = st.container()
prompt_placeholder = st.form("chat-form")

# Streamlit built-in function for user interaction
with st.sidebar:
    st.sidebar.image("./static/doctor.png")

    st.sidebar.markdown("---")
    header = st.sidebar.header("Doctor AI : Support When You Need It the Most")
    st.markdown("""
                **Doctor AI** offers an innovative web application with an integrated AI chatbot, tailoring its
                advice based on each patient's case. This platform combines exchange, reliable information,
                and emotional support, thereby enhancing the healing journey for cancer patients.""")
    
    # Contributors 
    st.sidebar.markdown("---")
    with st.expander('Contributors'):
        columns = st.columns([3,0.5,0.5])
        with columns[0]:
            st.write("**Nirmal Avhad**")
        with columns[1]:
            st.write("""<div style="width:100%;text-align:center;">
                            <a href="https://www.linkedin.com/in/nirmalavhad" style="float:center">
                            <img src="./app/static/LinkedIn_logo_initials.png" width="22px"></img>
                            </a></div>""",unsafe_allow_html=True)
        with columns[2]:
            st.write("""<div style="width:100%;text-align:center;">
                            <a href="https://www.github.com/luci1113" style="float:center">
                            <img src="./app/static/github-sign.png" width="22px"></img>
                            </a></div>""",unsafe_allow_html=True)
        columns = st.columns([3,0.5,0.5])
        with columns[0]:
            st.write("**Anup Muttha**")
        with columns[1]:
            st.write("""<div style="width:100%;text-align:center;">
                            <a href="https://www.linkedin.com/in/anup-muttha/" style="float:center">
                            <img src="./app/static/LinkedIn_logo_initials.png" width="22px"></img>
                            </a></div>""",unsafe_allow_html=True)
    
        columns = st.columns([3,0.5,0.5])
        with columns[0]:
            st.write("**Arshdeep Singh Mathadu**")
        with columns[1]:
            st.write("""<div style="width:100%;text-align:center;">
                            <a href="https://www.linkedin.com/in/arshdeepsingh13/" style="float:center">
                            <img src="./app/static/LinkedIn_logo_initials.png" width="22px"></img>
                            </a></div>""",unsafe_allow_html=True)
        columns = st.columns([3,0.5,0.5])
        with columns[0]:
            st.write("**Sanjay Prajapati**")
        with columns[1]:
            st.write("""<div style="width:100%;text-align:center;">
                            <a href="https://www.linkedin.com/in/i-sanjay-cs" style="float:center">
                            <img src="./app/static/LinkedIn_logo_initials.png" width="22px"></img>
                            </a></div>""",unsafe_allow_html=True)
        
            
    # University drop down         
    with st.expander("University"):
        st.image("./static/college.jpg")
    with st.expander('Coordinator'):
        columns = st.columns([3,1])
        with columns[0]:
            st.write("**Mrs. Sabha Dharawadkar**")
        

with chat_placeholder:  # chat display
    for chat in st.session_state.history:
        div = f"""
            <div class="chat-row {
                '' if chat.origin == "ai" else "row-reverse"}">
                <img class="chat-icon" src='./app/static/{"robot.png" if chat.origin == 'ai' else 'user.png '}' 
                width=32 height=32>
                <div class="chat-bubble
                {"ai-bubble" if chat.origin == 'ai' else "human-bubble"}">{chat.message}</div>
            </div>
            """
        st.markdown(div,unsafe_allow_html=True)

# Prompt behavior
with prompt_placeholder:
    cols = st.columns((6,1))
    cols[0].text_input(
        label="chat",
        value="Hello Nirmal",
        label_visibility="collapsed",
        key='human_prompt'
    )
    cols[1].form_submit_button(
        label="Submit",
        type='primary',
        on_click=on_click_callback
    )