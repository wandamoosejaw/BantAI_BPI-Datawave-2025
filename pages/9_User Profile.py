import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.style import inject_custom_css
from utils.database import (
    get_user_timeline_data, get_user_info, get_user_stats, 
    get_user_location_patterns, get_user_device_patterns, get_user_risk_trends
)
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

st.set_page_config(page_title="User Profile & Timeline", layout="wide")
inject_custom_css()

st.title("👤 User Profile & Timeline Analysis")
st.markdown("Visualize user behavior patterns and AI learning over time")

# Get list of users for dropdown
try:
    conn = st.connection('sql', type='sqlite3', url='bantai_security.db')
    users_query = "SELECT user_id, username FROM users ORDER BY username"
    users_df = conn.query(users_query)
except:
    # Fallback to direct database connection
    import sqlite3
    conn_db = sqlite3.connect('bantai_security.db')
    users_df = pd.read_sql_query("SELECT user_id, username FROM users ORDER BY username", conn_db)
    conn_db.close()

if users_df.empty:
    st.error("❌ No users found in database. Please initialize the database first.")
    st.info("💡 Go to Admin Control to simulate some login activities first.")
    st.stop()

# User selection interface
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    selected_user_id = st.selectbox(
        "🔍 Select User:",
        options=users_df['user_id'].tolist(),
        format_func=lambda x: f"{users_df[users_df['user_id'] == x]['username'].iloc[0]} ({x})"
    )

with col2:
    if st.button("🔄 Refresh Data", type="secondary", use_container_width=True):
        st.rerun()

with col3:
    if st.button("⚙️ Admin Control", type="primary", use_container_width=True):
        st.switch_page("pages/7_Admin_Control.py")

if not selected_user_id:
    st.warning("⚠️ Please select a user to view their profile.")
    st.stop()

# Load user data
with st.spinner("📊 Loading user profile data..."):
    try:
        user_info = get_user_info(selected_user_id)
        user_stats = get_user_stats(selected_user_id)
        timeline_df = get_user_timeline_data(selected_user_id)
        
        if user_info is None:
            st.error(f"❌ User {selected_user_id} not found!")
            st.stop()
            
    except Exception as e:
        st.error(f"❌ Error loading user data: {e}")
        st.info("💡 Try refreshing the page or check if the database is properly initialized.")
        st.stop()

# User Info Header
st.markdown("---")
user_header_col1, user_header_col2 = st.columns([3, 1])

