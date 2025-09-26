#Alerts.py

#import libraries
import streamlit as st
from utils.style import inject_custom_css
from utils.charts import login_attempts_vs_flags_chart, top_risk_reasons_chart, login_outcomes_pie_chart
import pandas as pd
from datetime import datetime

#Set page configurations
st.set_page_config(page_title="Alerts", page_icon="icons\bantai_logo.png")
st.write("# BantAI Security Dashboard")

st.sidebar.image("icons\BantAI_text_logo.png")



