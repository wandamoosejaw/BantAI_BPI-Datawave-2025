# import libraries
import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    /* Global font */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
        color: #333333 !important;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #F5F5F5 !important;
    }

    section[data-testid="stSidebar"] * {
        font-family: 'Poppins', sans-serif !important;
        color: #333333 !important;
    }

    /* Metric number highlight */
    div[data-testid="stMetricValue"] {
        color: #E63946 !important;
    }

    /* Keep logo pinned at top of sidebar */
    section[data-testid="stSidebar"] img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        max-width: 120px;
        position: relative;
        top: 0;
        z-index: 1000;
    }

    /* Push nav menu down below logo */
    [data-testid="stSidebarNav"] {
        margin-top: 20px !important;
    }

    ####LOGIN STYLE CONFIG          
    /* Login page two-column background colors */
            [data-testid="stHorizontalBlock"] > div:nth-child(1) {
                background-color: #FFFFFF;
                padding: 30px;
                border-radius: 8px;
            }
    /* Column 1: Form */
        [data-testid="stForm"] {
        background-color: transparent;   /* remove box background */
        box-shadow: none;                /* remove box shadow */
        border: none;                    /* remove border */
        padding: 0;
        }

    /* Form input fields */
        [data-testid="stForm"] input {
            background-color: #F5F5F5;   /* field background */
            border: none;                /* remove all borders */
            border-radius: 6px;          /* smooth corners */
            padding: 10px;
            width: 100%;                 /* span full column */
            box-shadow: none;            /* no outline */
        }

    /* Remove black stroke when typing */
        [data-testid="stForm"] input:focus {
            outline: none;
            box-shadow: 0 0 0 2px #c7c7c7;   /* subtle gray glow instead of black stroke */
        }

            
    /* Force col1 (first column) background + font */
        div.stColumn:first-child {
            background-color: #FFFFFF !important;
            padding: 30px;
            border-radius: 8px;
            font-family: 'Poppins', sans-serif !important;
            color: #333333 !important;
            min-height: 100vh;   /* fill full viewport height */
        }


    /* Ensure col2 (second column) has gray bg */
            div.stColumn:nth-child(2) {
                background-color: #F5F5F5 !important;
                padding: 30px;
                border-radius: 8px;
            } 

    /* Force Poppins inside all columns */
            div.stColumn, div.stColumn * {
                font-family: 'Poppins', sans-serif !important;
                color: #333333 !important;
            }
         
     /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Title styling */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 600 !important;
        color: #2c3e50 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #e9ecef;
        text-align: center;
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        font-weight: 500;
    }
    
    /* Chart containers */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #e9ecef;
        margin-bottom: 1.5rem;
    }
    
    .chart-title {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        color: #2c3e50 !important;
        margin-bottom: 1rem !important;
        margin-top: 0 !important;
    }
    
    /* Bottom metrics styling */
    .bottom-metrics {
        margin-top: 1rem;
    }
    
    .bottom-metric {
        margin-bottom: 1.5rem;
    }
    
    .bottom-metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.25rem;
    }
    
    .bottom-metric-label {
        font-size: 0.85rem;
        color: #6c757d;
        font-weight: 500;
        line-height: 1.3;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border: none !important;
    }
    
    .stDataFrame > div {
        border: none !important;
    }
    
    /* Remove default streamlit padding/margins */
    .element-container {
        margin: 0 !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Hide streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }               
                
    </style>
    
                
        
    """, unsafe_allow_html=True)
