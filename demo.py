# # Add these imports at the top with the other imports
# import pandas as pd
# from datetime import datetime
# import base64
# import io
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib import colors
# from reportlab.lib.units import inch
# import matplotlib.pyplot as plt
# from io import BytesIO
# import matplotlib
# matplotlib.use('Agg')  # Use non-interactive backend

# Add this function after get_db_connection() function
# def generate_diagnostic_report(company_info, metrics_data):
#     """Generate a diagnostic report based on user inputs and metrics"""
#     logger.info("Generating diagnostic report")
    
#     # Create a DataFrame to store the metrics data for analysis
#     report_data = {
#         'Pillar': [],
#         'Metric': [],
#         'Current Value': [],
#         'Target Range': [],
#         'Status': []
#     }
    
#     # Process each metric
#     for metric_info in metrics_data:
#         pillar = metric_info['pillar']
#         metric_name = metric_info['metric_name']
#         current_value = metric_info['current_value']
#         low_range = metric_info['low_range']
#         hi_range = metric_info['hi_range']
#         units = metric_info['units']
        
#         # Determine status based on current value and target range
#         if low_range <= current_value <= hi_range:
#             status = "Good"
#         elif current_value < low_range:
#             status = "Below Target"
#         else:
#             status = "Above Target"
        
#         # Format the value based on units
#         if units == "Percentage":
#             formatted_value = f"{current_value:.1f}%"
#             formatted_range = f"{low_range:.1f}% - {hi_range:.1f}%"
#         elif units == "Months":
#             formatted_value = f"{int(current_value)} months"
#             formatted_range = f"{int(low_range)} - {int(hi_range)} months"
#         elif units == "Days":
#             formatted_value = f"{int(current_value)} days"
#             formatted_range = f"{int(low_range)} - {int(hi_range)} days"
#         elif units == "Hours":
#             formatted_value = f"{int(current_value)} hours"
#             formatted_range = f"{int(low_range)} - {int(hi_range)} hours"
#         elif units == "Trend":
#             if current_value < 0:
#                 formatted_value = "Decreasing"
#             elif current_value > 0:
#                 formatted_value = "Increasing"
#             else:
#                 formatted_value = "Flat"
#             formatted_range = "Recommended: " + ("Decreasing" if hi_range <= 0 else "Increasing" if low_range >= 0 else "Flat")
#         elif units == "Ratio":
#             formatted_value = f"{current_value:.1f}"
#             formatted_range = f"{low_range:.1f} - {hi_range:.1f}"
#         else:
#             formatted_value = f"{current_value:.1f}"
#             formatted_range = f"{low_range:.1f} - {hi_range:.1f}"
        
#         # Add to report data
#         report_data['Pillar'].append(pillar)
#         report_data['Metric'].append(metric_name)
#         report_data['Current Value'].append(formatted_value)
#         report_data['Target Range'].append(formatted_range)
#         report_data['Status'].append(status)
    
#     # Create DataFrame
#     df = pd.DataFrame(report_data)
    
#     # Calculate summary statistics
#     metrics_count = len(df)
#     good_count = len(df[df['Status'] == 'Good'])
#     below_target_count = len(df[df['Status'] == 'Below Target'])
#     above_target_count = len(df[df['Status'] == 'Above Target'])
    
#     # Calculate percentages
#     good_percent = (good_count / metrics_count) * 100 if metrics_count > 0 else 0
    
#     # Generate summary text
#     summary = {
#         'metrics_count': metrics_count,
#         'good_count': good_count,
#         'good_percent': good_percent,
#         'below_target_count': below_target_count,
#         'above_target_count': above_target_count,
#         'company_stage': company_info['stage'],
#         'revenue': company_info['revenue'],
#         'months_existed': company_info['months_existed'],
#         'date': datetime.now().strftime('%Y-%m-%d'),
#         'data': df
#     }
    
#     logger.info(f"Report generated: {good_count}/{metrics_count} metrics in good range ({good_percent:.1f}%)")
    
#     return summary

# Add this function after generate_diagnostic_report()
# def create_pdf_report(report_data):
#     """Create a PDF report from the diagnostic data"""
#     logger.info("Creating PDF report")
    
#     # Create a buffer to store the PDF
#     buffer = io.BytesIO()
    
#     # Create the PDF document
#     doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
#     # Get styles
#     styles = getSampleStyleSheet()
#     title_style = styles['Heading1']
#     subtitle_style = styles['Heading2']
#     normal_style = styles['Normal']
    
