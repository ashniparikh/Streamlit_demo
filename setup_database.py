import sqlite3
import os
import logging
from streamlit import runtime
import streamlit as st

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def create_growth_stages_table():
    """Create the SQLite database and populate the growth_stages table"""
    try:
        # Check if the data directory exists, if not create it
        if not os.path.exists('data'):
            os.makedirs('data')
            logger.info("Created 'data' directory")

        # Connect to the database (creates it if it doesn't exist)
        conn = sqlite3.connect('data/traction_diagnostics.db')
        cursor = conn.cursor()

        # Create the growth_stages table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS growth_stages (
            id INTEGER PRIMARY KEY,
            growth_stage_name TEXT NOT NULL,
            description TEXT NOT NULL,
            low_range DECIMAL(10,2) NOT NULL,
            high_range DECIMAL(10,2) NOT NULL
        )
        ''')

        # Clear existing data to avoid duplicates if we run this script multiple times
        cursor.execute('DELETE FROM growth_stages')
        logger.debug("Cleared existing growth stages data")

        # Insert growth stage data
        growth_stages = [
            (1, 'Pre-Qualification',
             'Your company is still in the early stages with less than $1M ARR. This diagnostics tool is designed for companies with $1M+ ARR. We recommend focusing on product-market fit and initial traction before using this diagnostic tool.',
             0.00, 0.99),
            (2, 'Validation Seekers',
             'Your company is in the Validation Seekers stage ($1M-$2M ARR). At this stage, you\'re likely establishing early monetization with some paying customers, but may be encountering your first serious growth plateau or realizing early traction was a false signal.',
             0.99, 1.99),
            (3, 'Traction Builders',
             'Your company is in the Traction Builders stage ($2M-$4M ARR). You\'ve achieved early validation but may have hit a plateau in growth. You might be experimenting with positioning or pricing pivots without clarity.',
             1.99, 3.99),
            (4, 'Scale Preparers',
             'Your company is in the Scale Preparers stage ($4M-$7M ARR). You may be stuck in \'hiring solves everything\' mode, but growth has stalled. You could be questioning whether your initial model can scale or needs a pivot.',
             3.99, 6.99),
            (5, 'Growth Accelerators',
             'Your company is in the Growth Accelerators stage ($7M-$10M ARR). You\'re likely facing internal chaos from rapid scaling and unclear priorities, and may be unsure if you should push deeper into your core or pivot to a broader opportunity.',
             6.99, 10.00),
            (6, 'Expansion Navigators',
             'Your company is in the Expansion Navigators stage ($10M+ ARR). You\'re likely reaching the upper bounds of your initial market and expanding into adjacent opportunities.',
             10.01, 999.99)
        ]

        cursor.executemany('INSERT INTO growth_stages VALUES (?, ?, ?, ?, ?)', growth_stages)
        logger.info(f"Inserted {len(growth_stages)} growth stages")

        # Commit changes and close connection
        conn.commit()
        conn.close()

        logger.info("Growth stages table created successfully")
    except Exception as e:
        logger.error(f"Error creating growth stages table: {str(e)}")
        raise


def create_architecture_problems_table():
    """Create the SQLite table for architecture problems based on the spreadsheet structure"""
    try:
        # Check if the data directory exists, if not create it
        if not os.path.exists('data'):
            os.makedirs('data')
            logger.info("Created 'data' directory")

        # Connect to the database (creates it if it doesn't exist)
        conn = sqlite3.connect('data/traction_diagnostics.db')
        cursor = conn.cursor()

        # Create the architecture_problems table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS architecture_problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            architecture_pillar TEXT NOT NULL,       -- Business/Revenue, Product, Systems, Team
            growth_stage_name TEXT NOT NULL,         -- Aligned with growth_stages table (e.g., Validation Seekers)
            problem_description TEXT NOT NULL,       -- Description of the problem
            metric_name TEXT NOT NULL,               -- Name of the metric to measure
            low_range DECIMAL(10,2),                -- Lower threshold value
            hi_range DECIMAL(10,2),                 -- Upper threshold value
            min_range DECIMAL(10,2),                -- Minimum possible value for this metric
            max_range DECIMAL(10,2),                -- Maximum possible value for this metric
            units TEXT NOT NULL                     -- Percentage, Days, Ratio, etc.
        )
        ''')

        # Create an index for faster lookups by pillar and growth stage
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_pillar_stage 
        ON architecture_problems (architecture_pillar, growth_stage_name)
        ''')

        # Check if table already has data
        cursor.execute("SELECT COUNT(*) FROM architecture_problems")
        count = cursor.fetchone()[0]

        if count > 0:
            logger.info(f"Architecture problems table already contains {count} records - skipping data insertion")
            conn.close()
            return

        # Populate with data and hardcoded range values
        problems_data = [
            # Product pillar data
            # Product-Market Fit & Differentiation - Validation Seekers
            ("Product", "Validation Seekers",
             "Achieving true product-market fit beyond early adopters",
             "% of users 'very disappointed' if product is removed",
             40.0, 100.0, 0.0, 100.0, "Percentage"),

            # Product-Market Fit & Differentiation - Traction Builders
            ("Product", "Traction Builders",
             "Slow product iteration cycles",
             "Average release cycle time (days)",
             0.0, 14.0, 0.0, 90.0, "Days"),

            # Product-Market Fit & Differentiation - Scale Preparers
            ("Product", "Scale Preparers",
             "Product fragmentation across teams",
             "% of features used by >50% of users",
             70.0, 100.0, 0.0, 100.0, "Percentage"),

            # Product-Market Fit & Differentiation - Growth Accelerators
            ("Product", "Growth Accelerators",
             "Sustaining innovation at scale",
             "% of roadmap delivered quarterly",
             80.0, 100.0, 0.0, 100.0, "Percentage"),

            # Product-Market Fit & Differentiation - Frequent Pivoters
            ("Product", "Frequent Pivoters",
             "No structured process for evaluating pivots",
             "% of strategic pivots backed by user research",
             90.0, 100.0, 0.0, 100.0, "Percentage"),

            # Customer Retention & Experience - Validation Seekers
            ("Product", "Validation Seekers",
             "Creating predictable and stable revenue patterns",
             "Net Revenue Retention (NRR)",
             90.0, 100.0, 0.0, 200.0, "Percentage"),

            # Customer Retention & Experience - Traction Builders
            ("Product", "Traction Builders",
             "Churn beginning to emerge",
             "Monthly Churn Rate",
             0.0, 3.0, 0.0, 100.0, "Percentage"),

            # Customer Retention & Experience - Scale Preparers
            ("Product", "Scale Preparers",
             "Retention no longer improving",
             "Customer Retention Rate (12-month)",
             85.0, 100.0, 0.0, 100.0, "Percentage"),

            # Customer Retention & Experience - Growth Accelerators
            # Note: This is complex - "CSAT >=80, NPS >=30"
            # Using 80.0 as the primary threshold
            ("Product", "Growth Accelerators",
             "Inconsistent customer experience",
             "CSAT/NPS scores",
             80.0, 100.0, 0.0, 100.0, "Percentage"),

            # Customer Retention & Experience - Frequent Pivoters
            ("Product", "Frequent Pivoters",
             "Rebuilding trust through consistent delivery",
             "Feature adoption rate within 30 days",
             60.0, 100.0, 0.0, 100.0, "Percentage"),

            # Business pillar data
            # Customer Acquisition & Channel Efficiency - Validation Seekers
            ("Business", "Validation Seekers",
             "Finding repeatable acquisition channels",
             "CAC Payback Period",
             0.0, 12.0, 0.0, 36.0, "Months"),

            # Customer Acquisition & Channel Efficiency - Traction Builders
            ("Business", "Traction Builders",
             "CAC rising faster than LTV",
             "LTV:CAC Ratio",
             3.0, 100.0, 0.0, 100.0, "Ratio"),

            # Customer Acquisition & Channel Efficiency - Scale Preparers
            # Ambiguous: "Flat or decreasing" - using a flag value
            ("Business", "Scale Preparers",
             "Channel saturation",
             "CAC trend over time by channel",
             -1.0, 0.0, -1.0, 1.0, "Trend"),

            # Customer Acquisition & Channel Efficiency - Growth Accelerators
            ("Business", "Growth Accelerators",
             "Fragmented customer journeys",
             "Conversion rate across funnel stages",
             10.0, 100.0, 0.0, 100.0, "Percentage"),

            # Customer Acquisition & Channel Efficiency - Frequent Pivoters
            # Ambiguous: "Increasing MoM" - using a flag value
            ("Business", "Frequent Pivoters",
             "Brand confusion",
             "Branded search traffic or unaided brand recall",
             1.0, 1.0, 0.0, 0.0, "Trend"),

            # Revenue Model & Pricing - Validation Seekers
            ("Business", "Validation Seekers",
             "Effective pricing",
             "Gross Margin",
             70.0, 100.0, 0.0, 100.0, "Percentage"),

            # Revenue Model & Pricing - Traction Builders
            ("Business", "Traction Builders",
             "Pressure to raise Series A",
             "ARR growth rate (YoY)",
             3.0, 100.0, 0.0, 1000.0, "Multiplier"),

            # Revenue Model & Pricing - Scale Preparers
            # Ambiguous: "2x growth + trending toward breakeven"
            ("Business", "Scale Preparers",
             "Mixed metrics for Series B",
             "ARR growth + EBITDA margin",
             2.0, 100.0, 0.0, 100.0, "Multiplier"),

            # Revenue Model & Pricing - Growth Accelerators
            ("Business", "Growth Accelerators",
             "Unclear monetization of expansions",
             "% revenue from upsell/cross-sell",
             20.0, 100.0, 0.0, 100.0, "Percentage"),

            # Revenue Model & Pricing - Frequent Pivoters
            ("Business", "Frequent Pivoters",
             "Incomplete initiatives",
             "% of features with clear monetization path",
             75.0, 100.0, 0.0, 100.0, "Percentage"),

            # Funding & Financial Management - Validation Seekers
            ("Business", "Validation Seekers",
             "Attracting Seed/Pre-A investors",
             "Burn Multiple",
             0.0, 1.5, 0.0, 10.0, "Ratio"),

            # Funding & Financial Management - Traction Builders
            ("Business", "Traction Builders",
             "Raising Series A",
             "Revenue efficiency (ARR/Headcount)",
             100.0, 100000.0, 0.0, 1000000.0, "Currency"),

            # Funding & Financial Management - Scale Preparers
            # Ambiguous: "Stable or decreasing QoQ"
            ("Business", "Scale Preparers",
             "Raising Series B",
             "Net Burn Rate",
             0.0, 0.0, 0.0, 0.0, "Trend"),

            # Funding & Financial Management - Growth Accelerators
            ("Business", "Growth Accelerators",
             "IPO/acquisition readiness",
             "Rule of 40 (Growth % + Profit %)",
             40.0, 100.0, 0.0, 100.0, "Score"),

            # Funding & Financial Management - Frequent Pivoters
            ("Business", "Frequent Pivoters",
             "Avoiding repeated mistakes",
             "Forecast accuracy",
             90.0, 100.0, 0.0, 100.0, "Percentage"),

            # Systems pillar data
            # Operational Scalability & Process - Validation Seekers
            ("Systems", "Validation Seekers",
             "Avoiding premature scaling",
             "Ratio of GTM spend to new ARR",
             0.0, 1.5, 0.0, 10.0, "Ratio"),

            # Operational Scalability & Process - Traction Builders
            ("Systems", "Traction Builders",
             "Founder-led sales bottlenecks",
             "% revenue from non-founder deals",
             75.0, 100.0, 0.0, 100.0, "Percentage"),

            # Operational Scalability & Process - Scale Preparers
            ("Systems", "Scale Preparers",
             "Process bloat",
             "Avg time to close tickets (ops/dev)",
             0.0, 5.0, 0.0, 30.0, "Days"),

            # Operational Scalability & Process - Growth Accelerators
            ("Systems", "Growth Accelerators",
             "Shifting priorities too often",
             "% roadmap changes per quarter",
             0.0, 25.0, 0.0, 100.0, "Percentage"),

            # Operational Scalability & Process - Frequent Pivoters
            ("Systems", "Frequent Pivoters",
             "Context switching",
             "Avg # of priorities per team per sprint",
             0.0, 3.0, 0.0, 20.0, "Count"),

            # System Architecture & Technical Debt - Validation Seekers
            ("Systems", "Validation Seekers",
             "Founder burnout from systems",
             "% of time on operations vs strategy",
             0.0, 30.0, 0.0, 100.0, "Percentage"),

            # System Architecture & Technical Debt - Traction Builders
            ("Systems", "Traction Builders",
             "Tech debt impeding velocity",
             "% of engineering time on rework",
             0.0, 20.0, 0.0, 100.0, "Percentage"),

            # System Architecture & Technical Debt - Scale Preparers
            # Complex: ">99.9% uptime, <300ms latency"
            ("Systems", "Scale Preparers",
             "Architecture not scaling",
             "System uptime & latency under load",
             99.9, 100.0, 0.0, 100.0, "Percentage"),

            # System Architecture & Technical Debt - Growth Accelerators
            ("Systems", "Growth Accelerators",
             "Infra limits showing",
             "Cost of goods sold (COGS) as % revenue",
             0.0, 20.0, 0.0, 100.0, "Percentage"),

            # System Architecture & Technical Debt - Frequent Pivoters
            ("Systems", "Frequent Pivoters",
             "Abandoned features",
             "% of unused features over 90 days",
             0.0, 25.0, 0.0, 100.0, "Percentage"),

            # Data, Analytics & Decision-Making - Validation Seekers
            ("Systems", "Validation Seekers",
             "Balancing feedback with vision",
             "% of roadmap influenced by data",
             80.0, 100.0, 0.0, 100.0, "Percentage"),

            # Data, Analytics & Decision-Making - Traction Builders
            ("Systems", "Traction Builders",
             "Limited funnel visibility",
             "Funnel analytics completeness",
             100.0, 100.0, 0.0, 100.0, "Percentage"),

            # Data, Analytics & Decision-Making - Scale Preparers
            ("Systems", "Scale Preparers",
             "Analytics gaps",
             "% of KPIs with real-time visibility",
             90.0, 100.0, 0.0, 100.0, "Percentage"),

            # Data, Analytics & Decision-Making - Growth Accelerators
            ("Systems", "Growth Accelerators",
             "Conflicting metrics",
             "Single source of truth adoption",
             90.0, 100.0, 0.0, 100.0, "Percentage"),

            # Data, Analytics & Decision-Making - Frequent Pivoters
            ("Systems", "Frequent Pivoters",
             "Ignoring data for decisions",
             "% of strategic changes driven by data",
             75.0, 100.0, 0.0, 100.0, "Percentage"),

            # Team pillar data
            # Team Structure & Leadership - Validation Seekers
            ("Team", "Validation Seekers",
             "Early systems",
             "Org chart + documented roles",
             100.0, 100.0, 0.0, 100.0, "Percentage"),

            # Team Structure & Leadership - Traction Builders
            ("Team", "Traction Builders",
             "Scaling faster than systems",
             "FTE per manager ratio",
             0.0, 7.0, 0.0, 30.0, "Ratio"),

            # Team Structure & Leadership - Scale Preparers
            ("Team", "Scale Preparers",
             "Misalignment/accountability gaps",
             "% of roles with OKRs",
             90.0, 100.0, 0.0, 100.0, "Percentage"),

            # Team Structure & Leadership - Growth Accelerators
            ("Team", "Growth Accelerators",
             "Mgmt gaps emerging",
             "Leadership team tenure and turnover",
             18.0, 100.0, 0.0, 60.0, "Months"),

            # Team Structure & Leadership - Frequent Pivoters
            # Complex: "eNPS >=20, Engagement >=70%"
            ("Team", "Frequent Pivoters",
             "Morale breakdown",
             "eNPS or team engagement score",
             70.0, 100.0, 0.0, 100.0, "Percentage"),

            # Strategic Clarity & Focus - Validation Seekers
            ("Team", "Validation Seekers",
             "Crowded market differentiation",
             "Win rate vs key competitors",
             30.0, 100.0, 0.0, 100.0, "Percentage"),

            # Strategic Clarity & Focus - Traction Builders
            ("Team", "Traction Builders",
             "Marketing/sales misalignment",
             "Lead conversion rate from MQL to SQL",
             60.0, 100.0, 0.0, 100.0, "Percentage"),

            # Strategic Clarity & Focus - Scale Preparers
            ("Team", "Scale Preparers",
             "Decision-making confusion",
             "Decision turnaround time",
             0.0, 72.0, 0.0, 168.0, "Hours"),

            # Strategic Clarity & Focus - Growth Accelerators
            ("Team", "Growth Accelerators",
             "Unclear strategic direction",
             "% of team aligned on top 3 priorities",
             90.0, 100.0, 0.0, 100.0, "Percentage"),

            # Strategic Clarity & Focus - Frequent Pivoters
            ("Team", "Frequent Pivoters",
             "Frequent strategic changes",
             "Strategy revisions per quarter",
             0.0, 1.0, 0.0, 10.0, "Count"),
        ]

        # Insert the data
        cursor.executemany('''
        INSERT INTO architecture_problems 
        (architecture_pillar, growth_stage_name, problem_description, 
         metric_name, low_range, hi_range, min_range, max_range, units)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', problems_data)

        logger.info(f"Inserted {len(problems_data)} architecture problems")

        # Commit changes and close connection
        conn.commit()
        conn.close()

        logger.info("Architecture problems table created successfully")
    except Exception as e:
        logger.error(f"Error creating architecture problems table: {str(e)}")
        raise


