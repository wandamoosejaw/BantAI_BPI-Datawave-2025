# Alerts.py

#import libraries
import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.style import inject_custom_css



st.set_page_config(page_title="Dashboard", page_icon="icons/bantai_logo.png")
st.write("# Alerts")


# Right after st.set_page_config(), add:
inject_custom_css()