#     # Create a custom style for headers
#     header_style = ParagraphStyle(
#         'Header',
#         parent=styles['Heading3'],
#         textColor=colors.HexColor("#233292"),
#         spaceAfter=12
#     )
    
#     # Create a list to hold the PDF elements
#     elements = []
    
#     # Add title
#     elements.append(Paragraph("Adaptive Traction Architecture Diagnostics Report", title_style))
#     elements.append(Spacer(1, 0.25*inch))
    
#     # Add date
#     elements.append(Paragraph(f"Report Date: {report_data['date']}", normal_style))
#     elements.append(Spacer(1, 0.25*inch))
    
#     # Add company info
#     elements.append(Paragraph("Company Information", subtitle_style))
#     elements.append(Paragraph(f"Company Age: {report_data['months_existed']} months", normal_style))
#     elements.append(Paragraph(f"Annual Revenue: ${report_data['revenue']:.2f}M", normal_style))
#     elements.append(Paragraph(f"Growth Stage: {report_data['company_stage']}", normal_style))
#     elements.append(Spacer(1, 0.25*inch))
    
#     # Add summary
#     elements.append(Paragraph("Diagnostic Summary", subtitle_style))
#     elements.append(Paragraph(f"Total Metrics Evaluated: {report_data['metrics_count']}", normal_style))
#     elements.append(Paragraph(f"Metrics in Target Range: {report_data['good_count']} ({report_data['good_percent']:.1f}%)", normal_style))
#     elements.append(Paragraph(f"Metrics Below Target: {report_data['below_target_count']}", normal_style))
#     elements.append(Paragraph(f"Metrics Above Target: {report_data['above_target_count']}", normal_style))
#     elements.append(Spacer(1, 0.5*inch))
    
#     # Create a summary chart
#     fig, ax = plt.figure(figsize=(6, 4)), plt.axes()
#     statuses = ['In Target Range', 'Below Target', 'Above Target']
#     counts = [report_data['good_count'], report_data['below_target_count'], report_data['above_target_count']]
#     colors_pie = ['#385424', '#AC2147', '#26619C']
    
#     ax.pie(counts, labels=statuses, colors=colors_pie, autopct='%1.1f%%', startangle=90)
#     ax.axis('equal')
#     plt.title('Metrics Status Distribution')
    
#     # Save the chart to a BytesIO object
#     img_buffer = BytesIO()
#     plt.savefig(img_buffer, format='png', dpi=100)
#     img_buffer.seek(0)
#     plt.close()
    
#     # Add the chart to the PDF
#     img = RLImage(img_buffer, width=5*inch, height=3*inch)
#     elements.append(img)
#     elements.append(Spacer(1, 0.5*inch))
    
#     # Group metrics by pillar
#     df = report_data['data']
#     for pillar in ['Business', 'Product', 'Systems', 'Team']:
#         pillar_data = df[df['Pillar'] == pillar]
        
#         if not pillar_data.empty:
#             elements.append(Paragraph(f"{pillar} Pillar Metrics", header_style))
            
#             # Create a table for this pillar's metrics
#             table_data = [['Metric', 'Current Value', 'Target Range', 'Status']]
            
#             for _, row in pillar_data.iterrows():
#                 status_color = colors.green if row['Status'] == 'Good' else colors.red
#                 table_data.append([
#                     row['Metric'],
#                     row['Current Value'],
#                     row['Target Range'],
#                     row['Status']
#                 ])
            
#             # Create the table
#             table = Table(table_data, colWidths=[2.5*inch, 1.25*inch, 1.5*inch, 1*inch])
            
#             # Style the table
#             table_style = TableStyle([
#                 ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#233292")),
#                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#                 ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                 ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                 ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#                 ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#                 ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ])
            
#             # Apply conditional formatting for status column
#             for i in range(1, len(table_data)):
#                 if table_data[i][3] == 'Good':
#                     table_style.add('TEXTCOLOR', (3, i), (3, i), colors.green)
#                     table_style.add('FONTNAME', (3, i), (3, i), 'Helvetica-Bold')
#                 else:
#                     table_style.add('TEXTCOLOR', (3, i), (3, i), colors.red)
#                     table_style.add('FONTNAME', (3, i), (3, i), 'Helvetica-Bold')
            
#             table.setStyle(table_style)
#             elements.append(table)
#             elements.append(Spacer(1, 0.25*inch))
    
#     # Add recommendations section
#     elements.append(Paragraph("Recommendations", subtitle_style))
    
#     # Generate basic recommendations based on metrics that need improvement
#     needs_improvement = df[df['Status'] != 'Good']
    