def query_problems_by_pillar_and_stage(pillar, stage_name):
    """Query problems for a specific pillar and growth stage

    Args:
        pillar: One of "Product", "Business", "Systems", "Team"
        stage_name: One of the growth stage names (e.g., "Validation Seekers")

    Returns:
        List of problem dictionaries
    """
    try:
        conn = sqlite3.connect('data/traction_diagnostics.db')
        conn.row_factory = sqlite3.Row  # This enables column access by name
        cursor = conn.cursor()

        cursor.execute('''
        SELECT * FROM architecture_problems 
        WHERE architecture_pillar = ? AND growth_stage_name = ?
        ''', (pillar, stage_name))

        results = [dict(row) for row in cursor.fetchall()]
        conn.close()

        logger.debug(f"Retrieved {len(results)} problems for {pillar} pillar in {stage_name} stage")
        return results
    except Exception as e:
        logger.error(f"Error querying problems: {str(e)}")
        return []


def setup_database():
    """Main function to set up the entire database"""
    try:
        logger.info("Starting database setup")
        create_growth_stages_table()
        create_architecture_problems_table()
        logger.info("Database setup completed successfully")
        # For Streamlit integration, log a message in the UI as well
        if runtime.exists():
            st.success("Database setup completed successfully")
    except Exception as e:
        logger.error(f"Database setup failed: {str(e)}")
        # For Streamlit integration, show error in the UI as well
        if runtime.exists():
            st.error(f"Database setup failed: {str(e)}")
        raise


if __name__ == "__main__":
    setup_database()