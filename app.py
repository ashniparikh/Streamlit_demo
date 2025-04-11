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
# import matplotlib.pyplot as plt
# import seaborn as sns
import base64
import sqlite3
import importlib.util
import streamlit as st
import html
import logging
import toml

def import_and_setup_database():
    """Import the setup_database module and run the setup function"""
    try:
        # Check if setup_database.py exists
        if not os.path.exists('setup_database.py'):
            # logger.error("setup_database.py file not found")
            st.error("setup_database.py file not found. Please ensure it's in the same directory as app.py.")
            st.stop()

        # Import the module dynamically
        spec = importlib.util.spec_from_file_location("setup_database", "setup_database.py")
        setup_db_module = importlib.util.module_from_spec(spec)
        sys.modules["setup_database"] = setup_db_module
        spec.loader.exec_module(setup_db_module)

        # logger.info("Successfully imported setup_database module")

        # Run the setup function
        setup_db_module.setup_database()
        # logger.info("Database setup completed")
    except Exception as e:
        # logger.error(f"Error setting up database: {str(e)}")
        st.error(f"Error setting up database: {str(e)}")
        st.stop()

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
        # logger.debug("Logo rendered successfully")
    except Exception as e:
        # logger.error(f"Error displaying logo: {str(e)}")
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
        # logger.debug(f"Company existence duration input: {months_existed} months")

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
            # logger.debug(f"MRR input: ${mrr}K, converted to ARR: ${annual_revenue}M")

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
            # logger.debug(f"ARR input: ${annual_revenue}M")

        # Warning for revenue > 10M
        if annual_revenue > 10.0:
            # logger.info(f"ARR exceeds $10M: ${annual_revenue}M")
            st.warning(
                "Your revenue exceeds \\$10M ARR. This diagnostic tool is primarily designed for companies in the \\$1M-\\$10M ARR range. Some insights may not apply to your current scale.")

        # # Determine company stage using the database
        # stage, explanation = determine_company_stage(annual_revenue)

        # # Display stage with styling based on qualification
        # if stage == "Pre-Qualification":
        #     # logger.info(f"Company stage determined as Pre-Qualification (ARR: ${annual_revenue}M)")
        #     st.markdown(f"<div class='error'><strong>Company Stage: {stage}</strong><br>{explanation}</div>",
        #                 unsafe_allow_html=True)
        # else:
        #     # logger.info(f"Company stage determined as {stage} (ARR: ${annual_revenue}M)")
        #     st.markdown(f"<div class='success'><strong>Company Stage: {stage}</strong></div>", unsafe_allow_html=True)
        #     st.markdown(f"<div class='info'>{explanation}</div>", unsafe_allow_html=True)

        #     # Only show diagnostic options if qualified
        #     if stage != "Pre-Qualification":
        #         st.markdown("<h4>Four Pillars of Adaptive Traction Architecture</h4>", unsafe_allow_html=True)

        #         # Create tabs for the four pillars
        #         # logger.debug("Creating pillar tabs")
        #         pillars_tabs = st.tabs(["Business/Revenue", "Product", "Systems", "Team"])

        #         # Business pillar tab
        #         with pillars_tabs[0]:
        #             st.markdown(
        #                 "**Evaluates your acquisition channels, pricing strategy, customer journey, and revenue resilience to identify patterns limiting growth or creating vulnerability to market shifts.**")

        #             # logger.debug("Displaying Business pillar metrics")
        #             display_metrics_for_pillar("Business", stage)

        #         # Product pillar tab
        #         with pillars_tabs[1]:
        #             st.markdown(
        #                 "**Assesses your product development approach, feedback mechanisms, feature adoption patterns, and market responsiveness to reveal gaps between product evolution and market needs.**")

        #             # logger.debug("Displaying Product pillar metrics")
        #             display_metrics_for_pillar("Product", stage)

        #         # Systems pillar tab
        #         with pillars_tabs[2]:
        #             st.markdown(
        #                 "**Examines your operational processes, technology infrastructure, data accessibility, and technical debt to identify inefficiencies and scalability constraints.**")

        #             # logger.debug("Displaying Systems pillar metrics")
        #             display_metrics_for_pillar("Systems", stage)

        #         # Team pillar tab
        #         with pillars_tabs[3]:
        #             st.markdown(
        #                 "**Explores your decision-making frameworks, information flow patterns, organizational structure, and change management capabilities to uncover bottlenecks limiting adaptive capacity.**")

        #             # logger.debug("Displaying Team pillar metrics")
        #             display_metrics_for_pillar("Team", stage)

        #         if st.button("Run Diagnostics"):
        #             # logger.info("Run Diagnostics button clicked")
        #             st.success("Diagnostic analysis complete!")

        # st.markdown("</div>", unsafe_allow_html=True)
        # # logger.info("App rendered successfully")

    except Exception as e:
        # logger.error(f"An error occurred in the main app flow: {str(e)}", exc_info=True)
        st.error(f"An error occurred: {str(e)}")
        st.info("Please refresh the page and try again.")

if __name__ == '__main__':
    try:
        # Make sure the database is set up
        import_and_setup_database()
        main()
    except Exception as e:
        # logger.critical(f"Fatal error in app startup: {str(e)}", exc_info=True)
        st.error(f"Fatal error: {str(e)}")