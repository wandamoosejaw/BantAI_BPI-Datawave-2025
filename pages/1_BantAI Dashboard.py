# BantAI Dashboard - Enhanced with Model Intelligence
import streamlit as st
from datetime import datetime
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.style import inject_custom_css
from utils.charts import login_attempts_vs_flags_chart, top_risk_reasons_chart, login_outcomes_pie_chart
from utils.database import (
    get_login_activities_enhanced, 
    get_dashboard_metrics_enhanced, 
    get_detection_accuracy, 
    get_false_positives_count
)

# Page Configuration
st.set_page_config(page_title="BantAI Dashboard", page_icon="icons/bantai_logo.png", layout="wide")

# Inject the css
inject_custom_css()

# Header
col_header1, col_header2 = st.columns([3, 1])
with col_header1:
    st.title("BantAI Security Dashboard")
    st.caption("Filipino-Centric AI Agent for Secure Digital Banking Access")
with col_header2:
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%B %d, %Y")
    formatted_time = current_datetime.strftime("%I:%M %p")
    st.markdown(f"**{formatted_date}**  \n{formatted_time}")

# Get real-time data from enhanced database
try:
    df = get_login_activities_enhanced()
    metrics = get_dashboard_metrics_enhanced()
    detection_accuracy = get_detection_accuracy()
    false_positives_count = get_false_positives_count()
    
    # Enhanced metrics from new database structure
    total_attempts = metrics['total_attempts']
    high_risk = metrics['high_risk']
    blocked_attempts = metrics['blocked']
    otp_required = metrics['otp_required']
    attack_ips = metrics['attack_ips']
    
except Exception as e:
    st.error(f"Database connection error: {e}")
    # Fallback to dummy data
    total_attempts = 15
    high_risk = 3
    blocked_attempts = 1
    otp_required = 2
    attack_ips = 1
    detection_accuracy = 94
    false_positives_count = 12

# Enhanced KPI Metrics showing AI actions
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Login Attempts",
        value=f"{total_attempts:,}",
        help="Total login attempts analyzed by BantAI"
    )

with col2:
    st.metric(
        label="High-Risk Detected",
        value=f"{high_risk:,}",
        delta=f"{high_risk/total_attempts*100:.1f}% of total" if total_attempts > 0 else "0%",
        help="Activities flagged as high-risk (≥70%)"
    )

with col3:
    st.metric(
        label="Blocked by AI",
        value=f"{blocked_attempts:,}",
        delta="Prevented" if blocked_attempts > 0 else "None",
        help="Login attempts automatically blocked"
    )

with col4:
    st.metric(
        label="OTP Required",
        value=f"{otp_required:,}",
        delta="Additional Auth" if otp_required > 0 else "None",
        help="Logins requiring SMS OTP verification"
    )

st.markdown("---")

# AI Actions Overview
st.subheader("AI Decision Summary")

if total_attempts > 0:
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        allowed = total_attempts - blocked_attempts - otp_required
        st.metric(
            label="✅ ALLOW",
            value=f"{allowed:,}",
            delta=f"{allowed/total_attempts*100:.1f}%",
            help="Automatically approved logins"
        )
    
    with action_col2:
        st.metric(
            label="🔐 ALLOW_WITH_OTP", 
            value=f"{otp_required:,}",
            delta=f"{otp_required/total_attempts*100:.1f}%",
            help="Approved with SMS verification"
        )
    
    with action_col3:
        st.metric(
            label="🚫 BLOCK",
            value=f"{blocked_attempts:,}",
            delta=f"{blocked_attempts/total_attempts*100:.1f}%",
            help="Denied access - high risk"
        )

st.markdown("---")

# Charts section
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Login Attempts vs. High-Risk Flags")
    login_attempts_vs_flags_chart()

with chart_col2:
    st.subheader("Top Risk Reasons")
    top_risk_reasons_chart()

st.markdown("---")

# Enhanced Recent Activities with AI Analysis
recent_col1, recent_col2 = st.columns([3, 1])

