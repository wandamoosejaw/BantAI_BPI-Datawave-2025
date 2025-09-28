# streamlit_app.py
import streamlit as st
from utils.style import inject_custom_css
import time

# --- Config at very top ---
st.set_page_config(
    page_title="BPI BantAI",
    page_icon="icons/bantai_logo.png",
    layout="wide"
)

# --- Custom CSS for login layout ---
login_page_style = """
    <style>
        /* Hide sidebar on login */
        section[data-testid="stSidebar"] {
            display: none;
        }

        /* Remove default padding & margins from main container */
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
        }

        /* Full-height columns */
        [data-testid="stHorizontalBlock"] {
            min-height: 100vh !important;   /* force viewport height */
        }

        /* Column 1 (white background) */
        [data-testid="stHorizontalBlock"] > div:nth-child(1) {
            background-color: #FFFFFF !important;
            padding: 3rem !important;
        }

        /* Column 2 (gray background) */
        [data-testid="stHorizontalBlock"] > div:nth-child(2) {
            background-color: #F5F5F5 !important;
            padding: 0;
        }

        /* Style the login button only */
        [data-testid="stForm"] button {
            background-color: #E63946 !important;
            color: #fff !important;
            font-weight: bold !important;
            border-radius: 6px !important;
            width: 100% !important;
            padding: 0.6em 0 !important;
            border: none !important;
            transition: background-color 0.2s ease-in-out;
        }
        [data-testid="stForm"] button:hover {
            background-color: #b71c1c !important;
        }
    </style>
"""
st.markdown(login_page_style, unsafe_allow_html=True)

# Inject global styles (fonts/colors, etc.)
inject_custom_css()

# --- Session state ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- Login page ---
if not st.session_state.authenticated:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image("icons/bpi_all_caps.png", width="content")   # logo stays responsive
        st.image("icons/BantAI_text_logo.png", width=200)     # fixed width text logo
        st.write("## Welcome!")

        with st.form("sign_in"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Log in")

        if submit:
            if username == "admin" and password == "1234":
                st.session_state.authenticated = True
                st.success("Login successful! Redirecting...")
                time.sleep(1)
                st.switch_page("pages/1_BantAI Dashboard.py")
            else:
                st.error("Invalid username or password")

    with col2:
        st.image("icons/page_AI.png", width="stretch")  # fills the right column

# --- Auto-redirect if already logged in ---
else:
    st.switch_page("pages/1_BantAI Dashboard.py")


    
