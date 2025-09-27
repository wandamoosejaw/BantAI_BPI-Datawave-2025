from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import pandas as pd
from datetime import datetime
import os

def generate_audit_report(report_data):
    """Generate comprehensive audit report PDF"""
    
    # Create filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/BantAI_Audit_Report_{timestamp}.pdf"
    
    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)
    
    # Create PDF document
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2c3e50')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.HexColor('#34495e')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    # Build PDF content
    story = []
    
    # Title Page
    story.append(Paragraph(report_data['title'], title_style))
    story.append(Spacer(1, 12))
    
    # Report metadata
    story.append(Paragraph(f"<b>Report ID:</b> {report_data['report_id']}", normal_style))
    story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    story.append(Paragraph(f"<b>Date Range:</b> {report_data['start_date']} to {report_data['end_date']}", normal_style))
    story.append(Paragraph(f"<b>System:</b> BantAI - Filipino-Centric AI Security Agent", normal_style))
    story.append(Spacer(1, 30))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    
    df = report_data['data']
    total_activities = len(df)
    high_risk_activities = len(df[df['AI Risk Score (0–100)'] >= 70]) if total_activities > 0 else 0
    admin_actions = len(df[df['Action'].isin(['False Positive', 'True Positive - Blocked'])]) if total_activities > 0 else 0
    
    summary_data = [
        ['Metric', 'Value'],
        ['Total Login Activities Analyzed', f"{total_activities:,}"],
        ['High-Risk Activities Detected', f"{high_risk_activities:,}"],
        ['AI Detection Accuracy', f"{report_data['detection_accuracy']}%"],
        ['False Positives (7 days)', f"{report_data['false_positives_count']:,}"],
        ['Admin Actions Taken', f"{admin_actions:,}"]
    ]
    
    if total_activities > 0:
        summary_data.extend([
            ['Attack IP Attempts', f"{len(df[df['is_attack_ip'] == True]):,}"],
            ['Failed Login Attempts', f"{len(df[df['login_successful'] == False]):,}"]
        ])
    
    summary_table = Table(summary_data, colWidths=[3*inch, 1.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7'))
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 20))
    
    # Key Findings
    story.append(Paragraph("Key Security Findings", heading_style))
    
    risk_percentage = (high_risk_activities / total_activities * 100) if total_activities > 0 else 0
    accuracy = report_data['detection_accuracy']
    
    findings = []
    if risk_percentage > 10:
        findings.append(f"• High risk activity rate: {risk_percentage:.1f}% requires attention")
    else:
        findings.append(f"• Risk activity rate: {risk_percentage:.1f}% within normal parameters")
    
    if accuracy >= 95:
        findings.append(f"• AI detection accuracy of {accuracy}% exceeds performance targets")
    elif accuracy >= 85:
        findings.append(f"• AI detection accuracy of {accuracy}% meets minimum requirements")
    else:
        findings.append(f"• AI detection accuracy of {accuracy}% requires model retraining")
    
    if admin_actions > 0:
        findings.append(f"• {admin_actions} activities required manual review and intervention")
    
    for finding in findings:
        story.append(Paragraph(finding, normal_style))
    
    story.append(PageBreak())
    
    # AI Model Performance Section
    if report_data['include_sections']['performance']:
        story.append(Paragraph("AI Model Performance Analysis", heading_style))
        
        performance_data = [
            ['Metric', 'Value', 'Status'],
            ['Detection Accuracy', f"{accuracy}%", 'Excellent' if accuracy >= 95 else 'Good' if accuracy >= 85 else 'Needs Improvement'],
            ['Total Predictions Made', f"{total_activities:,}", 'Active'],
            ['Model Feedback Loop', f"{admin_actions} reviews", 'Active' if admin_actions > 0 else 'Limited']
        ]
        
        if total_activities > 0:
            high_confidence = len(df[df['AI Risk Score (0–100)'] >= 80])
            performance_data.append(['High Confidence Predictions', f"{high_confidence:,}", f"{high_confidence/total_activities*100:.1f}%"])
            performance_data.append(['False Positive Rate', f"{report_data['false_positives_count']/(total_activities or 1)*100:.1f}%", 'Within Tolerance'])
        
        performance_table = Table(performance_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
        performance_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ebf3fd')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7'))
        ]))
        
        story.append(performance_table)
        story.append(Spacer(1, 20))
    
    # Admin Actions Summary
    if report_data['include_sections']['admin_actions'] and admin_actions > 0:
        story.append(Paragraph("Administrative Actions Summary", heading_style))
        
        false_positives = len(df[df['Action'] == 'False Positive']) if total_activities > 0 else 0
        true_positives = len(df[df['Action'] == 'True Positive - Blocked']) if total_activities > 0 else 0
        
        admin_summary = [
            ['Action Type', 'Count', 'Percentage'],
            ['False Positive Corrections', f"{false_positives:,}", f"{false_positives/admin_actions*100:.1f}%" if admin_actions > 0 else "0%"],
            ['True Positive Confirmations', f"{true_positives:,}", f"{true_positives/admin_actions*100:.1f}%" if admin_actions > 0 else "0%"],
            ['Total Administrative Reviews', f"{admin_actions:,}", "100%"]
        ]
        
        admin_table = Table(admin_summary, colWidths=[2.5*inch, 1*inch, 1*inch])
        admin_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fdf2f2')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7'))
        ]))
        
        story.append(admin_table)
        story.append(Spacer(1, 20))
    
    # Detailed Activity Log
    if report_data['include_sections']['details'] and total_activities > 0:
        story.append(PageBreak())
        story.append(Paragraph("Detailed Activity Log", heading_style))
        
        # Prepare data for table
        columns_to_include = [
            'User ID', 'Login Timestamp (UTC+8)', 'Country', 'City', 
            'AI Risk Score (0–100)', 'device_type', 'Action'
        ]
        
        display_df = df[columns_to_include].copy()
        
        if not report_data['include_sensitive']:
            # Anonymize user data
            display_df['User ID'] = display_df['User ID'].apply(lambda x: f"USER_{hash(str(x)) % 10000:04d}")
        
        # Create table data
        table_data = [columns_to_include]
        for _, row in display_df.head(50).iterrows():  # Limit to 50 rows for PDF
            table_data.append([str(row[col]) for col in columns_to_include])
        
        if len(display_df) > 50:
            table_data.append(['...'] * len(columns_to_include))
            table_data.append([f'Showing 50 of {len(display_df)} total records'] + [''] * (len(columns_to_include) - 1))
        
        # Create table with smaller font for data
        detail_table = Table(table_data, repeatRows=1)
        detail_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        story.append(detail_table)
    
    # Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        f"Report generated by BantAI Security System | Confidential Banking Security Analysis | Page generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, alignment=TA_CENTER, textColor=colors.grey)
    ))
    
    # Build PDF
    doc.build(story)
    
    return filename