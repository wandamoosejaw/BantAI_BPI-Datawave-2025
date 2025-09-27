import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.style import inject_custom_css
from utils.database import add_login_activity_enhanced, get_login_activities_enhanced
from datetime import datetime

st.set_page_config(page_title="Admin Control", layout="wide")
inject_custom_css()

st.title("⚙️ Admin Control Panel")
st.markdown("Simulate login attempts and test BantAI's AI security analysis")

# Real-time system status
col_status1, col_status2, col_status3 = st.columns(3)

with col_status1:
    st.metric("🤖 AI Model", "Active", help="BantAI model is running")
with col_status2:
    st.metric("🛡️ Protection", "Enabled", help="Real-time threat detection active")
with col_status3:
    current_time = datetime.now().strftime("%H:%M:%S")
    st.metric("🕐 Status", f"Live {current_time}", help="System monitoring active")

st.markdown("---")

# Simulate new login attempt
st.subheader("🧪 Simulate Login Attempt")
st.markdown("Test different scenarios to see how BantAI's AI analyzes login patterns")

with st.form("simulate_login"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**User & Location**")
        user_id = st.text_input("User ID", value="U_TEST", help="Enter user identifier")
        country = st.selectbox("Country", [
            "Philippines", "United Arab Emirates", "Saudi Arabia", "Qatar", 
            "Singapore", "United States", "Canada", "Hong Kong", "Japan",
            "Russia", "Nigeria", "China"
        ], help="Select login country")
        city = st.text_input("City", value="Manila", help="Enter city name")
        device_type = st.selectbox("Device Type", ["mobile", "desktop", "tablet"], help="Select device used for login")
        
    with col2:
        st.markdown("**Login Characteristics**")
        time_diff = st.number_input("Time Difference (hours)", 
                                   min_value=0.1, max_value=168.0, value=2.0, step=0.1,
                                   help="Hours since last login")
        distance = st.number_input("Distance (km)", 
                                  min_value=0, max_value=20000, value=100, step=10,
                                  help="Distance from last login location")
        latency = st.number_input("Network Latency (ms)", 
                                 min_value=10, max_value=5000, value=50, step=10,
                                 help="Network response time")
        
        # Risk factors
        st.markdown("**Risk Factors**")
        is_attack_ip = st.checkbox("Known Attack IP", help="Simulate login from known malicious IP")
        login_successful = st.checkbox("Login Successful", value=True, help="Whether login attempt succeeded")

    # Preset scenarios
    st.markdown("**Quick Test Scenarios**")
    scenario_col1, scenario_col2, scenario_col3 = st.columns(3)
    
    with scenario_col1:
        if st.form_submit_button("🇦🇪 OFW Dubai Scenario", use_container_width=True):
            # Simulate legitimate OFW travel
            user_id = "U_OFW_TEST"
            country = "United Arab Emirates"
            city = "Dubai"
            time_diff = 12.0
            distance = 8500
            device_type = "mobile"
            latency = 180
            is_attack_ip = False
            login_successful = True
    
    with scenario_col2:
        if st.form_submit_button("🚨 Attack Scenario", use_container_width=True):
            # Simulate cyberattack
            user_id = "U_ATTACK_TEST"
            country = "Russia"
            city = "Moscow"
            time_diff = 0.5
            distance = 12000
            device_type = "desktop"
            latency = 2200
            is_attack_ip = True
            login_successful = False
    
    with scenario_col3:
        if st.form_submit_button("🏠 Local Login", use_container_width=True):
            # Simulate normal local login
            user_id = "U_LOCAL_TEST"
            country = "Philippines"
            city = "Manila"
            time_diff = 2.0
            distance = 15
            device_type = "mobile"
            latency = 45
            is_attack_ip = False
            login_successful = True

    # Main simulation button
    simulate_button = st.form_submit_button("🚀 Run AI Analysis", type="primary", use_container_width=True)

# Process simulation
if simulate_button:
    with st.spinner("🤖 BantAI is analyzing the login attempt..."):
        try:
            # Use the enhanced function to add login activity
            prediction = add_login_activity_enhanced(
                user_id=user_id,
                country=country, 
                city=city,
                time_diff=time_diff,
                distance=distance,
                device_type=device_type,
                latency=latency,
                is_attack_ip=is_attack_ip,
                login_successful=login_successful
            )
            
            st.success("✅ AI Analysis Complete!")
            
            # Display comprehensive AI analysis results
            st.markdown("---")
            st.subheader("🧠 BantAI Analysis Results")
            
            # Risk assessment
            risk_color = "🔴" if prediction['risk_percentage'] >= 70 else "🟡" if prediction['risk_percentage'] >= 30 else "🟢"
            action_icon = "🚫" if prediction['action'] == 'BLOCK' else "🔐" if prediction['action'] == 'ALLOW_WITH_OTP' else "✅"
            
            result_col1, result_col2, result_col3 = st.columns(3)
            
            with result_col1:
                st.metric(
                    label="Risk Assessment",
                    value=f"{prediction['risk_percentage']:.1f}%",
                    delta=f"{prediction['classification']} RISK"
                )
            
            with result_col2:
                st.metric(
                    label="AI Decision",
                    value=prediction['action'],
                    delta=f"Confidence: {prediction['behavior_consistency']}%"
                )
            
            with result_col3:
                st.metric(
                    label="Location Context", 
                    value=prediction['location_context'][:20] + "..." if len(prediction['location_context']) > 20 else prediction['location_context'],
                    delta=f"{country}"
                )
            
            # Detailed recommendation
            st.markdown("### 💡 AI Recommendation")
            st.info(f"{action_icon} **{prediction['recommendation']}**")
            
            # Analysis factors
            st.markdown("### 📊 Analysis Factors")
            for factor in prediction['analysis_factors']:
                st.markdown(f"• {factor}")
            
            # Warnings (if any)
            if prediction['warnings']:
                st.markdown("### ⚠️ Risk Indicators")
                for warning in prediction['warnings']:
                    st.warning(warning)
            
            # Filipino-specific insights
            if "OFW" in prediction['location_context']:
                st.markdown("### 🇵🇭 Filipino Context")
                st.success("✅ **OFW Pattern Detected**: This login matches typical Overseas Filipino Worker travel patterns to major employment hubs.")
            elif "cybercrime" in prediction['location_context'].lower():
                st.markdown("### 🇵🇭 Filipino Context")
                st.error("🚨 **Threat Location**: This location is known for targeting Filipino financial accounts.")
            
        except Exception as e:
            st.error(f"❌ Simulation failed: {e}")
            st.info("💡 Try refreshing the page or check if the database is properly initialized")

# Recent simulation results
st.markdown("---")
st.subheader("📈 Recent Simulations")

try:
    df = get_login_activities_enhanced()
    
    if len(df) > 0:
        # Show last 3 simulations
        recent_df = df.head(3)
        
        for index, row in recent_df.iterrows():
            with st.expander(f"🔍 {row['User ID']} from {row['Country']} - {row['Classification']} Risk", expanded=False):
                sim_col1, sim_col2 = st.columns(2)
                
                with sim_col1:
                    st.markdown(f"**Timestamp:** {row['Login Timestamp (UTC+8)']}")
                    st.markdown(f"**Location:** {row['City']}, {row['Country']}")
                    st.markdown(f"**Device:** {row['device_type']}")
                    st.markdown(f"**Risk Score:** {row['Risk %']:.1f}%")
                
                with sim_col2:
                    st.markdown(f"**AI Action:** {row['AI Action']}")
                    st.markdown(f"**Admin Status:** {row['Admin Action']}")
                    st.markdown(f"**Context:** {row['Location Context']}")
                
                st.markdown(f"**AI Recommendation:** {row['AI Recommendation']}")
    else:
        st.info("No simulations yet. Run your first test above!")
        
except Exception as e:
    st.error(f"Unable to load recent simulations: {e}")

# Quick actions
st.markdown("---")
st.subheader("⚡ Quick Actions")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("📊 View All Activities", use_container_width=True):
        st.switch_page("pages/3_Recent Login Activities.py")

with action_col2:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/1_BantAI Dashboard.py")

with action_col3:
    if st.button("📄 Export Reports", use_container_width=True):
        st.switch_page("pages/8_Export Report.py")

# System information
st.markdown("---")
st.caption("🤖 BantAI Admin Control Panel | Real-time AI security testing | Filipino-centric threat detection")