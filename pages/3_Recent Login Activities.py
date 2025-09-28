import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.style import inject_custom_css
from utils.database import get_login_activities, update_action

st.set_page_config(page_title="Recent Login Activities", layout="wide")
inject_custom_css()

st.title("Recent Login Activities")
st.markdown("Filtered view of recent login attempts with admin actions.")

# Get data from database instead of hardcoded data
df = get_login_activities()

# Display the dataframe
st.dataframe(df, use_container_width=True, hide_index=True)

# Add admin action buttons for each row
st.markdown("### Admin Actions")

for index, row in df.iterrows():
    col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
    
    with col1:
       risk_level = "HIGH RISK" if row['Risk %'] >= 70 else "LOW RISK"
    st.write(f"**{row['User ID']}** - {risk_level} ({row['Risk %']}%) - {row['Country']}")
    
    with col2:
        if st.button("✅ False Positive", key=f"fp_{row['#']}"):
            update_action(row['#'], 'False Positive')
            st.success("Marked as False Positive")
            st.rerun()
    
    with col3:
        if st.button("❌ True Positive", key=f"tp_{row['#']}"):
            update_action(row['#'], 'True Positive - Blocked')
            st.success("Marked as True Positive")
            st.rerun()
    
    with col4:
        if st.button("🔒 Require OTP", key=f"otp_{row['#']}"):
            update_action(row['#'], 'Require OTP')
            st.success("OTP Required")
            st.rerun()
    
    st.markdown("---")