#     if needs_improvement.empty:
#         elements.append(Paragraph("All metrics are within target ranges. Continue monitoring and maintaining current practices.", normal_style))
#     else:
#         elements.append(Paragraph("Focus on improving the following areas:", normal_style))
        
#         for _, row in needs_improvement.iterrows():
#             elements.append(Paragraph(f"• {row['Metric']} - Currently at {row['Current Value']} (Target: {row['Target Range']})", normal_style))
        
#     # Add footer
#     elements.append(Spacer(1, 1*inch))
#     elements.append(Paragraph(f"© {datetime.now().year} Minimalist Innovation LLC. All rights reserved.", normal_style))
    
#     # Build the PDF
#     doc.build(elements)
#     buffer.seek(0)
    
#     logger.info("PDF report created successfully")
#     return buffer

# # Add this function after create_pdf_report()
# def get_download_link(buffer, filename):
#     """Generate a download link for the given buffer and filename"""
#     b64 = base64.b64encode(buffer.getvalue()).decode()
#     return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}" class="download-btn">Download Report</a>'




# Now we need to modify the main() function to incorporate these new features. Add the following code within the main() function, right after the "Run Diagnostics" button:

# # Add this inside the main() function after the "Run Diagnostics" button
# if st.button("Run Diagnostics", type="primary"):
#     logger.info("Run Diagnostics button clicked")
    
#     # Collect all the metrics values from session state
#     metrics_data = []
#     for key, value in st.session_state.items():
#         if key.startswith(("Business_", "Product_", "Systems_", "Team_")):
#             # Parse the key to extract pillar and ID
#             parts = key.split('_')
#             pillar = parts[0]
#             problem_id = parts[1]
            
#             # Query the database to get the full problem info
#             conn = get_db_connection()
#             cursor = conn.cursor()
#             cursor.execute('SELECT * FROM architecture_problems WHERE id = ?', (problem_id,))
#             problem_info = cursor.fetchone()
#             conn.close()
            
#             if problem_info:
#                 metrics_data.append({
#                     'pillar': pillar,
#                     'problem_id': problem_id,
#                     'metric_name': problem_info['metric_name'],
#                     'current_value': value,
#                     'low_range': problem_info['low_range'],
#                     'hi_range': problem_info['hi_range'],
#                     'units': problem_info['units']
#                 })
    
#     # Store the company information
#     company_info = {
#         'stage': stage,
#         'revenue': annual_revenue,
#         'months_existed': months_existed
#     }
    
#     # Generate the diagnostic report
#     report_data = generate_diagnostic_report(company_info, metrics_data)
    
#     # Store the report in session state
#     st.session_state['report_data'] = report_data
    
#     # Display a summary of the report
#     st.success("Diagnostic analysis complete!")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         st.markdown("<div class='info'>", unsafe_allow_html=True)
#         st.markdown(f"#### Report Summary")
#         st.markdown(f"**Growth Stage:** {report_data['company_stage']}")
#         st.markdown(f"**Metrics in Target Range:** {report_data['good_count']} out of {report_data['metrics_count']} ({report_data['good_percent']:.1f}%)")
#         st.markdown("</div>", unsafe_allow_html=True)
    
#     with col2:
#         # Create a figure for the pie chart
#         fig, ax = plt.subplots(figsize=(4, 4))
#         statuses = ['In Target Range', 'Below Target', 'Above Target']
#         counts = [report_data['good_count'], report_data['below_target_count'], report_data['above_target_count']]
#         colors_pie = ['#385424', '#AC2147', '#26619C']
        
#         ax.pie(counts, labels=statuses, colors=colors_pie, autopct='%1.1f%%', startangle=90)
#         ax.axis('equal')
#         st.pyplot(fig)
    
#     # Create a download button for the PDF report
#     pdf_buffer = create_pdf_report(report_data)
    
#     # Use markdown to display the download button with custom styling
#     download_link = get_download_link(pdf_buffer, f"ATA_Diagnostics_Report_{datetime.now().strftime('%Y%m%d')}.pdf")
#     st.markdown(download_link, unsafe_allow_html=True)

# # Add after the "Run Diagnostics" button and its related code
# elif 'report_data' in st.session_state:
#     # If a report was previously generated, show the download button again
#     st.success("Your diagnostic report is ready for download.")
    
#     # Recreate the PDF buffer
#     pdf_buffer = create_pdf_report(st.session_state['report_data'])
    
#     # Display the download link again
#     download_link = get_download_link(pdf_buffer, f"ATA_Diagnostics_Report_{datetime.now().strftime('%Y%m%d')}.pdf")
#     st.markdown(download_link, unsafe_allow_html=True)


