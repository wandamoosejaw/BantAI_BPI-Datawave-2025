# import libraries
import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
                

    /* Immediate hide - runs before page fully loads */
        button[kind="header"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* FORCE Poppins everywhere - highest specificity */
    html, body, [class*="css"], *, 
    section[data-testid="stSidebar"], 
    section[data-testid="stSidebar"] *,
    section[data-testid="stSidebarNav"],
    section[data-testid="stSidebarNav"] * {
        font-family: 'Poppins', sans-serif !important;
        color: #333333 !important;
    }

    /* Hide unwanted Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}



    /* Sidebar styling - WHITE background */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        font-family: 'Poppins', sans-serif !important;
    }

    section[data-testid="stSidebar"] > div {
        background-color: #FFFFFF !important;
        font-family: 'Poppins', sans-serif !important;
    }

    /* Force Poppins on ALL sidebar elements */
    section[data-testid="stSidebar"] *,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] a,
    section[data-testid="stSidebar"] button {
        font-family: 'Poppins', sans-serif !important;
        color: #333333 !important;
    }

    /* Streamlit's native navigation styling with Poppins */
    section[data-testid="stSidebarNav"] {
        font-family: 'Poppins', sans-serif !important;
        display: block !important;
        margin-top: 1rem !important;
    }

    section[data-testid="stSidebarNav"] ul {
        padding: 0 !important;
        margin: 0 !important;
        font-family: 'Poppins', sans-serif !important;
        list-style: none !important;
    }

    section[data-testid="stSidebarNav"] li {
        list-style: none !important;
        margin-bottom: 0.5rem !important;
        font-family: 'Poppins', sans-serif !important;
    }

    section[data-testid="stSidebarNav"] a {
        display: block !important;
        padding: 0.75rem 1rem !important;
        color: #333333 !important;
        text-decoration: none !important;
        border-radius: 8px !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
        transition: background-color 0.2s ease !important;
    }

    section[data-testid="stSidebarNav"] a:hover {
        background-color: #f8f9fa !important;
    }

    /* Active page styling */
    section[data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: #e3f2fd !important;
        font-weight: 600 !important;
    }

    /* Custom sidebar buttons styling */
    section[data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        text-align: center !important;
        background-color: #E63946 !important;
        color: white !important;
        border: none !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
        padding: 0.75rem 1rem !important;
        border-radius: 8px !important;
        transition: background-color 0.2s ease !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #c73035 !important;
    }

    /* Logo styling */
    section[data-testid="stSidebar"] img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        max-width: 120px;
        margin-bottom: 1rem;
    }

    /* Main container styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }

    /* Typography - force Poppins */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif !important;
        color: #2c3e50 !important;
    }

    h1 {
        font-size: 2.5rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }

    h3 {
        font-weight: 600 !important;
        font-size: 1.25rem !important;
    }

    /* Metric containers styling */
    div[data-testid="metric-container"] {
        background: white !important;
        border: 1px solid #DDDDDD !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        box-shadow: none !important;
    }

    /* Metric values with Poppins */
    div[data-testid="stMetricValue"] {
        color: #E63946 !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
    }

    div[data-testid="stMetricLabel"] {
        font-family: 'Poppins', sans-serif !important;
        color: #6c757d !important;
        font-weight: 500 !important;
    }

    /* Column containers */
    div[data-testid="column"] {
        padding: 0.5rem !important;
    }

    /* Dataframe styling with Poppins */
    div[data-testid="stDataFrame"],
    div[data-testid="stDataFrame"] *,
    div[data-testid="stDataFrame"] table,
    div[data-testid="stDataFrame"] th,
    div[data-testid="stDataFrame"] td {
        font-family: 'Poppins', sans-serif !important;
        color: #333333 !important;
    }

    div[data-testid="stDataFrame"] {
        border: none !important;
        background: transparent !important;
    }

    div[data-testid="stDataFrame"] > div {
        border: none !important;
        border-radius: 8px !important;
    }

    /* Chart containers */
    div[data-testid="stVegaLiteChart"] {
        background: transparent !important;
        border: none !important;
        margin: 0 !important;
    }

    /* Remove element gaps */
    div[data-testid="element-container"] {
        margin-bottom: 0 !important;
    }

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
    
    /* Completely hide the broken collapse button */
    button[kind="header"],
    button[title="Close sidebar"],
    button[aria-label="Close sidebar"],
    *[data-testid*="collaps"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* Hide any element containing keyboard_arrow text */
*   :contains("keyboard_arrow") {
    display: none !important;
    }
                
    /* Nuclear option - hide all possible collapse button selectors */
        button[kind="header"],
        button[title="Close sidebar"],
        button[aria-label="Close sidebar"],
        button[data-testid*="collaps"],
        .css-1544g2n,
        .css-1cypcdb,
        .css-18ni7ap,
        [class*="collapse"],
        [class*="sidebar"][class*="button"],
        button:contains("keyboard_arrow"),
        *:contains("keyboard_arrow_double") {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            width: 0 !important;
            height: 0 !important;
            overflow: hidden !important;
    }

/* Hide any button in the sidebar header area */
    section[data-testid="stSidebar"] > div:first-child button {
        display: none !important;
    }

/* Alternative: Hide the entire top area of sidebar */
    section[data-testid="stSidebar"] > div:first-child > div:first-child {
    display: none !important;
}
                
/* Add BantAI text as CSS */
section[data-testid="stSidebar"]::before {
    content: "BantAI";
    display: block;
    font-family: 'Poppins', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #E63946;
    text-align: center;
    padding: 1rem 0;
    margin-bottom: 1rem;
    border-bottom: 1px solid #dee2e6;
}
/* Add spacing after logo */
    section[data-testid="stSidebarNav"] {
        font-family: 'Poppins', sans-serif !important;
        display: block !important;
        margin-top: 1rem !important;
        padding-top: 0 !important;
    }
                
/* Add proper spacing to sidebar navigation */
    section[data-testid="stSidebarNav"] {
        font-family: 'Poppins', sans-serif !important;
        display: block !important;
        margin-top: 2rem !important;  /* Increased from 1rem */
        padding-top: 1rem !important;
    }

/* Add some breathing room to the entire sidebar content */
    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem !important;
    }
                
    # Add to your utils/style.py
    /* Hide broken Material Icons */
    *:contains("keyboard_arrow") {
        display: none !important;
    }

    /* Hide any broken icon text */
    span:contains("keyboard_arrow_right"),
    span:contains("keyboard_arrow_left"),
    span:contains("keyboard_arrow_double") {
        display: none !important;
        visibility: hidden !important;
}

    </style>
    """, unsafe_allow_html=True)