with user_header_col1:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 25px; border-radius: 15px; color: white; margin-bottom: 20px;">
        <h2 style="margin: 0; color: white;">👤 {user_info['username']}</h2>
        <p style="margin: 8px 0; opacity: 0.9; font-size: 1.1rem;">📧 {user_info['email']}</p>
        <p style="margin: 5px 0; opacity: 0.9;">🏠 Home Locations: {', '.join(user_info['home_locations'])}</p>
        <p style="margin: 5px 0; opacity: 0.9;">📱 Common Devices: {', '.join(user_info['common_devices'])}</p>
    </div>
    """, unsafe_allow_html=True)

with user_header_col2:
    current_time = datetime.now().strftime("%H:%M:%S")
    st.metric("🕐 Profile Status", f"Live {current_time}", help="Real-time profile monitoring")

# User Statistics Dashboard
st.subheader("📊 User Statistics Overview")
stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)

with stats_col1:
    st.metric(
        "Total Logins", 
        user_stats['total_logins'],
        help="Total number of login attempts"
    )

with stats_col2:
    risk_delta = f"{user_stats['high_risk']} high-risk events"
    st.metric(
        "High Risk Events", 
        user_stats['high_risk'],
        delta=risk_delta if user_stats['high_risk'] > 0 else "None detected",
        delta_color="inverse"
    )

with stats_col3:
    st.metric(
        "Countries Visited", 
        user_stats['countries'],
        help="Number of unique countries accessed from"
    )

with stats_col4:
    behavior_delta = "Good" if user_stats['avg_behavior'] >= 80 else "Needs Review"
    st.metric(
        "Avg Behavior Score", 
        f"{user_stats['avg_behavior']}%",
        delta=behavior_delta,
        delta_color="normal" if user_stats['avg_behavior'] >= 80 else "inverse"
    )

if timeline_df.empty:
    st.warning("⚠️ No login activities found for this user.")
    st.info("💡 Use the Admin Control panel to simulate some login activities for this user.")
    
    # Quick action buttons when no data
    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    quick_col1, quick_col2 = st.columns(2)
    
    with quick_col1:
        if st.button("🧪 Simulate Login Activities", use_container_width=True):
            st.switch_page("pages/7_Admin_Control.py")
    
    with quick_col2:
        if st.button("📊 View All Activities", use_container_width=True):
            st.switch_page("pages/3_Recent Login Activities.py")
    
    st.stop()

# Timeline Visualization Section
st.markdown("---")
st.subheader("📈 Login Timeline & Risk Analysis")
st.markdown("Interactive timeline showing login patterns, risk scores, and AI behavioral learning")

def create_timeline_chart(df):
    """Create interactive timeline chart matching BantAI style"""
    fig = go.Figure()
    
    # Color mapping for risk levels
    color_map = {
        'LOW': '#10b981',    # Green
        'MEDIUM': '#f59e0b',  # Orange/Yellow
        'HIGH': '#ef4444'     # Red
    }
    
    # Add data points for each risk level
    for risk_level in ['LOW', 'MEDIUM', 'HIGH']:
        risk_data = df[df['risk_classification'] == risk_level]
        if not risk_data.empty:
            fig.add_trace(go.Scatter(
                x=risk_data['login_timestamp'],
                y=risk_data['risk_percentage'],
                mode='markers+lines',
                name=f'{risk_level} Risk',
                marker=dict(
                    color=color_map[risk_level],
                    size=12,
                    symbol='circle',
                    line=dict(width=2, color='white')
                ),
                line=dict(color=color_map[risk_level], width=3),
                hovertemplate=(
                    '<b>%{customdata[0]}</b><br>'
                    'Time: %{x}<br>'
                    'Risk: %{y:.1f}%<br>'
                    'Location: %{customdata[1]}, %{customdata[2]}<br>'
                    'Device: %{customdata[3]}<br>'
                    'Action: %{customdata[4]}<br>'
                    'Behavior: %{customdata[5]}%<br>'
                    '<extra></extra>'
                ),
                customdata=risk_data[['city', 'country', 'city', 'device_type', 'recommended_action', 'behavior_consistency']].values
            ))
    
    # Customize layout
    fig.update_layout(
        title='🔍 Login Risk Timeline - AI Behavioral Analysis',
        xaxis_title='Timeline',
        yaxis_title='Risk Percentage (%)',
        hovermode='closest',
        height=450,
        showlegend=True,
        template='plotly_white',
        plot_bgcolor='rgba(248, 250, 252, 0.8)',
        paper_bgcolor='rgba(255, 255, 255, 0.9)'
    )
    
    # Add risk threshold lines
    fig.add_hline(
        y=30, 
        line_dash="dash", 
        line_color="orange", 
        annotation_text="Medium Risk Threshold (30%)",
        annotation_position="top right"
    )
    fig.add_hline(
        y=70, 
        line_dash="dash", 
        line_color="red", 
        annotation_text="High Risk Threshold (70%)",
        annotation_position="top right"
    )
    
    return fig

# Display timeline chart
timeline_chart = create_timeline_chart(timeline_df)
st.plotly_chart(timeline_chart, use_container_width=True)

# Analysis Charts Section
st.markdown("---")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📍 Login Locations")
    
    # Location frequency analysis
    location_counts = timeline_df.groupby(['country', 'city']).size().reset_index(name='count')
    location_counts['location'] = location_counts['city'] + ', ' + location_counts['country']
    
    if not location_counts.empty:
        location_fig = px.bar(
            location_counts.sort_values('count', ascending=True).tail(8),
            x='count',
            y='location',
            orientation='h',
            title='🌍 Most Frequent Login Locations',
            color='count',
            color_continuous_scale='viridis',
            text='count'
        )
        location_fig.update_layout(
            height=350,
            showlegend=False,
            template='plotly_white'
        )
        location_fig.update_traces(textposition='outside')
        st.plotly_chart(location_fig, use_container_width=True)
    else:
        st.info("No location data available")

    # Behavior consistency chart
    st.subheader("📈 Behavior Consistency")
    
    # Group by date and average behavior consistency
    daily_behavior = timeline_df.groupby('date')['behavior_consistency'].mean().reset_index()
    daily_behavior['date'] = pd.to_datetime(daily_behavior['date'])
    
    if not daily_behavior.empty:
        behavior_fig = go.Figure()
        
        behavior_fig.add_trace(go.Scatter(
            x=daily_behavior['date'],
            y=daily_behavior['behavior_consistency'],
            mode='lines+markers',
            name='Behavior Consistency',
            line=dict(color='#3b82f6', width=4),
            marker=dict(size=10, color='#3b82f6'),
            fill='tonexty',
            fillcolor='rgba(59, 130, 246, 0.1)',
            hovertemplate='Date: %{x}<br>Consistency: %{y:.1f}%<extra></extra>'
        ))
        
        behavior_fig.update_layout(
            title='🧠 AI Behavioral Learning Over Time',
            xaxis_title='Date',
            yaxis_title='Consistency (%)',
            height=350,
            template='plotly_white',
            yaxis=dict(range=[0, 100])
        )
        
        # Add consistency threshold
        behavior_fig.add_hline(
            y=80, 
            line_dash="dash", 
            line_color="green", 
            annotation_text="Good Consistency (80%)"
        )
        
        st.plotly_chart(behavior_fig, use_container_width=True)
    else:
        st.info("Insufficient data for behavior analysis")

with chart_col2:
    st.subheader("📱 Device Usage")
    
    # Device usage distribution
    device_counts = timeline_df['device_type'].value_counts()
    
    if not device_counts.empty:
        device_fig = px.pie(
            values=device_counts.values,
            names=device_counts.index,
            title='💻 Device Distribution',
            color_discrete_map={
                'mobile': '#10b981',
                'desktop': '#3b82f6',
                'tablet': '#f59e0b'
            },
            hole=0.4
        )
        device_fig.update_layout(height=350, template='plotly_white')
        device_fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(device_fig, use_container_width=True)
    else:
        st.info("No device data available")

    # Recent Activities Summary
    st.subheader("🕒 Recent Activities")
    recent_activities = timeline_df.tail(5)[['login_timestamp', 'city', 'country', 'risk_classification', 'recommended_action']]
    recent_activities['login_timestamp'] = recent_activities['login_timestamp'].dt.strftime('%Y-%m-%d %H:%M')
    
    for _, activity in recent_activities.iterrows():
        risk_emoji = {'LOW': '🟢', 'MEDIUM': '🟡', 'HIGH': '🔴'}
        action_emoji = {'ALLOW': '✅', 'ALLOW_WITH_OTP': '⚠️', 'BLOCK': '❌'}
        
        st.markdown(f"""
        <div style="border-left: 4px solid #3b82f6; padding: 12px; margin: 8px 0; background: #f8fafc; border-radius: 5px;">
            <b>{activity['login_timestamp']}</b><br>
            📍 {activity['city']}, {activity['country']}<br>
            {risk_emoji.get(activity['risk_classification'], '⚪')} Risk: {activity['risk_classification']} 
            {action_emoji.get(activity['recommended_action'], '❓')} Action: {activity['recommended_action']}
        </div>
        """, unsafe_allow_html=True)

# Detailed Analysis Section
st.markdown("---")
st.subheader("📋 Detailed Login History")

# Filters for the detailed table
filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    risk_filter = st.selectbox("Filter by Risk:", ["All", "LOW", "MEDIUM", "HIGH"])

with filter_col2:
    countries_list = ["All"] + timeline_df['country'].unique().tolist()
    country_filter = st.selectbox("Filter by Country:", countries_list)

with filter_col3:
    days_filter = st.selectbox("Show last:", [7, 14, 30, 90, 365])

# Apply filters
filtered_df = timeline_df.copy()

if risk_filter != "All":
    filtered_df = filtered_df[filtered_df['risk_classification'] == risk_filter]

if country_filter != "All":
    filtered_df = filtered_df[filtered_df['country'] == country_filter]

# Date filter
cutoff_date = datetime.now() - timedelta(days=days_filter)
filtered_df = filtered_df[filtered_df['login_timestamp'] >= cutoff_date]

# Display filtered table
if not filtered_df.empty:
    display_df = filtered_df[['login_timestamp', 'city', 'country', 'device_type', 
                            'risk_percentage', 'risk_classification', 'recommended_action', 
                            'behavior_consistency', 'admin_action']].copy()
    
    display_df['login_timestamp'] = display_df['login_timestamp'].dt.strftime('%Y-%m-%d %H:%M')
    display_df = display_df.sort_values('login_timestamp', ascending=False)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "risk_percentage": st.column_config.ProgressColumn(
                "Risk %",
                help="Risk percentage from AI analysis",
                min_value=0,
                max_value=100,
                format="%.1f%%"
            ),
            "behavior_consistency": st.column_config.ProgressColumn(
                "Behavior %",
                help="Behavioral consistency score",
                min_value=0,
                max_value=100,
                format="%.0f%%"
            ),
            "login_timestamp": "Login Time",
            "city": "City",
            "country": "Country",
            "device_type": "Device",
            "risk_classification": "Risk Level",
            "recommended_action": "AI Action",
            "admin_action": "Admin Status"
        }
    )
else:
    st.info("🔍 No activities match the selected filters.")

# Export and Navigation
st.markdown("---")
st.subheader("📥 Export & Navigation")

export_col1, export_col2, export_col3 = st.columns(3)

with export_col1:
    if st.button("📄 Download Timeline CSV", use_container_width=True):
        csv = timeline_df.to_csv(index=False)
        st.download_button(
            label="💾 Download CSV File",
            data=csv,
            file_name=f"user_{selected_user_id}_timeline_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

with export_col2:
    if st.button("📊 View All Activities", use_container_width=True):
        st.switch_page("pages/3_Recent Login Activities.py")

with export_col3:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/1_BantAI Dashboard.py")

# Footer
st.markdown("---")
st.caption("🤖 BantAI User Profile & Timeline Analysis | AI-Powered Behavioral Pattern Recognition")

# Display AI insights for demo purposes
if selected_user_id == "U_TEST_001" and not timeline_df.empty:
    st.markdown("---")
    st.subheader("🇵🇭 Filipino Context Demo")
    
    st.success("""
    ✅ **Demo Timeline Loaded**: U_TEST_001 shows typical Filipino user patterns:
    
    • **Metro Manila Commute**: Regular Makati ↔ Taguig office travel
    • **Weekend Activities**: Shopping in Mandaluyong  
    • **Social Visits**: Evening login from Pasig (friend's place)
    • **Extended Metro Travel**: Visit to Parañaque (south Metro Manila)
    • **Consistent Behavior**: All activities show LOW risk with high behavior consistency
    
    This timeline demonstrates how BantAI learns normal user patterns and would flag anomalies.
    """)