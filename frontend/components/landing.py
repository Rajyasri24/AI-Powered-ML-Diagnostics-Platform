# =====================================================
# frontend/components/landing.py
# FINAL CLEAN APPLE STYLE LANDING PAGE
# =====================================================

import streamlit as st


def show_landing():

    # =====================================================
    # HERO
    # =====================================================

    st.title(
        "AI-Powered ML Diagnostics Platform"
    )

    st.markdown(
        """
        <div class="subtitle">

       Comprehensive model evaluation, explainability,
       data quality assessment and performance benchmarking
       for machine learning systems.

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # =====================================================
    # FEATURE CARDS
    # =====================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Explainability",
            "SHAP + Insights"
        )

    with col2:

        st.metric(
            "Diagnostics",
            "Dataset Intelligence"
        )

    with col3:

        st.metric(
            "Benchmarking",
            "Multi-Model Evaluation"
        )

    st.write("")
    st.write("")

    # =====================================================
    # PLATFORM OVERVIEW
    # =====================================================

    st.subheader(
        "Core Platform Capabilities"
    )

    overview1, overview2 = st.columns(2)

    with overview1:

        st.markdown(
            """
            ✓ Automated Model Benchmarking

            ✓ Feature Attribution Analysis

            ✓ Correlation & Dependency Discovery

            ✓ Intelligent Dataset Diagnostics

            ✓ Interactive Analytics Dashboard

            ✓ Classification Performance Evaluation
            """
        )

    with overview2:

        st.markdown(
            """
            ✓ Feature Importance Ranking

            ✓ Outlier Detection & Analysis

            ✓ Missing Value Intelligence

            ✓ Dataset Quality Assessment

            ✓ Interactive Visual Analytics

            ✓ AI-Generated Analysis Reports
            """
        )

    st.write("")
    st.write("")

    # =====================================================
    # BUTTONS
    # =====================================================

    left, center, right = st.columns([2,2,2])

    with center:

        if st.button(
            "Continue",
            width="stretch"
        ):

            st.session_state.page = "auth"

            st.rerun()

    st.write("")
    st.write("")

    # =====================================================
    # FOOTER
    # =====================================================

    st.caption(
        """
        Dataset Intelligence • Explainability • Model Benchmarking • Visual Analytics
        built using Streamlit, FastAPI, SHAP and modern ML workflows.
        """
    )