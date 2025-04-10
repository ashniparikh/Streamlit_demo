# import streamlit as st
# # Inject custom CSS to change the background color
# st.markdown( 
#     """ 
#     <style> 
#     .reportview-container { 
#         background-color: black; 
#     } 
#     </style> 
#     """, 
#     unsafe_allow_html=True
#     )
# # Set the title of the app
# st.title("Streamlit App with Markdown Field")
# # Display a Markdown field
# st.markdown(""" 
#     # Welcome to the Streamlit App 
    
#     This is an example of a simple app with a Markdown field. 
    
#     ## Features: 
#     - Display text in **Markdown** format 
#     - Support for *italic*, **bold**, and other text formatting options. 
    
#     ### Code Example: 
#     ```python 
#     import streamlit as st 
#     st.markdown("Hello, **Streamlit!**") 
#     ``` 
    
#     - You can even include links: [Streamlit Website](https://www.youtube.com/watch?v=PnRFjKgiWWU)""")


import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import sqlite3
import importlib.util
import streamlit as st
import html
import logging
import toml


# Load and use Streamlit config
def setup_logging():
    """Configure logging based on .streamlit/config.toml settings"""
    try:
        # Attempt to load the config.toml file
        config_path = os.path.join('.streamlit', 'config.toml')
        if os.path.exists(config_path):
            config = toml.load(config_path)

            # Get logging settings from config
            log_level = config.get('logger', {}).get('level', 'info').upper()
            log_format = config.get('logger', {}).get('messageFormat',
                                                      '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            # Check if file logging is enabled
            enable_file_logging = config.get('logger', {}).get('enableFileLogging', False)
            log_file_path = config.get('logger', {}).get('logFilePath', 'logs/app.log')

            # Convert string level to logging level
            level_map = {
                'DEBUG': logging.DEBUG,
                'INFO': logging.INFO,
                'WARNING': logging.WARNING,
                'ERROR': logging.ERROR,
                'CRITICAL': logging.CRITICAL
            }
            level = level_map.get(log_level, logging.INFO)

            # Configure basic logging
            logging.basicConfig(level=level, format=log_format)

            # Add file handler if enabled
            if enable_file_logging:
                # Ensure log directory exists
                log_dir = os.path.dirname(log_file_path)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir)

                # Add file handler
                file_handler = logging.FileHandler(log_file_path)
                file_handler.setFormatter(logging.Formatter(log_format))

                # Add to root logger
                root_logger = logging.getLogger()
                root_logger.addHandler(file_handler)

            return True
        else:
            # Fall back to basic config if no file exists
            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            return False
    except Exception as e:
        # If anything goes wrong, fall back to basic config
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.error(f"Error setting up logging from config: {str(e)}")
        return False


# Set up logging from config
config_loaded = setup_logging()
logger = logging.getLogger(__name__)

if config_loaded:
    logger.info("Logging configured from .streamlit/config.toml")
else:
    logger.info("Using default logging configuration")

