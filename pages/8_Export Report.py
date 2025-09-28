import streamlit as st
from datetime import datetime, timedelta
import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.style import inject_custom_css
from utils.database import get_login_activities, get_dashboard_metrics, get_detection_accuracy, get_false_positives_count
from utils.pdf_generator import generate_audit_report

# Page Configuration
st.set_page_config(page_title="Export Reports", page_icon="📊", layout="wide")
inject_custom_css()

st.title("📊 Export Audit Reports")
st.markdown("Generate comprehensive audit reports for BantAI security analysis")

# Date Range Selection
st.subheader("📅 Report Date Range")
col1, col2, col3 = st.columns(3)

with col1:
    # Quick presets
    preset = st.selectbox(
        "Quick Presets",
        ["Custom", "Last 7 days", "Last 30 days", "Last 90 days"]
    )

with col2:
    if preset == "Custom":
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=7))
    elif preset == "Last 7 days":
        start_date = datetime.now().date() - timedelta(days=7)
        st.info(f"Start Date: {start_date}")
    elif preset == "Last 30 days":
        start_date = datetime.now().date() - timedelta(days=30)
        st.info(f"Start Date: {start_date}")
    else:  # Last 90 days
        start_date = datetime.now().date() - timedelta(days=90)
        st.info(f"Start Date: {start_date}")

with col3:
    if preset == "Custom":
        end_date = st.date_input("End Date", value=datetime.now())
    else:
        end_date = datetime.now().date()
        st.info(f"End Date: {end_date}")

st.markdown("---")

# Report Content Selection
st.subheader("📋 Report Content")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Core Sections**")
    include_summary = st.checkbox("Executive Summary", value=True, disabled=True, help="Always included")
    include_details = st.checkbox("Detailed Activity Log", value=True)
    include_performance = st.checkbox("AI Model Performance", value=True)
    include_admin_actions = st.checkbox("Admin Actions Summary", value=True)

with col2:
    st.markdown("**Charts & Visualizations**")
    include_risk_chart = st.checkbox("Top Risk Reasons Chart", value=True)
    include_timeline_chart = st.checkbox("Login Timeline Chart", value=True)
    include_device_chart = st.checkbox("Device Distribution Chart", value=False)
    include_geo_chart = st.checkbox("Geographic Distribution", value=False)

st.markdown("---")

# Report Customization
st.subheader("⚙️ Report Options")

col1, col2 = st.columns(2)

with col1:
    report_title = st.text_input("Report Title", value="BantAI Security Analysis Report")
    report_id = st.text_input("Report ID", value=f"BANTAI-{datetime.now().strftime('%Y%m%d-%H%M%S')}")

with col2:
    include_sensitive = st.checkbox("Include Sensitive Data", value=False, help="Include full user details")
    report_format = st.selectbox("Export Format", ["PDF", "PDF + CSV Data"], index=0)

st.markdown("---")

# Preview Section
st.subheader("📊 Report Preview")

# Get data for preview - SINGLE data loading block
try:
    df = get_login_activities()
    metrics = get_dashboard_metrics()
    detection_accuracy = get_detection_accuracy()
    false_positives_count = get_false_positives_count()
    
    # Filter data by date range
    df['date'] = pd.to_datetime(df['Login Timestamp (UTC+8)']).dt.date
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    # Map column names for PDF generator
    if len(filtered_df) > 0:
        filtered_df = filtered_df.rename(columns={
            "Risk %": "AI Risk Score (0–100)",
            "AI Action": "Action"
        })
        
        # Handle null values in numeric columns
        filtered_df['AI Risk Score (0–100)'] = pd.to_numeric(filtered_df['AI Risk Score (0–100)'], errors='coerce').fillna(0)
    
except Exception as e:
    st.error(f"Error loading data: {e}")
    # Initialize empty dataframe as fallback
    filtered_df = pd.DataFrame()
    metrics = {'total_attempts': 0, 'failed_logins': 0, 'attack_ips': 0, 'high_risk': 0}
    detection_accuracy = 0
    false_positives_count = 0

