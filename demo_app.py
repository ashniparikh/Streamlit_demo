# import streamlit as st
# import pandas as pd
# import sqlite3
# import base64
# from datetime import datetime
# import io
# from reportlab.lib.pagesizes import letter
# from reportlab.lib import colors
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.units import inch

# # Set up page configuration
# st.set_page_config(page_title="Diagnostic Tool", layout="wide")

# # Initialize database
# def init_db():
#     conn = sqlite3.connect('diagnostics.db')
#     c = conn.cursor()
    
#     # Create table for diagnostic inputs if it doesn't exist
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS diagnostic_inputs (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             patient_name TEXT,
#             age INTEGER,
#             symptoms TEXT,
#             medical_history TEXT,
#             timestamp DATETIME
#         )
#     ''')
    
#     # Create table for diagnostic results if it doesn't exist
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS diagnostic_results (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             input_id INTEGER,
#             diagnosis TEXT,
#             recommendations TEXT,
#             timestamp DATETIME,
#             FOREIGN KEY (input_id) REFERENCES diagnostic_inputs (id)
#         )
#     ''')
    
#     conn.commit()
#     return conn

# # Function to save diagnostic inputs to database
# def save_inputs(patient_name, age, symptoms, medical_history):
#     conn = init_db()
#     c = conn.cursor()
#     timestamp = datetime.now()
    
#     c.execute('''
#         INSERT INTO diagnostic_inputs (patient_name, age, symptoms, medical_history, timestamp)
#         VALUES (?, ?, ?, ?, ?)
#     ''', (patient_name, age, symptoms, medical_history, timestamp))
    
#     conn.commit()
#     input_id = c.lastrowid
#     conn.close()
    
#     return input_id

# # Function to run diagnostics (simulated)
# def run_diagnostics(symptoms, medical_history, age):
#     # This is a simplified simulation of diagnostic logic
#     # In a real application, this would be more complex and accurate
    
#     common_conditions = {
#         "headache": "Tension headache or migraine",
#         "fever": "Viral infection",
#         "cough": "Upper respiratory infection",
#         "fatigue": "Possible anemia or sleep disorder",
#         "nausea": "Gastroenteritis",
#         "dizziness": "Inner ear disturbance or low blood pressure",
#         "pain": "Inflammatory response",
#         "rash": "Allergic reaction or dermatitis"
#     }
    
#     symptoms_lower = symptoms.lower()
#     diagnosis = []
#     recommendations = []
    
#     for symptom, condition in common_conditions.items():
#         if symptom in symptoms_lower:
#             diagnosis.append(condition)
            
#     if not diagnosis:
#         diagnosis = ["No specific condition identified from symptoms provided"]
    
#     # Add recommendations based on age and medical history
#     if age > 60:
#         recommendations.append("Regular check-ups recommended due to age factor")
    
#     if "diabetes" in medical_history.lower():
#         recommendations.append("Monitor blood sugar levels regularly")
    
#     if "hypertension" in medical_history.lower() or "high blood pressure" in medical_history.lower():
#         recommendations.append("Monitor blood pressure regularly")
    
#     if not recommendations:
#         recommendations.append("General health maintenance recommended")
    
#     return {
#         "diagnosis": ", ".join(diagnosis),
#         "recommendations": "; ".join(recommendations)
#     }

# # Function to save diagnostic results to database
# def save_results(input_id, diagnosis, recommendations):
#     conn = init_db()
#     c = conn.cursor()
#     timestamp = datetime.now()
    
#     c.execute('''
#         INSERT INTO diagnostic_results (input_id, diagnosis, recommendations, timestamp)
#         VALUES (?, ?, ?, ?)
#     ''', (input_id, diagnosis, recommendations, timestamp))
    
#     conn.commit()
#     conn.close()

# # Function to get diagnostic report
# def get_report(input_id):
#     conn = init_db()
#     c = conn.cursor()
    
#     c.execute('''
#         SELECT i.patient_name, i.age, i.symptoms, i.medical_history, i.timestamp,
#                r.diagnosis, r.recommendations, r.timestamp
#         FROM diagnostic_inputs i
#         JOIN diagnostic_results r ON i.id = r.input_id
#         WHERE i.id = ?
#     ''', (input_id,))
    
#     result = c.fetchone()
#     conn.close()
    
#     if result:
#         return {
#             "patient_name": result[0],
#             "age": result[1],
#             "symptoms": result[2],
#             "medical_history": result[3],
#             "input_timestamp": result[4],
#             "diagnosis": result[5],
#             "recommendations": result[6],
#             "result_timestamp": result[7]
#         }
#     return None

# # Function to generate PDF report
# def generate_pdf_report(report_data):
#     buffer = io.BytesIO()
    
#     # Create the PDF document
#     doc = SimpleDocTemplate(buffer, pagesize=letter)
#     styles = getSampleStyleSheet()
    
#     # Custom styles
#     title_style = ParagraphStyle(
#         'Title',
#         parent=styles['Heading1'],
#         fontSize=18,
#         spaceAfter=12
#     )
    
#     heading_style = ParagraphStyle(
#         'Heading',
#         parent=styles['Heading2'],
#         fontSize=14,
#         spaceAfter=6,
#         spaceBefore=12
#     )
    
#     normal_style = styles['Normal']
#     normal_style.fontSize = 10
#     normal_style.spaceAfter = 6
    
#     # Build the PDF content
#     content = []
    
#     # Report header
#     content.append(Paragraph("Diagnostic Report", title_style))
#     content.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
#     content.append(Spacer(1, 0.2*inch))
    
#     # Patient information section
#     content.append(Paragraph("Patient Information", heading_style))
    
#     patient_data = [
#         ["Name:", report_data['patient_name']],
#         ["Age:", str(report_data['age'])],
#     ]
    
#     table = Table(patient_data, colWidths=[1.5*inch, 4*inch])
#     table.setStyle(TableStyle([
#         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#         ('GRID', (0, 0), (-1, -1), 0.25, colors.white),
#         ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
#     ]))
#     content.append(table)
#     content.append(Spacer(1, 0.1*inch))
    
#     # Clinical information section
#     content.append(Paragraph("Clinical Information", heading_style))
    
#     content.append(Paragraph("<b>Symptoms:</b>", normal_style))
#     content.append(Paragraph(report_data['symptoms'], normal_style))
#     content.append(Spacer(1, 0.1*inch))
    
#     content.append(Paragraph("<b>Medical History:</b>", normal_style))
#     content.append(Paragraph(report_data['medical_history'], normal_style))
#     content.append(Spacer(1, 0.2*inch))
    
#     # Diagnostic results section
#     content.append(Paragraph("Diagnostic Results", heading_style))
    
#     diagnostic_data = [
#         ["Diagnosis:", report_data['diagnosis']],
#         ["Recommendations:", report_data['recommendations']]
#     ]
    
#     table = Table(diagnostic_data, colWidths=[1.5*inch, 4*inch])
#     table.setStyle(TableStyle([
#         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#         ('GRID', (0, 0), (-1, -1), 0.25, colors.white),
#         ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
#     ]))
#     content.append(table)
#     content.append(Spacer(1, 0.2*inch))
    
#     # Disclaimer
#     disclaimer_style = ParagraphStyle(
#         'Disclaimer',
#         parent=styles['Italic'],
#         fontSize=8,
#         textColor=colors.gray
#     )
#     content.append(Paragraph("This is an automated report generated for preliminary assessment only. Please consult with a healthcare professional for proper medical advice.", disclaimer_style))
    
#     # Build the PDF
#     doc.build(content)
#     buffer.seek(0)
    
#     return buffer

# # Function to generate downloadable link for PDF
# def get_pdf_download_link(pdf_buffer, filename="diagnostic_report.pdf"):
#     b64 = base64.b64encode(pdf_buffer.getvalue()).decode()
#     href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">Download PDF Report</a>'
#     return href

# # Main application
# def main():
#     st.title("Medical Diagnostic Tool")
    
#     # Initialize session state variables if they don't exist
#     if 'input_id' not in st.session_state:
#         st.session_state.input_id = None
#     if 'report_generated' not in st.session_state:
#         st.session_state.report_generated = False
#     if 'report_data' not in st.session_state:
#         st.session_state.report_data = None
    
#     # Create tabs for different sections
#     tab1, tab2, tab3 = st.tabs(["Input Information", "Run Diagnostics", "Download Report"])
    
#     with tab1:
#         st.header("Patient Information")
        
#         # Input form
#         with st.form("input_form"):
#             patient_name = st.text_input("Patient Name")
#             age = st.number_input("Age", min_value=0, max_value=120, value=30)
#             symptoms = st.text_area("Symptoms (please describe in detail)")
#             medical_history = st.text_area("Medical History")
            
#             submit_button = st.form_submit_button("Save Information")
            
#             if submit_button:
#                 if patient_name and symptoms:
#                     # Save inputs to database
#                     input_id = save_inputs(patient_name, age, symptoms, medical_history)
#                     st.session_state.input_id = input_id
#                     st.success("Information saved successfully! Please proceed to Run Diagnostics tab.")
#                     # Reset report generation status
#                     st.session_state.report_generated = False
#                     st.session_state.report_data = None
#                 else:
#                     st.error("Please provide at least the patient name and symptoms.")
    
#     with tab2:
#         st.header("Run Diagnostics")
        
#         if st.session_state.input_id:
#             conn = init_db()
#             c = conn.cursor()
#             c.execute("SELECT patient_name, age, symptoms, medical_history FROM diagnostic_inputs WHERE id = ?", 
#                      (st.session_state.input_id,))
#             input_data = c.fetchone()
#             conn.close()
            
#             if input_data:
#                 st.subheader("Patient Information")
#                 st.write(f"**Name:** {input_data[0]}")
#                 st.write(f"**Age:** {input_data[1]}")
#                 st.write(f"**Symptoms:** {input_data[2]}")
#                 st.write(f"**Medical History:** {input_data[3]}")
                
#                 if st.button("Run Diagnostic"):
#                     # Run the diagnostic algorithm
#                     results = run_diagnostics(input_data[2], input_data[3], input_data[1])
                    
#                     # Save results to database
#                     save_results(st.session_state.input_id, results["diagnosis"], results["recommendations"])
                    
#                     # Get the full report
#                     report = get_report(st.session_state.input_id)
#                     st.session_state.report_data = report
#                     st.session_state.report_generated = True
                    
#                     # Display the results
#                     st.subheader("Diagnostic Results")
#                     st.write(f"**Diagnosis:** {results['diagnosis']}")
#                     st.write(f"**Recommendations:** {results['recommendations']}")
#                     st.success("Diagnostic complete! You can now download the PDF report in the Download Report tab.")
#         else:
#             st.info("Please complete the Patient Information in the Input Information tab first.")
    
#     with tab3:
#         st.header("Download Report")
        
#         if st.session_state.report_generated and st.session_state.report_data:
#             st.subheader("Report Summary")
#             st.write(f"**Patient:** {st.session_state.report_data['patient_name']}")
#             st.write(f"**Diagnosis:** {st.session_state.report_data['diagnosis']}")
            
#             # Generate PDF report
#             pdf_buffer = generate_pdf_report(st.session_state.report_data)
#             filename = f"diagnostic_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
            
#             # Create download link
#             download_link = get_pdf_download_link(pdf_buffer, filename)
#             st.markdown(download_link, unsafe_allow_html=True)
            
#             st.info("Click the link above to download your PDF report.")
#         else:
#             st.info("Please complete the diagnostic process to generate a report for download.")

# if __name__ == "__main__":
#     main()





####################

# import os
# import sys
# import sqlite3
# import importlib.util
# import streamlit as st
# import html
# import logging
# import toml
# import io
# import base64
# import json
# from reportlab.lib.pagesizes import letter
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
# from reportlab.lib.units import inch
# from datetime import datetime

# # Load and use Streamlit config
# def setup_logging():
#     """Configure logging based on .streamlit/config.toml settings"""
#     try:
#         # Attempt to load the config.toml file
#         config_path = os.path.join('.streamlit', 'config.toml')
#         if os.path.exists(config_path):
#             config = toml.load(config_path)

#             # Get logging settings from config
#             log_level = config.get('logger', {}).get('level', 'info').upper()
#             log_format = config.get('logger', {}).get('messageFormat',
#                                                       '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#             # Check if file logging is enabled
#             enable_file_logging = config.get('logger', {}).get('enableFileLogging', False)
#             log_file_path = config.get('logger', {}).get('logFilePath', 'logs/app.log')

#             # Convert string level to logging level
#             level_map = {
#                 'DEBUG': logging.DEBUG,
#                 'INFO': logging.INFO,
#                 'WARNING': logging.WARNING,
#                 'ERROR': logging.ERROR,
#                 'CRITICAL': logging.CRITICAL
#             }
#             level = level_map.get(log_level, logging.INFO)

#             # Configure basic logging
#             logging.basicConfig(level=level, format=log_format)

#             # Add file handler if enabled
#             if enable_file_logging:
#                 # Ensure log directory exists
#                 log_dir = os.path.dirname(log_file_path)
#                 if log_dir and not os.path.exists(log_dir):
#                     os.makedirs(log_dir)

#                 # Add file handler
#                 file_handler = logging.FileHandler(log_file_path)
#                 file_handler.setFormatter(logging.Formatter(log_format))

#                 # Add to root logger
#                 root_logger = logging.getLogger()
#                 root_logger.addHandler(file_handler)

#             return True
#         else:
#             # Fall back to basic config if no file exists
#             logging.basicConfig(level=logging.INFO,
#                                 format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#             return False
#     except Exception as e:
#         # If anything goes wrong, fall back to basic config
#         logging.basicConfig(level=logging.INFO,
#                             format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#         logging.error(f"Error setting up logging from config: {str(e)}")
#         return False


# # Set up logging from config
# config_loaded = setup_logging()
# logger = logging.getLogger(__name__)

# if config_loaded:
#     logger.info("Logging configured from .streamlit/config.toml")
# else:
#     logger.info("Using default logging configuration")

# # === Page Configuration ===
# st.set_page_config(
#     page_title="Adaptive Traction Architecture Diagnostics",
#     page_icon="🔍",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # === Custom Theme & Styling ===
# # Try to load colors from config or use defaults
# try:
#     config_path = os.path.join('.streamlit', 'config.toml')
#     if os.path.exists(config_path):
#         config = toml.load(config_path)
#         color_config = config.get('colors', {})

#         # Get colors from config or use defaults
#         primary_color = color_config.get('primaryColor', "#233292")
#         secondary_color = color_config.get('secondaryColor', "#26619C")
#         tertiary_color = color_config.get('tertiaryColor', "#385424")
#         quaternary_color = color_config.get('quaternaryColor', "#4D466B")
#         highlight_color = color_config.get('highlightColor', "#AC2147")
#         link_color = color_config.get('linkColor', "#00A8A8")
#     else:
#         # Default colors
#         primary_color = "#233292"  # Deep blue
#         secondary_color = "#26619C"  # Medium blue
#         tertiary_color = "#385424"  # Forest green
#         quaternary_color = "#4D466B"  # Purple-gray
#         highlight_color = "#AC2147"  # Red highlight
#         link_color = "#00A8A8"  # Teal for hyperlinks
# except Exception as e:
#     logger.warning(f"Could not load colors from config, using defaults: {str(e)}")
#     # Default colors
#     primary_color = "#233292"  # Deep blue
#     secondary_color = "#26619C"  # Medium blue
#     tertiary_color = "#385424"  # Forest green
#     quaternary_color = "#4D466B"  # Purple-gray
#     highlight_color = "#AC2147"  # Red highlight
#     link_color = "#00A8A8"  # Teal for hyperlinks

# # Custom CSS for styling - this complements the config.toml settings
# css = """
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
#     @import url('https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,400;0,700;1,400;1,700&display=swap');

#     /* Headers styling with Montserrat font */
#     h1, h2, h3, h4, h5, h6 {
#         font-family: 'Montserrat', sans-serif !important;;
#         font-weight: 600;
#     }
    
#     /* Apply Open Sans to body text */
#     body, p, div, span, li, td, th, button {
#         font-family: 'Open Sans', sans-serif !important;
#     }

#     /* Custom container styling */
#     .dashboard-container {
#         border-radius: 8px;
#         padding: 24px;
#         box-shadow: 0 1px 3px rgba(0,0,0,0.05);
#         margin-bottom: 20px;
#     }
    
#     /* Custom styling for primary buttons */
#     .stButton button[kind="primary"] {
#         background-color: #AD244A;
#         color: white;
#         border: none;
#     }
#     .stButton button[kind="primary"]:hover {
#         background-color: #8f1d3e;  /* Slightly darker shade for hover effect */
#         color: white;
#         border: none;
#     }
    
#     /* Custom styling for secondary buttons */
#     .stButton button[kind="secondary"] {
#         background-color: #f0f2f6;  /* Use a light color for secondary */
#         color: #AD244A;
#         border: 1px solid #AD244A;
#     }
#     .stButton button[kind="secondary"]:hover {
#         background-color: #e5e7eb;  /* Slightly darker shade for hover effect */
#         color: #8f1d3e;
#         border: 1px solid #8f1d3e;
#     }
    
#     /* Custom styling for primary link buttons */
#     .stLinkButton a[kind="primary"] {
#         background-color: #AD244A;
#         color: white;
#         border: none;
#         text-decoration: none;
#     }
    
#     .stLinkButton a[kind="primary"]:hover {
#         background-color: #8f1d3e;  /* Slightly darker shade for hover effect */
#         color: white;
#         border: none;
#         text-decoration: none;
#     }
    
#     /* Custom styling for secondary link buttons */
#     .stLinkButton a[kind="secondary"] {
#         background-color: #f0f2f6;  /* Use a light color for secondary */
#         color: #AD244A;
#         border: 1px solid #AD244A;
#         text-decoration: none;
#     }
    
#     .stLinkButton a[kind="secondary"]:hover {
#         background-color: #e5e7eb;  /* Slightly darker shade for hover effect */
#         color: #8f1d3e;
#         border: 1px solid #8f1d3e;
#         text-decoration: none;
#     }
    
#     /* Success & Info messages */
#     .success {
#         background-color: rgba(56, 84, 36, 0.1);
#         border-left: 4px solid #385424;
#         padding: 15px;
#         border-radius: 4px;
#         margin-bottom: 20px;
#     }

#     .info {
#         background-color: rgba(38, 97, 156, 0.1);
#         border-left: 4px solid #26619C;
#         padding: 15px;
#         border-radius: 4px;
#         margin-bottom: 20px;
#     }

#     .error {
#         background-color: rgba(172, 33, 71, 0.1);
#         border-left: 4px solid #AC2147;
#         padding: 15px;
#         border-radius: 4px;
#         margin-bottom: 20px;
#     }

#     /* Footer styling */    
#     .footer {
#         position: fixed;
#         left: 0;
#         bottom: 0;
#         width: 100%;
#         background-color: #AD244A;
#         color: white;
#         text-align: center;
#         padding: 10px;
#         font-size: 0.8em;
#     }
#     .footer-spacer {
#         height: 40px;
#     }

#     /* Link styling */
#     a {
#         color: #00A8A8 !important;
#         text-decoration: none;
#     }

#     a:hover {
#         text-decoration: underline;
#     }
    
#     /* Download button styling */
#     .download-btn {
#         display: inline-block;
#         padding: 10px 20px;
#         background-color: #26619C;
#         color: white !important;
#         text-decoration: none;
#         border-radius: 5px;
#         font-weight: bold;
#         margin-top: 20px;
#         transition: background-color 0.3s;
#     }
    
#     .download-btn:hover {
#         background-color: #1b4878;
#         text-decoration: none;
#     }
    
#     /* Report summary styling */
#     .report-summary {
#         background-color: #f9f9f9;
#         border-left: 4px solid #26619C;
#         padding: 15px;
#         border-radius: 4px;
#         margin: 20px 0;
#     }
# </style>
# """

# # Apply CSS
# st.markdown(css, unsafe_allow_html=True)


# # === Helper Functions ===
# def add_logo():
#     try:
#         # Create a container with two columns
#         col1, col2 = st.columns([3, 1])

#         with col1:
#             # Left side: App logo (existing)
#             app_logo_html = f"""
#             <div style="display: flex; align-items: center;">
#                 <div style="background-color: {primary_color}; width: 40px; height: 40px; border-radius: 8px; 
#                           display: flex; justify-content: center; align-items: center; margin-right: 12px;">
#                     <span style="color: white; font-weight: bold; font-size: 18px;">ATA</span>
#                 </div>
#                 <div>
#                     <h2 style="margin: 0; padding: 0; color: {primary_color};">Adaptive Traction Architecture</h2>
#                     <p style="margin: 0; padding: 0; font-size: 14px; color: {secondary_color};"> Diagnostics</p>
#                 </div>
#             </div>
#             """
#             st.markdown(app_logo_html, unsafe_allow_html=True)

#         with col2:
#             # Right side: Company logo using st.image
#             import os
#             from PIL import Image

#             # Path to your SVG logo
#             logo_path = os.path.join("media", "Minimalist_Horizontal_Blue.svg")

#             # Display the logo - align it to the right
#             st.image(logo_path, width=200)  # Adjust width as needed

#         logger.debug("Logos rendered successfully")
#     except Exception as e:
#         logger.error(f"Error displaying logos: {str(e)}")
#         st.error(f"Error displaying logos: {str(e)}")


# def import_and_setup_database():
#     """Import the setup_database module and run the setup function"""
#     try:
#         # Check if setup_database.py exists
#         if not os.path.exists('setup_database.py'):
#             logger.error("setup_database.py file not found")
#             st.error("setup_database.py file not found. Please ensure it's in the same directory as app.py.")
#             st.stop()

#         # Import the module dynamically
#         spec = importlib.util.spec_from_file_location("setup_database", "setup_database.py")
#         setup_db_module = importlib.util.module_from_spec(spec)
#         sys.modules["setup_database"] = setup_db_module
#         spec.loader.exec_module(setup_db_module)

#         logger.info("Successfully imported setup_database module")

#         # Run the setup function
#         setup_db_module.setup_database()
#         logger.info("Database setup completed")
#     except Exception as e:
#         logger.error(f"Error setting up database: {str(e)}")
#         st.error(f"Error setting up database: {str(e)}")
#         st.stop()


# def get_db_connection():
#     """Create a database connection and return the connection object"""
#     try:
#         # Check if database exists, if not create it
#         if not os.path.exists('data/traction_diagnostics.db'):
#             logger.warning("Database file not found, attempting to initialize")
#             import_and_setup_database()

#         conn = sqlite3.connect('data/traction_diagnostics.db')
#         conn.row_factory = sqlite3.Row  # This enables column access by name
#         logger.debug("Database connection established")
#         return conn
#     except sqlite3.Error as e:
#         logger.error(f"Database connection error: {str(e)}")
#         st.error(f"Database connection error: {str(e)}")
#         if 'conn' in locals() and conn:
#             conn.close()
#         st.stop()


# def determine_company_stage(revenue):
#     """Query the SQLite database to determine company stage based on revenue"""
#     logger.debug(f"Determining company stage for revenue: ${revenue}M")
#     conn = get_db_connection()
#     try:
#         cursor = conn.cursor()

#         # Query the database for the appropriate growth stage
#         cursor.execute(
#             'SELECT growth_stage_name, description FROM growth_stages WHERE ? BETWEEN low_range AND high_range',
#             (revenue,)
#         )

#         result = cursor.fetchone()

#         if result:
#             logger.info(f"Determined company stage: {result['growth_stage_name']}")
#             return result['growth_stage_name'], result['description']
#         else:
#             # Fallback in case no range matches (shouldn't happen with proper ranges)
#             logger.warning(f"Could not determine company stage for revenue: ${revenue}M")
#             return "Undetermined", "We couldn't determine your company stage. Please contact support."

#     except sqlite3.Error as e:
#         logger.error(f"Database query error: {str(e)}")
#         return "Error", f"An error occurred while determining your company stage: {str(e)}"

#     finally:
#         conn.close()


# def query_problems_by_pillar_and_stage(pillar, stage_name):
#     """Query problems for a specific pillar and growth stage

#     Args:
#         pillar: One of "Product", "Business", "Systems", "Team"
#         stage_name: One of the growth stage names (e.g., "Validation Seekers")

#     Returns:
#         List of problem dictionaries
#     """
#     logger.debug(f"Querying problems for pillar: {pillar}, stage: {stage_name}")
#     conn = get_db_connection()
#     try:
#         cursor = conn.cursor()

#         cursor.execute('''
#         SELECT * FROM architecture_problems 
#         WHERE architecture_pillar = ? AND growth_stage_name = ?
#         ''', (pillar, stage_name))

#         results = [dict(row) for row in cursor.fetchall()]
#         logger.debug(f"Found {len(results)} problems for {pillar} in {stage_name}")
#         return results
#     except sqlite3.Error as e:
#         logger.error(f"Error querying problems: {str(e)}")
#         st.error(f"Error retrieving metrics: {str(e)}")
#         return []
#     finally:
#         conn.close()


# def get_slider_format(metric_name):
#     """Determine the appropriate slider format based on the metric name"""
#     if "CAC Payback Period" in metric_name:
#         return "%d months"
#     elif "Decision turnaround time" in metric_name:
#         return "%d hours"
#     elif "CAC trend" in metric_name:
#         return "%.2f"
#     else:
#         return "%.1f%%"


# def get_slider_range(metric_name):
#     """Determine the appropriate slider range based on the metric name"""
#     if "CAC Payback Period" in metric_name:
#         return (0, 36)  # 0 to 36 months
#     elif "Decision turnaround time" in metric_name:
#         return (0, 168)  # 0 to 168 hours (1 week)
#     elif "CAC trend" in metric_name:
#         return (-1.0, 1.0)  # -1 to 1
#     else:
#         return (0.0, 100.0)  # 0% to 100%


# def get_step_size(metric_name):
#     """Determine the appropriate step size based on the metric name"""
#     if "CAC Payback Period" in metric_name:
#         return 1.0  # Months as decimal
#     elif "Decision turnaround time" in metric_name:
#         return 1.0  # Hours as decimal
#     elif "CAC trend" in metric_name:
#         return 0.1  # 0.1 increments
#     else:
#         return 0.1  # 0.1% increments

# -------------------------------------------------------------------------------------------------------
# def metric_health_assessment(value, low_range, hi_range):
#     """Determine if a metric value is healthy based on the acceptable range"""
#     if low_range < hi_range:
#         # For metrics where higher is better (e.g., conversion rates)
#         if value >= hi_range:
#             return "Excellent"
#         elif value >= low_range:
#             return "Good"
#         else:
#             return "Needs Attention"
#     else:
#         # For metrics where lower is better (e.g., churn rates)
#         if value <= low_range:
#             return "Excellent"
#         elif value <= hi_range:
#             return "Good"
#         else:
#             return "Needs Attention"
# ----------------------------------------------------------------------------------------------------------

# def display_metrics_for_pillar(pillar, growth_stage):
#     """Display metric sliders for a specific pillar and growth stage"""
#     # Get problems/metrics for this pillar and growth stage
#     problems = query_problems_by_pillar_and_stage(pillar, growth_stage)

#     # Initialize metrics data for this pillar if not already done
#     if 'metrics_data' not in st.session_state:
#         st.session_state.metrics_data = {}
#     if pillar not in st.session_state.metrics_data:
#         st.session_state.metrics_data[pillar] = []

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
#             key=slider_key
#         )

#         # Store the metric data for report generation
#         metric_data = {
#             'pillar': pillar,
#             'metric_name': metric_name,
#             'problem_description': problem_description,
#             'value': value,
#             'low_range': problem['low_range'],
#             'hi_range': problem['hi_range'],
#             'units': problem['units'],
#             'health': metric_health_assessment(value, problem['low_range'], problem['hi_range'])
#         }

#         # Update the session state metrics data
#         st.session_state.metrics_data[pillar] = [
#             m for m in st.session_state.metrics_data[pillar] if m['metric_name'] != metric_name
#         ]
#         st.session_state.metrics_data[pillar].append(metric_data)

#         st.markdown("---")


# def generate_report_pdf(company_info, metrics_data):
#     """Generate a PDF report of the diagnostic results
    
#     Args:
#         company_info: Dictionary with company information
#         metrics_data: Dictionary with metrics data by pillar
        
#     Returns:
#         PDF file as bytes
#     """
#     logger.info("Generating PDF report")
    
#     # Create a BytesIO object to store the PDF
#     buffer = io.BytesIO()
    
#     # Create the PDF document
#     doc = SimpleDocTemplate(buffer, pagesize=letter, 
#                            rightMargin=72, leftMargin=72,
#                            topMargin=72, bottomMargin=72)
    
#     # Container for the elements
#     elements = []
    
#     # Styles
#     styles = getSampleStyleSheet()
    
#     # Add custom styles
#     styles.add(ParagraphStyle(name='Title',
#                              fontName='Helvetica-Bold',
#                              fontSize=16,
#                              alignment=1,
#                              spaceAfter=12))
    
#     styles.add(ParagraphStyle(name='Heading2',
#                              fontName='Helvetica-Bold',
#                              fontSize=14,
#                              spaceBefore=12,
#                              spaceAfter=6))
    
#     styles.add(ParagraphStyle(name='Heading3',
#                              fontName='Helvetica-Bold',
#                              fontSize=12,
#                              spaceBefore=10,
#                              spaceAfter=4))
    
#     styles.add(ParagraphStyle(name='Normal',
#                              fontName='Helvetica',
#                              fontSize=10,
#                              spaceBefore=4,
#                              spaceAfter=4))
    
#     # Title
#     elements.append(Paragraph("Adaptive Traction Architecture Diagnostics Report", styles['Title']))
#     elements.append(Spacer(1, 0.2*inch))
    
#     # Date
#     report_date = datetime.now().strftime("%B %d, %Y")
#     elements.append(Paragraph(f"Generated on: {report_date}", styles['Normal']))
#     elements.append(Spacer(1, 0.2*inch))
    
#     # Company Information
#     elements.append(Paragraph("Company Information", styles['Heading2']))
    
#     # Create a table for company info
#     company_data = [
#         ["Company Stage", company_info['stage']],
#         ["Revenue", f"${company_info['revenue']}M ARR"],
#         ["Company Age", f"{company_info['age']} months"]
#     ]
    
#     company_table = Table(company_data, colWidths=[2*inch, 3*inch])
#     company_table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
#         ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
#         ('FONTSIZE', (0, 0), (-1, -1), 10),
#         ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     ]))
    
#     elements.append(company_table)
#     elements.append(Spacer(1, 0.2*inch))
    
#     # Add stage description
#     elements.append(Paragraph("Stage Description:", styles['Heading3']))
#     elements.append(Paragraph(company_info['stage_description'], styles['Normal']))
#     elements.append(Spacer(1, 0.3*inch))
    
#     # Diagnostics Summary
#     elements.append(Paragraph("Diagnostics Summary", styles['Heading2']))
    
#     # Count metrics by health status
#     excellent_count = good_count = needs_attention_count = 0
    
#     for pillar, metrics in metrics_data.items():
#         for metric in metrics:
#             if metric['health'] == 'Excellent':
#                 excellent_count += 1
#             elif metric['health'] == 'Good':
#                 good_count += 1
#             elif metric['health'] == 'Needs Attention':
#                 needs_attention_count += 1
    
#     total_metrics = excellent_count + good_count + needs_attention_count
    
#     # Create a summary paragraph
#     summary_text = f"""
#     Based on the diagnostic assessment, your company has {excellent_count} metrics 
#     in excellent condition, {good_count} metrics in good condition, and {needs_attention_count} metrics 
#     that need attention. This represents {int(100 * (excellent_count + good_count) / total_metrics)}% 
#     of metrics in good or excellent condition.
#     """
    
#     elements.append(Paragraph(summary_text, styles['Normal']))
#     elements.append(Spacer(1, 0.2*inch))
    
#     # Detailed Results by Pillar
#     elements.append(Paragraph("Detailed Results by Pillar", styles['Heading2']))
    
#     # Process each pillar
#     for pillar in ['Business', 'Product', 'Systems', 'Team']:
#         if pillar in metrics_data and metrics_data[pillar]:
#             elements.append(Paragraph(f"{pillar} Pillar", styles['Heading3']))
            
#             # Create table header
#             data = [["Metric", "Value", "Health"]]
            
#             # Add each metric to the table
#             for metric in metrics_data[pillar]:
#                 # Format the value based on the units
#                 if metric['units'] == 'Percentage':
#                     value_formatted = f"{metric['value']:.1f}%"
#                 elif metric['units'] == 'Months':
#                     value_formatted = f"{int(metric['value'])} months"
#                 elif metric['units'] == 'Hours':
#                     value_formatted = f"{int(metric['value'])} hours"
#                 elif metric['units'] == 'Trend':
#                     if metric['value'] > 0:
#                         value_formatted = f"+{metric['value']:.2f} (increasing)"
#                     elif metric['value'] < 0:
#                         value_formatted = f"{metric['value']:.2f} (decreasing)"
#                     else:
#                         value_formatted = "0.00 (flat)"
#                 else:
#                     value_formatted = f"{metric['value']:.1f}"
                
#                 data.append([metric['metric_name'], value_formatted, metric['health']])
            
#             # Create the table
#             table = Table(data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
            
#             # Define table style
#             table_style = [
#                 ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#                 ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#                 ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                 ('FONTSIZE', (0, 0), (-1, 0), 10),
#                 ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#                 ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ]
            
#             # Add colors for health status
#             for i in range(1, len(data)):
#                 health_status = data[i][2]
#                 if health_status == 'Excellent':
#                     table_style.append(('BACKGROUND', (2, i), (2, i), colors.lightgreen))
#                 elif health_status == 'Good':
#                     table_style.append(('BACKGROUND', (2, i), (2, i), colors.lightblue))
#                 elif health_status == 'Needs Attention':
#                     table_style.append(('BACKGROUND', (2, i), (2, i), colors.salmon))
            
#             table.setStyle(TableStyle(table_style))
#             elements.append(table)
#             elements.append(Spacer(1, 0.2*inch))
            
#             # Add problem descriptions for metrics that need attention
#             attention_metrics = [m for m in metrics_data[pillar] if m['health'] == 'Needs Attention']
#             if attention_metrics:
#                 elements.append(Paragraph("Areas Needing Attention:", styles['Heading3']))
#                 for metric in attention_metrics:






########################
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
#             key=slider_key
#         )

#         st.markdown("---")




# def setup_database():
#     """Main function to set up the entire database"""
#     try:
#         logger.info("Starting database setup")
#         create_growth_stages_table()
#         create_architecture_problems_table()
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
