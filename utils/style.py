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

    /* FIXED: Sidebar styling with Poppins font */
    section[data-testid="stSidebar"] {
        background-color: #F5F5F5 !important;
        font-family: 'Poppins', sans-serif !important;
    }

    /* FIXED: Force Poppins on all sidebar elements */
    section[data-testid="stSidebar"] * {
        font-family: 'Poppins', sans-serif !important;
        color: #333333 !important;
    }

    /* FIXED: Sidebar navigation links */
    section[data-testid="stSidebar"] .css-17lntkn,
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"],
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] * {
        font-family: 'Poppins', sans-serif !important;
        color: #333333 !important;
        background-color: transparent !important;
    }

    /* FIXED: Sidebar buttons and links */
    section[data-testid="stSidebar"] button,
    section[data-testid="stSidebar"] a,
    section[data-testid="stSidebar"] .stButton,
    section[data-testid="stSidebar"] .stSelectbox {
        font-family: 'Poppins', sans-serif !important;
        color: #333333 !important;
    }

    /* FIXED: Override any conflicting column styles for sidebar */
    section[data-testid="stSidebar"] div.stColumn,
    section[data-testid="stSidebar"] div.stColumn * {
        background-color: transparent !important;
        font-family: 'Poppins', sans-serif !important;
        color: #333333 !important;
    }

    /* FIXED: Remove the login page column styling from sidebar */
    section[data-testid="stSidebar"] div.stColumn:first-child,
    section[data-testid="stSidebar"] div.stColumn:nth-child(2) {
        background-color: transparent !important;
        padding: 0 !important;
        border-radius: 0 !important;
        min-height: auto !important;
    }

    /* Hide Streamlit's default navigation */
    section[data-testid="stSidebarNav"] {
        display: none !important;
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

            
    /* Force col1 (first column) background + font - ONLY for main content, not sidebar */
        .main div.stColumn:first-child {
            background-color: #FFFFFF !important;
            padding: 30px;
            border-radius: 8px;
            font-family: 'Poppins', sans-serif !important;
            color: #333333 !important;
            min-height: 100vh;   /* fill full viewport height */
        }


    /* Ensure col2 (second column) has gray bg - ONLY for main content, not sidebar */
            .main div.stColumn:nth-child(2) {
                background-color: #F5F5F5 !important;
                padding: 30px;
                border-radius: 8px;
            } 

    /* Force Poppins inside all main content columns - not sidebar */
            .main div.stColumn, .main div.stColumn * {
                font-family: 'Poppins', sans-serif !important;
                color: #333333 !important;
            }
         
     /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }
    
    /* Title styling */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 600 !important;
        color: #2c3e50 !important;
        margin-bottom: 0.5rem !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* FIXED: Row containers for proper grouping */
    .metrics-row {
        background: transparent;
        margin-bottom: 2rem;
    }
    
    .charts-row {
        background: transparent;
        margin-bottom: 2rem;
    }
    
    .bottom-row {
        background: transparent;
        margin-bottom: 2rem;
    }
    
    /* FIXED: Container wrappers that actually contain Streamlit elements */
    .chart-container-wrapper {
        background: white !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        border: 1px solid #e9ecef !important;
        margin-bottom: 1rem !important;
        height: 100% !important;
    }
    
    .table-container-wrapper {
        background: white !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        border: 1px solid #e9ecef !important;
        margin-bottom: 1rem !important;
        height: 100% !important;
    }
    
    .right-panel-wrapper {
        background: white !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        border: 1px solid #e9ecef !important;
        height: 100% !important;
        display: flex;
        flex-direction: column;
    }
    
    .pie-chart-section {
        margin-bottom: 1rem;
    }
    
    .bottom-metrics-section {
        margin-top: auto;
    }
    
    /* FIXED: Target actual Streamlit column containers */
    div[data-testid="column"] {
        padding: 0.5rem !important;
    }
    
    div[data-testid="column"] > div {
        height: 100%;
    }
    
    /* Metric cards */
    .metric-card {
        background: white !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        border: 1px solid #e9ecef !important;
        text-align: center !important;
        margin-bottom: 1rem !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        height: 120px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }
    
    .metric-card:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15) !important;
    }
    
    .metric-value {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #2c3e50 !important;
        margin-bottom: 0.5rem !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    .metric-label {
        font-size: 0.9rem !important;
        color: #6c757d !important;
        font-weight: 500 !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* Chart titles */
    .chart-title {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        color: #2c3e50 !important;
        margin-bottom: 1rem !important;
        margin-top: 0 !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* Bottom metrics styling */
    .bottom-metric {
        margin-bottom: 1.5rem !important;
        text-align: center !important;
    }
    
    .bottom-metric-value {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #2c3e50 !important;
        margin-bottom: 0.25rem !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    .bottom-metric-label {
        font-size: 0.85rem !important;
        color: #6c757d !important;
        font-weight: 500 !important;
        line-height: 1.3 !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* FIXED: Target Streamlit's actual dataframe container */
    div[data-testid="stDataFrame"] {
        border: none !important;
        background: transparent !important;
    }
    
    div[data-testid="stDataFrame"] > div {
        border: none !important;
        border-radius: 8px !important;
    }
    
    /* FIXED: Remove gaps between elements */
    div[data-testid="element-container"] {
        margin-bottom: 0 !important;
    }
    
    div[data-testid="stVerticalBlock"] > div[style*="gap"] {
        gap: 0.5rem !important;
    }
    
    /* FIXED: Target Streamlit's chart containers */
    div[data-testid="stVegaLiteChart"] {
        background: transparent !important;
        border: none !important;
        margin: 0 !important;
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