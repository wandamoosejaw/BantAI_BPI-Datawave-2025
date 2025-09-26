# utils/charts.py
import streamlit as st
import altair as alt
import pandas as pd

def login_attempts_vs_flags_chart():
    """Create the line chart matching the Figma design"""
    df = pd.DataFrame({
        'Time': list(range(10)),
        'Login_Attempts': [0, 100, 90, 50, 80, 100, 10, 75, 50, 100],
        'High_Risk_Flags': [0, 25, 10, 75, 25, 0, 25, 50, 25, 75]
    })
    
    # Melt the dataframe for proper visualization
    df_melted = df.melt('Time', var_name='Type', value_name='Count')
    
    # Create the line chart with better integration
    chart = alt.Chart(df_melted).mark_line(
        strokeWidth=2,
        point=True
    ).encode(
        x=alt.X('Time:O', 
                axis=alt.Axis(title='', grid=True, gridColor='#f0f0f0', labelFontSize=12)),
        y=alt.Y('Count:Q', 
                scale=alt.Scale(domain=[0, 100]),
                axis=alt.Axis(title='', grid=True, gridColor='#f0f0f0', labelFontSize=12)),
        color=alt.Color(
            'Type:N',
            scale=alt.Scale(
                domain=['Login_Attempts', 'High_Risk_Flags'],
                range=['#e74c3c', '#2c3e50']
            ),
            legend=alt.Legend(
                title=None,
                orient='top-right',
                direction='vertical',
                labelFontSize=12
            )
        )
    ).resolve_scale(
        color='independent'
    ).properties(
        height=250,
        width=500
    )
    
    # Use container width but with better sizing
    st.altair_chart(chart, use_container_width=True, theme=None)

def top_risk_reasons_chart():
    """Create the bar chart matching the Figma design"""
    df = pd.DataFrame({
        'Reason': ['Impossible Travel', 'Attack IP', 'Unusual Device', 'Failed OTP'],
        'Count': [400, 500, 250, 950]
    })
    
    # Define colors for each bar to match Figma
    colors = ['#17a2b8', '#ffc107', '#fd7e14', '#28a745']
    
    chart = alt.Chart(df).mark_bar(
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3
    ).encode(
        x=alt.X('Reason:N', 
                axis=alt.Axis(title='', labelAngle=0, labelFontSize=12),
                sort='-y'),
        y=alt.Y('Count:Q', 
                axis=alt.Axis(title='', grid=True, gridColor='#f0f0f0', labelFontSize=12),
                scale=alt.Scale(domain=[0, 1000])),
        color=alt.Color(
            'Reason:N',
            scale=alt.Scale(
                domain=['Impossible Travel', 'Attack IP', 'Unusual Device', 'Failed OTP'],
                range=colors
            ),
            legend=None
        )
    ).properties(
        height=250,
        width=400
    )
    
    st.altair_chart(chart, use_container_width=True, theme=None)

def login_outcomes_pie_chart():
    """Create the pie chart matching the Figma design"""
    df = pd.DataFrame({
        'Outcome': ['Successful', 'Failed'],
        'Count': [800, 200]
    })
    
    chart = alt.Chart(df).mark_arc(
        innerRadius=40,
        outerRadius=80,
        stroke='white',
        strokeWidth=2
    ).encode(
        theta=alt.Theta('Count:Q'),
        color=alt.Color(
            'Outcome:N',
            scale=alt.Scale(
                domain=['Successful', 'Failed'],
                range=['#17a2b8', '#fd7e14']
            ),
            legend=alt.Legend(
                title=None,
                orient='bottom',
                direction='horizontal',
                symbolType='circle',
                symbolSize=100,
                labelFontSize=12
            )
        )
    ).properties(
        height=180,
        width=180
    )
    
    st.altair_chart(chart, use_container_width=True, theme=None)