# Preview metrics
if len(filtered_df) > 0:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Activities", len(filtered_df))
    with col2:
        high_risk_count = len(filtered_df[filtered_df['AI Risk Score (0–100)'] >= 70])
        st.metric("High-Risk Activities", high_risk_count)
    with col3:
        st.metric("Detection Accuracy", f"{detection_accuracy}%")
    with col4:
        admin_actions = len(filtered_df[filtered_df['Action'].isin(['False Positive', 'True Positive - Blocked'])])
        st.metric("Admin Actions", admin_actions)
    
    st.markdown("**Sample Data (First 5 rows)**")
    st.dataframe(filtered_df.head(), use_container_width=True, hide_index=True)
else:
    st.warning("No data found for the selected date range")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Activities", 0)
    with col2:
        st.metric("High-Risk Activities", 0)
    with col3:
        st.metric("Detection Accuracy", f"{detection_accuracy}%")
    with col4:
        st.metric("Admin Actions", 0)

st.markdown("---")

# Generate Report Section
st.subheader("🚀 Generate Report")

col1, col2 = st.columns(2)

with col1:
    if st.button("📄 Generate PDF Report", type="primary", use_container_width=True, key="generate_pdf_btn"):
        if len(filtered_df) > 0:
            try:
                with st.spinner("Generating PDF report..."):
                    # Prepare report data
                    report_data = {
                        'title': report_title,
                        'report_id': report_id,
                        'start_date': start_date,
                        'end_date': end_date,
                        'data': filtered_df,
                        'metrics': metrics,
                        'detection_accuracy': detection_accuracy,
                        'false_positives_count': false_positives_count,
                        'include_charts': {
                            'risk_reasons': include_risk_chart,
                            'timeline': include_timeline_chart,
                            'devices': include_device_chart,
                            'geography': include_geo_chart
                        },
                        'include_sections': {
                            'details': include_details,
                            'performance': include_performance,
                            'admin_actions': include_admin_actions
                        },
                        'include_sensitive': include_sensitive
                    }
                    
                    # Generate PDF
                    pdf_path = generate_audit_report(report_data)
                    
                    # Provide download
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            label="⬇️ Download PDF Report",
                            data=pdf_file.read(),
                            file_name=f"{report_id}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                            key="download_pdf_btn"
                        )
                    
                    st.success("Report generated successfully!")
                    
            except Exception as e:
                st.error(f"Error generating report: {e}")
        else:
            st.error("No data available for the selected date range")

with col2:
    if report_format == "PDF + CSV Data":
        if st.button("📊 Download CSV Data", use_container_width=True, key="download_csv_btn"):
            if len(filtered_df) > 0:
                csv_data = filtered_df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv_data,
                    file_name=f"{report_id}_data.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="download_csv_final_btn"
                )
            else:
                st.error("No data available for export")

# Report History
st.markdown("---")
st.subheader("📁 Recent Reports")
st.info("Report generation history will be tracked here in future versions")

# Help Section
with st.expander("❓ Help & Information"):
    st.markdown("""
    **Report Contents:**
    - **Executive Summary**: Overview of security metrics and key findings
    - **Detailed Activity Log**: Complete list of login attempts with risk scores
    - **AI Model Performance**: Detection accuracy and model statistics
    - **Admin Actions Summary**: Review of manual interventions and corrections
    
    **Chart Options:**
    - **Top Risk Reasons**: Bar chart showing most common security threats
    - **Login Timeline**: Activity patterns over time
    - **Device Distribution**: Breakdown by device types
    - **Geographic Distribution**: Login locations analysis
    
    **Best Practices:**
    - Generate reports regularly for compliance documentation
    - Include admin actions to show human oversight
    - Use appropriate date ranges for your audit requirements
    - Keep sensitive data inclusion to minimum necessary
    """)

# Technical note
st.caption("Generated reports are suitable for regulatory compliance and audit requirements")