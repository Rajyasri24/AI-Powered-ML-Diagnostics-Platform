# =====================================================
# frontend/components/styles.py
# FINAL CLEAN APPLE-STYLE UI
# =====================================================

import streamlit as st


def load_css():

    st.markdown(
        """
        <style>

        /* =====================================================
           GLOBAL
        ===================================================== */

        html,
        body,
        [class*="css"] {

            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "SF Pro Display",
                "Segoe UI",
                sans-serif;

            color: #111111;
        }

        .main {

            background:
                linear-gradient(
                    180deg,
                    #f5f7fb 0%,
                    #eef2f7 100%
                );
        }

        .block-container {

            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }

        /* =====================================================
           TITLES
        ===================================================== */

        h1 {

            font-size: 3.5rem !important;

            font-weight: 700 !important;

            text-align: center;

            color: #111111;

            margin-bottom: 0.4rem;
        }

        h2 {

            font-weight: 650 !important;

            color: #111111;
        }

        h3 {

            font-weight: 600 !important;

            color: #111111;
        }

        /* =====================================================
           SUBTITLE
        ===================================================== */

        .subtitle {

            text-align: center;

            color: #5f6368;

            font-size: 1.1rem;

            max-width: 850px;

            margin: auto;

            line-height: 1.8;

            margin-bottom: 2rem;
        }

        /* =====================================================
           BUTTONS
        ===================================================== */

        .stButton > button {

            background: #000000;

            color: white;

            border: none;

            border-radius: 14px;

            height: 3.2rem;

            font-size: 15px;

            font-weight: 600;

            transition: all 0.25s ease;

            width: 100%;
        }

        .stButton > button:hover {

            background: #111111;

            transform: translateY(-2px);

            box-shadow:
                0 8px 18px rgba(0,0,0,0.15);
        }

        /* =====================================================
           INPUTS
        ===================================================== */

        .stSelectbox div[data-baseweb="select"],
        .stTextInput input {

            border-radius: 14px;

            border: 1px solid #dcdcdc;

            background: white;
        }

        /* =====================================================
           METRICS
        ===================================================== */

        [data-testid="metric-container"] {

            background: white;

            border-radius: 20px;

            padding: 1rem;

            box-shadow:
                0 4px 16px rgba(0,0,0,0.05);

            border: 1px solid #f0f0f0;
        }

        /* =====================================================
           DATAFRAMES
        ===================================================== */

        .stDataFrame {

            background: white;

            border-radius: 20px;

            overflow: hidden;

            border: 1px solid #eeeeee;

            box-shadow:
                0 4px 16px rgba(0,0,0,0.04);
        }

        /* =====================================================
           CHARTS
        ===================================================== */

        .js-plotly-plot {

            background: white !important;

            border-radius: 20px;

            padding: 0.5rem;

            border: 1px solid #eeeeee;

            box-shadow:
                0 4px 16px rgba(0,0,0,0.04);
        }

        /* =====================================================
           SEPARATORS
        ===================================================== */

        hr {

            border: none;

            border-top:
                1px solid #eaeaea;

            margin-top: 2rem;
            margin-bottom: 2rem;
        }

        </style>
        """,
        unsafe_allow_html=True
    )