# # Also, we need to initialize the session state when the app starts. Add this at the beginning of the main() function:

# # Add this near the beginning of the main() function, after add_logo()
# if 'report_data' not in st.session_state:
#     st.session_state['report_data'] = None

# # Finally, let's update the display_metrics_for_pillar function to store metrics in the session state:
# # Modify the display_metrics_for_pillar function to store values in session state
# def display_metrics_for_pillar(pillar, growth_stage):
#     """Display metric sliders for a specific pillar and growth stage"""
#     # Get problems/metrics for this pillar and growth stage
#     problems = query_problems_by_pillar_and_stage(pillar, growth_stage)

#     if not problems:
#         logger.warning(f"No metrics found for {pillar} in {growth_stage} stage")
#         st.write(f"No metrics found for {pillar} in {growth_stage} stage.")
#         return

#     # Display each metric with a slider
#     for problem in problems:
#         # Escape the metric name and problem description
#         metric_name = html.escape(problem['metric_name'])
#         problem_description = html.escape(problem['problem_description'])

#         # Display the metric name and problem description with bold for the metric name
#         st.markdown(f"**{metric_name}**")
#         st.markdown(f"{problem_description}")

#         # Create a unique key for each slider
#         slider_key = f"{pillar}_{problem['id']}_{problem['metric_name']}"
        
#         # Simplified key for session state
#         session_key = f"{pillar}_{problem['id']}"

#         # Get appropriate format and range for this metric
#         slider_format = get_slider_format(problem['metric_name'])
#         min_val, max_val = get_slider_range(problem['metric_name'])
#         step_size = get_step_size(problem['metric_name'])

#         # Determine default value based on the rules
#         if min_val != problem['low_range']:
#             default_value = problem['low_range']
#         elif max_val != problem['hi_range']:
#             default_value = problem['hi_range']
#         else:
#             # If no special case, use the midpoint or appropriate default
#             if "CAC trend" in problem['metric_name']:
#                 default_value = 0.0  # Default to flat for CAC trend
#             else:
#                 default_value = (problem['low_range'] + problem['hi_range']) / 2

#         # Ensure default is within bounds
#         default_value = max(min_val, min(max_val, default_value))

#         logger.debug(f"Creating slider for metric: {metric_name}, range: {min_val}-{max_val}, default: {default_value}")

#         # Create the slider with appropriate format
#         value = st.slider(
#             f"**Current value**",
#             min_value=float(min_val),
#             max_value=float(max_val),
#             value=float(default_value),
#             step=step_size,
#             format=slider_format,
#             key=session_key
#         )

#         st.markdown("---")




# # For setup_database.py, we don't need significant changes since our main implementation happens in app.py. However, for completeness, let's add a function that could be used to store report results in the database if needed in the future:

# # Add this function at the end of setup_database.py, before if __name__ == "__main__":
# def create_reports_table():
#     """Create a table to store generated reports"""
#     try:
#         # Connect to the database
#         conn = sqlite3.connect('data/traction_diagnostics.db')
#         cursor = conn.cursor()

#         # Create the reports table
#         cursor.execute('''
#         CREATE TABLE IF NOT EXISTS diagnostic_reports (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             report_date DATETIME NOT NULL,
#             company_stage TEXT NOT NULL,
#             revenue DECIMAL(10,2) NOT NULL,
#             months_existed INTEGER NOT NULL,
#             good_metrics_count INTEGER NOT NULL,
#             total_metrics_count INTEGER NOT NULL,
#             report_data TEXT NOT NULL  -- JSON string of the full report data
#         )
#         ''')

#         # Commit changes and close connection
#         conn.commit()
#         conn.close()

#         logger.info("Reports table created successfully")
#     except Exception as e:
#         logger.error(f"Error creating reports table: {str(e)}")
#         raise

# # Update the setup_database function to include the new reports table
# def setup_database():
#     """Main function to set up the entire database"""
#     try:
#         logger.info("Starting database setup")
#         create_growth_stages_table()
#         create_architecture_problems_table()
#         create_reports_table()  # Add this line
#         logger.info("Database setup completed successfully")
#         # For Streamlit integration, log a message in the UI as well
#         if runtime.exists():
#             st.success("Database setup completed successfully")
#     except Exception as e:
#         logger.error(f"Database setup failed: {str(e)}")
#         # For Streamlit integration, show error in the UI as well
#         if runtime.exists():
#             st.error(f"Database setup failed: {str(e)}")
#         raise