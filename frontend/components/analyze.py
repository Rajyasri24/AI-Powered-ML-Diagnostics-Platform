# =====================================================
# frontend/components/analyze.py
# FINAL CLEAN ANALYZE PAGE
# =====================================================

import streamlit as st
import pandas as pd
import requests
import os


def show_analyze():

    # =====================================================
    # TITLE
    # =====================================================

    st.title(
        "Dataset Analysis"
    )

    st.markdown(
        """
        <div class="subtitle">

        Upload datasets, benchmark machine learning models,
        generate explainability reports and evaluate
        AI reliability using intelligent diagnostics.

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    # =====================================================
    # NAVIGATION
    # =====================================================

    nav1, nav2, nav3 = st.columns(3)

    with nav1:

        if st.button(
            "← Home",
            width="stretch"
        ):

            st.session_state.page = "landing"

            st.rerun()

    with nav2:

        if st.button(
            "Open Dashboard",
            width="stretch"
        ):

            st.session_state.page = "dashboard"

            st.rerun()

    with nav3:

        if st.button(
            "Logout",
            width="stretch"
        ):

            st.session_state.logged_in = False

            st.session_state.page = "landing"

            st.rerun()

    st.write("")
    st.write("")

    # =====================================================
    # FILE UPLOAD
    # =====================================================

    uploaded_file = st.file_uploader(
        "Upload CSV Dataset",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:

            df = pd.read_csv(uploaded_file)

            st.session_state["dashboard_df"] = df

            # =====================================================
            # PREVIEW
            # =====================================================

            st.subheader(
                "Dataset Preview"
            )

            st.dataframe(
                df.head(),
                width="stretch"
            )

            st.write("")

            # =====================================================
            # KPIs
            # =====================================================

            k1, k2, k3, k4 = st.columns(4)

            with k1:

                st.metric(
                    "Rows",
                    df.shape[0]
                )

            with k2:

                st.metric(
                    "Columns",
                    df.shape[1]
                )

            with k3:

                st.metric(
                    "Missing Values",
                    int(df.isnull().sum().sum())
                )

            with k4:

                st.metric(
                    "Duplicates",
                    int(df.duplicated().sum())
                )

            st.write("")
            st.write("")

            # =====================================================
            # TARGET + MODEL
            # =====================================================

            c1, c2 = st.columns(2)

            with c1:

                target_column = st.selectbox(

                    "Select Target Column ▼",

                    df.columns
                )

            with c2:

                model_name = st.selectbox(

                    "Select Model ▼",

                    [

                        "RandomForest",

                        "XGBoost",

                        "LogisticRegression",

                        "DecisionTree",

                        "KNN",

                        "SVC",

                        "LinearRegression",

                        "Ridge",

                        "Lasso",

                        "SVR"
                    ]
                )

            st.write("")
            st.write("")

            # =====================================================
            # RUN BUTTON
            # =====================================================

            left, center, right = st.columns([3,2,3])

            with center:

                run_analysis = st.button(

                    "Run Full Analysis",

                    width="stretch"
                )

            # =====================================================
            # RUN ANALYSIS
            # =====================================================

            if run_analysis:

                with st.spinner(
                    "Running AI analysis..."
                ):

                    uploaded_file.seek(0)

                    files = {

                        "file":
                        (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "text/csv"
                        )
                    }

                    data = {

                        "target_column":
                        target_column,

                        "model_name":
                        model_name
                    }
                    BACKEND_URL = os.getenv(
                        "BACKEND_URL",
                        "http://127.0.0.1:8000"
                    )
                    response = requests.post(

                         f"{BACKEND_URL}/analyze",

                        files=files,

                        data=data
                    )

                    if response.status_code == 200:

                        result = response.json()

                        st.session_state[
                            "analysis_result"
                        ] = result

                        st.success(
                            "Analysis Complete"
                        )

                        st.write("")

                        # =====================================================
                        # OVERVIEW
                        # =====================================================

                        o1, o2 = st.columns(2)

                        with o1:

                            st.subheader(
                                "Problem Type"
                            )

                            st.info(
                                result["problem_type"]
                            )

                        with o2:

                            st.subheader(
                                "Best Model"
                            )

                            st.success(
                                result["best_model"]
                            )

                        st.write("")

                        # =====================================================
                        # METRICS
                        # =====================================================

                        st.subheader(
                            "Performance Metrics"
                        )

                        metrics = result["metrics"]

                        metric_cols = st.columns(
                            len(metrics)
                        )

                        for idx, (
                            key,
                            value
                        ) in enumerate(
                            metrics.items()
                        ):

                            metric_cols[idx].metric(

                                key.upper(),

                                round(
                                    float(value),
                                    4
                                )
                            )

                        st.write("")

                        # =====================================================
                        # MODEL LEADERBOARD
                        # =====================================================

                        st.subheader(
                            "Model Leaderboard"
                        )

                        leaderboard = pd.DataFrame(

                            result[
                                "model_leaderboard"
                            ]
                        )

                        st.dataframe(
                            leaderboard,
                            width="stretch"
                        )

                        st.write("")

                        # =====================================================
                        # TOP FEATURES
                        # =====================================================

                        if result["top_features"]:

                            st.subheader(
                                "Top Features"
                            )

                            feature_df = pd.DataFrame(

                                result[
                                    "top_features"
                                ]
                            )

                            st.dataframe(
                                feature_df,
                                width="stretch"
                            )

                        # =====================================================
                        # CORRELATIONS
                        # =====================================================

                        if result["correlations"]:

                            st.subheader(
                                "High Correlations"
                            )

                            corr_df = pd.DataFrame(

                                result[
                                    "correlations"
                                ]
                            )

                            st.dataframe(
                                corr_df,
                                width="stretch"
                            )

                        # =====================================================
                        # SHAP
                        # =====================================================

                        if result["shap"]:

                            st.subheader(
                                "SHAP Explainability"
                            )

                            st.image(
                                result["shap"],
                                width="stretch"
                            )

                        # =====================================================
                        # CONFUSION MATRIX
                        # =====================================================

                        if result["cm"]:

                            st.subheader(
                                "Confusion Matrix"
                            )

                            st.image(
                                result["cm"],
                                width="stretch"
                            )

                        # =====================================================
                        # RELIABILITY REPORT
                        # =====================================================

                        st.subheader(
                            "AI Reliability Report"
                        )

                        st.write(
                            result["llm"]
                        )

                        st.write("")
                        st.write("")

                        # =====================================================
                        # DASHBOARD BUTTON
                        # =====================================================

                        left, center, right = st.columns([3,2,3])

                        with center:

                            if st.button(
                                "Open Analytics Dashboard",
                                width="stretch"
                            ):

                                st.session_state.page = "dashboard"

                                st.rerun()

                    else:

                        st.error(
                            "Backend request failed."
                        )

        except Exception as e:

            st.error(str(e))