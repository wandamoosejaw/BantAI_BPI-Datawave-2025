# Home.py
import streamlit as st
from utils.style import inject_custom_css
from utils.charts import login_attempts_vs_flags_chart, top_risk_reasons_chart, login_outcomes_pie_chart

# Sidebar configuration
st.set_page_config(
    page_title="BantAI Security Dashboard",
    page_icon="icons/bantai_logo.png",
    layout="wide"
)

# Inject custom CSS
inject_custom_css()

# --- Sidebar logout button ---
st.sidebar.markdown("---")  # separator line
if st.sidebar.button("🚪 Logout"):
    st.session_state.authenticated = False
    st.switch_page("streamlit_app.py")

# Header with date
col_header1, col_header2 = st.columns([3, 1])
with col_header1:
    st.title("BantAI Security Dashboard")
with col_header2:
    st.markdown("<div style='text-align: right; color: #666; margin-top: 20px;'>September 03, 2023</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">89,855</div>
        <div class="metric-label">Login Attempts (24h)</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">89,855</div>
        <div class="metric-label">Failed Logins (24h)</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">89,855</div>
        <div class="metric-label">Attack IP Hits (24h)</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">89,855</div>
        <div class="metric-label">High-Risk Flags (24h)</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Charts section
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("""
    <div class="chart-container">
        <h3 class="chart-title">Login Attempts vs. High-Risk Flags</h3>
    """, unsafe_allow_html=True)
    login_attempts_vs_flags_chart()
    st.markdown("</div>", unsafe_allow_html=True)

with chart_col2:
    st.markdown("""
    <div class="chart-container">
        <h3 class="chart-title">Top Risk Reasons</h3>
    """, unsafe_allow_html=True)
    top_risk_reasons_chart()
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Bottom section
bottom_col1, bottom_col2 = st.columns([2, 1])

with bottom_col1:
    st.markdown("""
    <div class="chart-container">
        <h3 class="chart-title">Recent Login Activities</h3>
    """, unsafe_allow_html=True)
    
    # Sample data for recent login activities
    recent_activities = {
        "Time": ["14:32:15", "14:28:43", "14:25:12", "14:22:58", "14:20:31"],
        "User": ["alice@company.com", "bob@company.com", "charlie@company.com", "diana@company.com", "eve@company.com"],
        "IP Address": ["192.168.1.100", "10.0.0.25", "172.16.0.8", "192.168.1.150", "10.0.0.33"],
        "Location": ["Manila, PH", "Cebu, PH", "Davao, PH", "Manila, PH", "Quezon City, PH"],
        "Status": ["✅ Success", "❌ Failed", "✅ Success", "⚠️ Flagged", "✅ Success"]
    }
    
    st.dataframe(
        recent_activities,
        use_container_width=True,
        hide_index=True,
        height=200
    )
    st.markdown("</div>", unsafe_allow_html=True)

with bottom_col2:
    # Login Outcomes section
    st.markdown("""
    <div class="chart-container">
        <h3 class="chart-title">Login Outcomes</h3>
    """, unsafe_allow_html=True)
    
    login_outcomes_pie_chart()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Metrics
    st.markdown("""
    <div class="bottom-metrics">
        <div class="bottom-metric">
            <div class="bottom-metric-value">97%</div>
            <div class="bottom-metric-label">Login Risk Detection Accuracy</div>
        </div>
        <div class="bottom-metric">
            <div class="bottom-metric-value">234</div>
            <div class="bottom-metric-label">False Positives Marked (7d)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)