# === Page Configuration ===
st.set_page_config(
    page_title="Adaptive Traction Architecture Diagnostics",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# === Custom Theme & Styling ===
# Try to load colors from config or use defaults
try:
    config_path = os.path.join('.streamlit', 'config.toml')
    if os.path.exists(config_path):
        config = toml.load(config_path)
        color_config = config.get('colors', {})

        # Get colors from config or use defaults
        primary_color = color_config.get('primaryColor', "#233292")
        secondary_color = color_config.get('secondaryColor', "#26619C")
        tertiary_color = color_config.get('tertiaryColor', "#385424")
        quaternary_color = color_config.get('quaternaryColor', "#4D466B")
        highlight_color = color_config.get('highlightColor', "#AC2147")
        link_color = color_config.get('linkColor', "#00A8A8")
    else:
        # Default colors
        primary_color = "#233292"  # Deep blue
        secondary_color = "#26619C"  # Medium blue
        tertiary_color = "#385424"  # Forest green
        quaternary_color = "#4D466B"  # Purple-gray
        highlight_color = "#AC2147"  # Red highlight
        link_color = "#00A8A8"  # Teal for hyperlinks
except Exception as e:
    logger.warning(f"Could not load colors from config, using defaults: {str(e)}")
    # Default colors
    primary_color = "#233292"  # Deep blue
    secondary_color = "#26619C"  # Medium blue
    tertiary_color = "#385424"  # Forest green
    quaternary_color = "#4D466B"  # Purple-gray
    highlight_color = "#AC2147"  # Red highlight
    link_color = "#00A8A8"  # Teal for hyperlinks

# Custom CSS for styling - this complements the config.toml settings
css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,400;0,700;1,400;1,700&display=swap');

    /* Headers styling with Montserrat font */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
    }

    /* Custom container styling */
    .dashboard-container {
        border-radius: 8px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* Success & Info messages */
    .success {
        background-color: rgba(56, 84, 36, 0.1);
        border-left: 4px solid #385424;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 20px;
    }

    .info {
        background-color: rgba(38, 97, 156, 0.1);
        border-left: 4px solid #26619C;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 20px;
    }

    .error {
        background-color: rgba(172, 33, 71, 0.1);
        border-left: 4px solid #AC2147;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 20px;
    }

    /* Link styling */
    a {
        color: #00A8A8 !important;
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }
</style>
"""

# Apply CSS
st.markdown(css, unsafe_allow_html=True)
# === Helper Functions ===
def add_logo():
    try:
        # Create a simple logo using text and styling
        logo_html = f"""
        <div style="display: flex; align-items: center; margin-bottom: 24px;">
            <div style="background-color: {primary_color}; width: 40px; height: 40px; border-radius: 8px; 
                      display: flex; justify-content: center; align-items: center; margin-right: 12px;">
                <span style="color: white; font-weight: bold; font-size: 18px;">ATA</span>
            </div>
            <div>
                <h2 style="margin: 0; padding: 0; color: {primary_color};">Adaptive Traction Architecture</h2>
                <p style="margin: 0; padding: 0; font-size: 14px; color: {secondary_color};"> Diagnostics</p>
            </div>
        </div>
        """
        st.markdown(logo_html, unsafe_allow_html=True)
        logger.debug("Logo rendered successfully")
    except Exception as e:
        logger.error(f"Error displaying logo: {str(e)}")
        st.error(f"Error displaying logo: {str(e)}")

# === App Layout ===
def main():
    try:
        # logger.info("Starting Adaptive Traction Architecture Diagnostics app")

        # Add logo
        add_logo()

        # About Adaptive Traction Architecture
        st.markdown("<div class='dashboard-container'>", unsafe_allow_html=True)

        about_markdown = """
        ### About Adaptive Traction Architecture

        Adaptive Traction Architecture™ is a comprehensive framework designed for B2C and B2B2C SaaS startups making \\$1M - \\$10M ARR that face specific growth challenges. It builds four key pillars that work together to help startups maintain momentum through market shifts: Products That Adapt, Business Models That Work, Teams That Respond, and Systems That Scale. This architectural approach enables startups to detect and respond to market changes without losing traction.

        ### About the Diagnostics Framework

        The Adaptive Traction Architecture Diagnostics tool is a powerful assessment platform that shows what's really holding your business back. It provides a clear view of your startup's health across 10 key areas including Product-Market Fit, Retention, Acquisition, and more. The framework helps you identify what's driving growth, what's slowing you down, and which bets are worth making next, enabling smarter, data-driven decisions.
        """
        st.markdown(about_markdown)
        st.markdown("</div>", unsafe_allow_html=True)

        # Basic interactivity for demo purposes
        st.markdown("<div class='dashboard-container'>", unsafe_allow_html=True)
        st.markdown("<h3>Start Your Diagnostics</h3>", unsafe_allow_html=True)

        # Ask for company existence duration
        months_existed = st.number_input("How long has your company been in existence? (months)",
                                         min_value=1, max_value=240, value=12)
        logger.debug(f"Company existence duration input: {months_existed} months")

        # Revenue input based on company age
        if months_existed < 24:
            # For newer companies, ask for MRR and convert to ARR
            mrr = st.slider("**Monthly Recurring Revenue (MRR in \\$K)**",
                            min_value=0.0,
                            max_value=1000.0,
                            value=83.33,  # This equals ~$1M ARR
                            step=20.83,  # This equals ~$250K ARR (0.25M)
                            format="$%.2fK")

            # Convert MRR (in thousands) to ARR (in millions)
            annual_revenue = (mrr * 12) / 1000
            logger.debug(f"MRR input: ${mrr}K, converted to ARR: ${annual_revenue}M")

            # Display the converted ARR value
            st.info(f"**Your estimated Annual Recurring Revenue (ARR): __\\${annual_revenue:.2f}M__**")
        else:
            # For established companies, ask directly for ARR
            annual_revenue = st.slider("**Annual Recurring Revenue (ARR in \\$M)**",
                                       min_value=0.0,
                                       max_value=12.0,
                                       value=1.5,
                                       step=0.25,
                                       format="$%.2fM")
            logger.debug(f"ARR input: ${annual_revenue}M")

        # Warning for revenue > 10M
        if annual_revenue > 10.0:
            logger.info(f"ARR exceeds $10M: ${annual_revenue}M")
            st.warning(
                "Your revenue exceeds \\$10M ARR. This diagnostic tool is primarily designed for companies in the \\$1M-\\$10M ARR range. Some insights may not apply to your current scale.")

        # # Determine company stage using the database
        # stage, explanation = determine_company_stage(annual_revenue)

        # # Display stage with styling based on qualification
        # if stage == "Pre-Qualification":
        #     logger.info(f"Company stage determined as Pre-Qualification (ARR: ${annual_revenue}M)")
        #     st.markdown(f"<div class='error'><strong>Company Stage: {stage}</strong><br>{explanation}</div>",
        #                 unsafe_allow_html=True)
        # else:
        #     logger.info(f"Company stage determined as {stage} (ARR: ${annual_revenue}M)")
        #     st.markdown(f"<div class='success'><strong>Company Stage: {stage}</strong></div>", unsafe_allow_html=True)
        #     st.markdown(f"<div class='info'>{explanation}</div>", unsafe_allow_html=True)

        #     # Only show diagnostic options if qualified
        #     if stage != "Pre-Qualification":
        #         st.markdown("<h4>Four Pillars of Adaptive Traction Architecture</h4>", unsafe_allow_html=True)

        #         # Create tabs for the four pillars
        #         logger.debug("Creating pillar tabs")
        #         pillars_tabs = st.tabs(["Business/Revenue", "Product", "Systems", "Team"])

        #         # Business pillar tab
        #         with pillars_tabs[0]:
        #             st.markdown(
        #                 "**Evaluates your acquisition channels, pricing strategy, customer journey, and revenue resilience to identify patterns limiting growth or creating vulnerability to market shifts.**")

        #             logger.debug("Displaying Business pillar metrics")
        #             display_metrics_for_pillar("Business", stage)

        #         # Product pillar tab
        #         with pillars_tabs[1]:
        #             st.markdown(
        #                 "**Assesses your product development approach, feedback mechanisms, feature adoption patterns, and market responsiveness to reveal gaps between product evolution and market needs.**")

        #             logger.debug("Displaying Product pillar metrics")
        #             display_metrics_for_pillar("Product", stage)

        #         # Systems pillar tab
        #         with pillars_tabs[2]:
        #             st.markdown(
        #                 "**Examines your operational processes, technology infrastructure, data accessibility, and technical debt to identify inefficiencies and scalability constraints.**")

        #             logger.debug("Displaying Systems pillar metrics")
        #             display_metrics_for_pillar("Systems", stage)

        #         # Team pillar tab
        #         with pillars_tabs[3]:
        #             st.markdown(
        #                 "**Explores your decision-making frameworks, information flow patterns, organizational structure, and change management capabilities to uncover bottlenecks limiting adaptive capacity.**")

        #             logger.debug("Displaying Team pillar metrics")
        #             display_metrics_for_pillar("Team", stage)

        #         if st.button("Run Diagnostics"):
        #             logger.info("Run Diagnostics button clicked")
        #             st.success("Diagnostic analysis complete!")

        # st.markdown("</div>", unsafe_allow_html=True)
        # logger.info("App rendered successfully")

    except Exception as e:
        logger.error(f"An error occurred in the main app flow: {str(e)}", exc_info=True)
        st.error(f"An error occurred: {str(e)}")
        st.info("Please refresh the page and try again.")

if __name__ == '__main__':
    try:
        # Make sure the database is set up
        # import_and_setup_database()
        main()
    except Exception as e:
        logger.critical(f"Fatal error in app startup: {str(e)}", exc_info=True)
        st.error(f"Fatal error: {str(e)}")