with recent_col1:
    st.subheader("Recent AI Analysis")
    
    if len(df) > 0:
        # Show last 5 activities with enhanced details
        for index, row in df.head(5).iterrows():
            with st.container():
                # Create activity card
                risk_color = "🔴" if row['Risk %'] >= 70 else "🟡" if row['Risk %'] >= 30 else "🟢"
                action_icon = "🚫" if row['AI Action'] == 'BLOCK' else "🔐" if row['AI Action'] == 'ALLOW_WITH_OTP' else "✅"
                
                col_a, col_b, col_c = st.columns([2, 2, 1])
                
                with col_a:
                    st.markdown(f"**{row['User ID']}** from {row['Country']}")
                    st.caption(f"{row['Login Timestamp (UTC+8)']} • {row['device_type']}")
                
                with col_b:
                    st.markdown(f"{risk_color} **{row['Risk %']:.1f}% Risk** ({row['Classification']})")
                    st.caption(f"{action_icon} AI Action: **{row['AI Action']}**")
                
                with col_c:
                    if row['Admin Action'] == 'Pending Review':
                        st.markdown("🔄 Pending")
                    else:
                        st.markdown("✓ Reviewed")
                
                # Show AI recommendation
                st.markdown(f"💡 **Recommendation:** {row['AI Recommendation']}")
                
                # Show analysis factors
                if row['Analysis Factors']:
                    factors = row['Analysis Factors'] if isinstance(row['Analysis Factors'], list) else []
                    if factors:
                        with st.expander("📊 Analysis Details", expanded=False):
                            for factor in factors:
                                st.markdown(f"• {factor}")
                            
                            # Show warnings if any
                            if row['Warnings']:
                                warnings = row['Warnings'] if isinstance(row['Warnings'], list) else []
                                if warnings:
                                    for warning in warnings:
                                        st.markdown(f"{warning}")
                
                st.markdown("---")
        
        # Link to full analysis page
        if st.button("🔍 View All Activities & Take Actions"):
            st.switch_page("pages/3_Recent Login Activities.py")
    else:
        st.info("No recent login activities to display")

with recent_col2:
    st.subheader("System Performance")
    
    # Detection accuracy
    accuracy_color = "🟢" if detection_accuracy >= 95 else "🟡" if detection_accuracy >= 85 else "🔴"
    st.metric(
        label=f"{accuracy_color} Detection Accuracy",
        value=f"{detection_accuracy}%",
        help="AI model accuracy based on admin feedback"
    )
    
    # False positives
    st.metric(
        label="False Positives (7d)",
        value=f"{false_positives_count}",
        help="Admin corrections in last 7 days"
    )
    
    # Login outcome pie chart
    st.subheader("Login Outcomes")
    login_outcomes_pie_chart()
    
    # Filipino context insights
    if len(df) > 0:
        st.subheader("🇵🇭 Filipino Context")
        
        # Count OFW-related logins
        ofw_locations = df[df['Location Context'].str.contains('OFW', na=False)]
        domestic_locations = df[df['Location Context'].str.contains('Domestic', na=False)]
        
        st.metric("OFW Hub Logins", len(ofw_locations))
        st.metric("Domestic Logins", len(domestic_locations))

# System Status with Enhanced Indicators
st.markdown("---")
st.subheader("🔍 System Status")

status_col1, status_col2, status_col3, status_col4 = st.columns(4)

with status_col1:
    if total_attempts > 0:
        st.success("✅ AI Model Active")
        st.caption(f"Analyzed {total_attempts} attempts")
    else:
        st.warning("⚠️ No Recent Activity")

with status_col2:
    if detection_accuracy >= 95:
        st.success(f"✅ Excellent Accuracy")
        st.caption(f"{detection_accuracy}% detection rate")
    elif detection_accuracy >= 85:
        st.warning(f"⚠️ Good Accuracy")
        st.caption(f"{detection_accuracy}% detection rate")
    else:
        st.error(f"❌ Needs Improvement")
        st.caption(f"{detection_accuracy}% detection rate")

with status_col3:
    if blocked_attempts == 0:
        st.success("✅ No Threats Blocked")
    elif blocked_attempts <= 2:
        st.warning(f"⚠️ {blocked_attempts} Threat(s) Blocked")
    else:
        st.error(f"🚨 {blocked_attempts} Threats Blocked")
    st.caption("Automatic protection active")

with status_col4:
    if attack_ips == 0:
        st.success("✅ No Attack IPs")
    else:
        st.error(f"🚨 {attack_ips} Attack IP(s)")
    st.caption("Threat intelligence active")

# Quick Actions
st.markdown("---")
st.subheader("⚡ Quick Actions")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("🔄 Refresh Dashboard", use_container_width=True):
        st.rerun()

with action_col2:
    if st.button("⚙️ Admin Control Panel", use_container_width=True):
        st.switch_page("pages/7_Admin_Control.py")

with action_col3:
    if st.button("📊 Export Reports", use_container_width=True):
        st.switch_page("pages/8_Export Report.py")

# Real-time updates indicator
st.caption(f"📡 Last updated: {datetime.now().strftime('%H:%M:%S')} • BantAI v1.0 • Real-time monitoring active")