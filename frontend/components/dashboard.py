# # =====================================================
# # frontend/components/dashboard.py
# # FINAL FULL UPDATED VERSION
# # ADAPTIVE ANALYTICS + NO EMPTY CHARTS
# # =====================================================

# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go


# # =====================================================
# # CACHE
# # =====================================================

# @st.cache_data
# def get_sample_df(df):

#     if len(df) > 10000:

#         return df.sample(
#             10000,
#             random_state=42
#         )

#     return df.copy()


# # =====================================================
# # DASHBOARD
# # =====================================================

# def show_dashboard():

#     # =====================================================
#     # HEADER
#     # =====================================================

#     st.title(
#         "Analytics Dashboard"
#     )

#     st.markdown(
#         """
#         Real-time AI-powered dataset analytics,
#         model benchmarking and reliability intelligence.
#         """
#     )

#     st.write("")

#     # =====================================================
#     # NAVIGATION
#     # =====================================================

#     nav1, nav2, nav3 = st.columns([1,1,1])

#     with nav1:

#         if st.button(
#             "← Back to Analyze",
#             width="stretch"
#         ):

#             st.session_state.page = "analyze"

#             st.rerun()

#     with nav2:

#         if st.button(
#             "Home",
#             width="stretch"
#         ):

#             st.session_state.page = "landing"

#             st.rerun()

#     with nav3:

#         if st.button(
#             "Logout",
#             width="stretch"
#         ):

#             st.session_state.logged_in = False

#             st.session_state.page = "landing"

#             st.rerun()

#     st.write("")
#     st.write("")

#     # =====================================================
#     # CHECK DATA
#     # =====================================================

#     if "dashboard_df" not in st.session_state:

#         st.warning(
#             "Please analyze a dataset first."
#         )

#         return

#     df = st.session_state["dashboard_df"]

#     chart_df = get_sample_df(df)

#     numeric_cols = chart_df.select_dtypes(
#         include=np.number
#     ).columns.tolist()

#     categorical_cols = chart_df.select_dtypes(
#         exclude=np.number
#     ).columns.tolist()

#     # =====================================================
#     # KPIs
#     # =====================================================

#     k1, k2, k3, k4 = st.columns(4)

#     with k1:

#         st.metric(
#             "Rows",
#             f"{len(df):,}"
#         )

#     with k2:

#         st.metric(
#             "Columns",
#             df.shape[1]
#         )

#     with k3:

#         st.metric(
#             "Missing Values",
#             int(df.isnull().sum().sum())
#         )

#     with k4:

#         st.metric(
#             "Duplicates",
#             int(df.duplicated().sum())
#         )

#     st.write("")
#     st.write("")

#     # =====================================================
#     # ROW 1
#     # =====================================================

#     r1c1, r1c2, r1c3 = st.columns(3)

#     # =====================================================
#     # HISTOGRAM / FALLBACK
#     # =====================================================

#     with r1c1:

#         if len(numeric_cols) > 0:

#             st.subheader(
#                 "Feature Distribution"
#             )

#             hist_col = st.selectbox(

#                 "Histogram Feature",

#                 numeric_cols,

#                 key="hist"
#             )

#             fig_hist = px.histogram(

#                 chart_df,

#                 x=hist_col,

#                 nbins=30,

#                 color_discrete_sequence=[
#                     "#A8D8EA"
#                 ]
#             )

#             fig_hist.update_layout(
#                 template="plotly_white",
#                 height=350
#             )

#             st.plotly_chart(
#                 fig_hist,
#                 width="stretch"
#             )

#         else:

#             st.subheader(
#                 "Dataset Composition"
#             )

#             fig_types = px.pie(

#                 names=[
#                     "Numeric",
#                     "Categorical"
#                 ],

#                 values=[
#                     len(numeric_cols),
#                     len(categorical_cols)
#                 ],

#                 color_discrete_sequence=[
#                     "#A8D8EA",
#                     "#FFD6E0"
#                 ]
#             )

#             fig_types.update_layout(
#                 height=350
#             )

#             st.plotly_chart(
#                 fig_types,
#                 width="stretch"
#             )

#     # =====================================================
#     # MISSING VALUES / FALLBACK
#     # =====================================================

#     with r1c2:

#         total_missing = int(
#             df.isnull().sum().sum()
#         )

#         # -------------------------------------------------

#         if total_missing > 0:

#             st.subheader(
#                 "Missing Value Analysis"
#             )

#             missing_data = (

#                 df.isnull()
#                 .sum()
#                 .sort_values(ascending=False)
#             )

#             missing_data = missing_data[
#                 missing_data > 0
#             ].head(10)

#             fig_missing = px.bar(

#                 x=missing_data.values,

#                 y=missing_data.index,

#                 orientation="h",

#                 color=missing_data.values,

#                 color_continuous_scale=[
#                     "#FFD6E0",
#                     "#FFDAC1"
#                 ]
#             )

#             fig_missing.update_layout(
#                 template="plotly_white",
#                 height=350
#             )

#             st.plotly_chart(
#                 fig_missing,
#                 width="stretch"
#             )

#         # -------------------------------------------------

#         elif len(numeric_cols) > 0:

#             st.subheader(
#                 "Feature Variance"
#             )

#             variance = (

#                 chart_df[numeric_cols]
#                 .var()
#                 .sort_values(ascending=False)
#                 .head(10)
#             )

#             fig_var = px.bar(

#                 x=variance.values,

#                 y=variance.index,

#                 orientation="h",

#                 color=variance.values,

#                 color_continuous_scale=[
#                     "#B5EAD7",
#                     "#A8D8EA"
#                 ]
#             )

#             fig_var.update_layout(
#                 template="plotly_white",
#                 height=350
#             )

#             st.plotly_chart(
#                 fig_var,
#                 width="stretch"
#             )

#         # -------------------------------------------------

#         else:

#             st.subheader(
#                 "Duplicate Analysis"
#             )

#             duplicates = int(
#                 df.duplicated().sum()
#             )

#             clean_rows = len(df) - duplicates

#             fig_dup = px.pie(

#                 names=[
#                     "Clean Rows",
#                     "Duplicate Rows"
#                 ],

#                 values=[
#                     clean_rows,
#                     duplicates
#                 ],

#                 color_discrete_sequence=[
#                     "#B5EAD7",
#                     "#FFD6E0"
#                 ]
#             )

#             fig_dup.update_layout(
#                 height=350
#             )

#             st.plotly_chart(
#                 fig_dup,
#                 width="stretch"
#             )

#     # =====================================================
#     # PIE / FALLBACK
#     # =====================================================

#     with r1c3:

#         if len(categorical_cols) > 0:

#             st.subheader(
#                 "Category Breakdown"
#             )

#             pie_col = st.selectbox(

#                 "Categorical Feature",

#                 categorical_cols,

#                 key="pie"
#             )

#             pie_data = (

#                 chart_df[pie_col]
#                 .astype(str)
#                 .value_counts()
#                 .head(6)
#             )

#             fig_pie = px.pie(

#                 values=pie_data.values,

#                 names=pie_data.index,

#                 color_discrete_sequence=[

#                     "#FFD6E0",
#                     "#CDE7BE",
#                     "#B5EAD7",
#                     "#FFDAC1",
#                     "#C7CEEA",
#                     "#FFF1BA"
#                 ]
#             )

#             fig_pie.update_layout(
#                 height=350
#             )

#             st.plotly_chart(
#                 fig_pie,
#                 width="stretch"
#             )

#         # -------------------------------------------------

#         elif len(numeric_cols) > 0:

#             st.subheader(
#                 "Skewness Analysis"
#             )

#             skew_data = (

#                 chart_df[numeric_cols]
#                 .skew()
#                 .sort_values(ascending=False)
#                 .head(10)
#             )

#             fig_skew = px.bar(

#                 x=skew_data.index,

#                 y=skew_data.values,

#                 color=skew_data.values,

#                 color_continuous_scale=[
#                     "#D5AAFF",
#                     "#A8D8EA"
#                 ]
#             )

#             fig_skew.update_layout(
#                 template="plotly_white",
#                 height=350
#             )

#             st.plotly_chart(
#                 fig_skew,
#                 width="stretch"
#             )

#         # -------------------------------------------------

#         else:

#             st.subheader(
#                 "Memory Usage"
#             )

#             mem_usage = round(

#                 df.memory_usage(
#                     deep=True
#                 ).sum() / 1024**2,

#                 2
#             )

#             mem_df = pd.DataFrame({

#                 "Metric": [
#                     "Dataset Memory"
#                 ],

#                 "Value": [
#                     mem_usage
#                 ]
#             })

#             fig_mem = px.bar(

#                 mem_df,

#                 x="Metric",

#                 y="Value",

#                 color="Value",

#                 color_continuous_scale=[
#                     "#C7CEEA",
#                     "#A8D8EA"
#                 ]
#             )

#             fig_mem.update_layout(
#                 template="plotly_white",
#                 height=350
#             )

#             st.plotly_chart(
#                 fig_mem,
#                 width="stretch"
#             )

#     st.write("")
#     st.write("")

#     # =====================================================
#     # ROW 2
#     # =====================================================

#     r2c1, r2c2, r2c3 = st.columns(3)

#     # =====================================================
#     # CORRELATION
#     # =====================================================

#     with r2c1:

#         if len(numeric_cols) > 1:

#             st.subheader(
#                 "Correlation Heatmap"
#             )

#             corr = (
#                 chart_df[numeric_cols[:15]]
#                 .corr()
#             )

#             fig_corr = px.imshow(

#                 corr,

#                 color_continuous_scale="RdBu",

#                 aspect="auto"
#             )

#             fig_corr.update_layout(
#                 height=350
#             )

#             st.plotly_chart(
#                 fig_corr,
#                 width="stretch"
#             )

#         else:

#             st.info(
#                 "Not enough numeric columns."
#             )

#     # =====================================================
#     # OUTLIER
#     # =====================================================

#     with r2c2:

#         if len(numeric_cols) > 0:

#             st.subheader(
#                 "Outlier Analysis"
#             )

#             outlier_col = st.selectbox(

#                 "Outlier Feature",

#                 numeric_cols,

#                 key="outlier"
#             )

#             fig_box = px.box(

#                 chart_df,

#                 y=outlier_col,

#                 color_discrete_sequence=[
#                     "#D5AAFF"
#                 ]
#             )

#             fig_box.update_layout(
#                 height=350
#             )

#             st.plotly_chart(
#                 fig_box,
#                 width="stretch"
#             )

#         else:

#             st.info(
#                 "No numeric columns available."
#             )

#     # =====================================================
#     # MODEL BENCHMARK
#     # =====================================================

#     with r2c3:

#         if (
#             "analysis_result"
#             in st.session_state
#         ):

#             leaderboard = pd.DataFrame(

#                 st.session_state[
#                     "analysis_result"
#                 ][
#                     "model_leaderboard"
#                 ]
#             )

#             numeric_metric_cols = leaderboard.select_dtypes(
#                 include=["number"]
#             ).columns

#             if len(numeric_metric_cols) > 0:

#                 metric_col = numeric_metric_cols[0]

#                 st.subheader(
#                     "Model Benchmark"
#                 )

#                 fig_model = px.bar(

#                     leaderboard,

#                     x="model",

#                     y=metric_col,

#                     color="model",

#                     color_discrete_sequence=[

#                         "#FFB7B2",
#                         "#FFDAC1",
#                         "#E2F0CB",
#                         "#B5EAD7",
#                         "#C7CEEA",
#                         "#D5AAFF"
#                     ]
#                 )

#                 fig_model.update_layout(
#                     template="plotly_white",
#                     height=350,
#                     showlegend=False
#                 )

#                 st.plotly_chart(
#                     fig_model,
#                     width="stretch"
#                 )

#     st.write("")
#     st.write("")

#     # =====================================================
#     # DATA PREVIEW
#     # =====================================================

#     st.subheader(
#         "Dataset Preview"
#     )

#     st.dataframe(

#         df.sample(
#             min(25, len(df)),
#             random_state=42
#         ),

#         width="stretch"
#     )

#     st.write("")
#     st.write("")

#     # =====================================================
#     # LEADERBOARD
#     # =====================================================

#     if (
#         "analysis_result"
#         in st.session_state
#     ):

#         st.subheader(
#             "Model Leaderboard"
#         )

#         leaderboard = pd.DataFrame(

#             st.session_state[
#                 "analysis_result"
#             ][
#                 "model_leaderboard"
#             ]
#         )

#         st.dataframe(
#             leaderboard,
#             width="stretch"
#         )


# =====================================================
# frontend/components/dashboard.py
# FINAL FULL UPDATED VERSION
# ADAPTIVE ANALYTICS + NO EMPTY CHARTS
# =====================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# =====================================================
# CACHE
# =====================================================

@st.cache_data
def get_sample_df(df):

    if len(df) > 10000:

        return df.sample(
            10000,
            random_state=42
        )

    return df.copy()


# =====================================================
# DASHBOARD
# =====================================================

def show_dashboard():

    # =====================================================
    # HEADER
    # =====================================================

    st.title(
        "Analytics Dashboard"
    )

    st.markdown(
        """
        Real-time AI-powered dataset analytics,
        model benchmarking and reliability intelligence.
        """
    )

    st.write("")

    # =====================================================
    # NAVIGATION
    # =====================================================

    nav1, nav2, nav3 = st.columns([1,1,1])

    with nav1:

        if st.button(
            "← Back to Analyze",
            width="stretch"
        ):

            st.session_state.page = "analyze"

            st.rerun()

    with nav2:

        if st.button(
            "Home",
            width="stretch"
        ):

            st.session_state.page = "landing"

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
    # CHECK DATA
    # =====================================================

    if "dashboard_df" not in st.session_state:

        st.warning(
            "Please analyze a dataset first."
        )

        return

    df = st.session_state["dashboard_df"]

    chart_df = get_sample_df(df)

    if df.empty:

        st.warning(
            "Dataset is empty."
        )

        return

    if chart_df.empty:

        st.warning(
            "No data available for visualization."
        )

        return

    numeric_cols = chart_df.select_dtypes(
        include=np.number
    ).columns.tolist()

    categorical_cols = chart_df.select_dtypes(
        exclude=np.number
    ).columns.tolist()

    # =====================================================
    # KPIs
    # =====================================================

    k1, k2, k3, k4 = st.columns(4)

    with k1:

        st.metric(
            "Rows",
            f"{len(df):,}"
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
    # ROW 1
    # =====================================================

    r1c1, r1c2, r1c3 = st.columns(3)

    # =====================================================
    # HISTOGRAM / FALLBACK
    # =====================================================

    with r1c1:

        if len(numeric_cols) > 0:

            st.subheader(
                "Feature Distribution"
            )

            hist_col = st.selectbox(

                "Histogram Feature",

                numeric_cols,

                key="hist"
            )

            # fig_hist = px.histogram(

            #     chart_df,

            #     x=hist_col,

            #     nbins=30,

            #     color_discrete_sequence=[
            #         "#A8D8EA"
            #     ]
            # )

            # fig_hist.update_layout(
            #     template="plotly_white",
            #     height=350
            # )

            # st.plotly_chart(
            #     fig_hist,
            #     width="stretch"
            # )


            valid_hist = chart_df[
                [hist_col]
            ].dropna()

            if len(valid_hist) > 0:

                fig_hist = px.histogram(
                    valid_hist,
                    x=hist_col,
                    nbins=30,
                    color_discrete_sequence=[
                        "#A8D8EA"
                    ]
                )

                fig_hist.update_layout(
                    template="plotly_white",
                    height=350
                )

                st.plotly_chart(
                    fig_hist,
                    use_container_width=True
                )

            else:

                st.info(
                    "Selected feature contains only missing values."
                 )

        else:

            st.subheader(
                "Dataset Composition"
            )

            fig_types = px.pie(

                names=[
                    "Numeric",
                    "Categorical"
                ],

                values=[
                    len(numeric_cols),
                    len(categorical_cols)
                ],

                color_discrete_sequence=[
                    "#A8D8EA",
                    "#FFD6E0"
                ]
            )

            fig_types.update_layout(
                height=350
            )

            st.plotly_chart(
                fig_types,
                width="stretch"
            )

    # =====================================================
    # MISSING VALUES / FALLBACK
    # =====================================================

    with r1c2:

        total_missing = int(
            df.isnull().sum().sum()
        )

        # -------------------------------------------------

        if total_missing > 0:

            st.subheader(
                "Missing Value Analysis"
            )

            missing_data = (

                df.isnull()
                .sum()
                .sort_values(ascending=False)
            )

            missing_data = missing_data[
                missing_data > 0
            ].head(10)

            fig_missing = px.bar(

                x=missing_data.values,

                y=missing_data.index,

                orientation="h",

                color=missing_data.values,

                color_continuous_scale=[
                    "#FFD6E0",
                    "#FFDAC1"
                ]
            )

            fig_missing.update_layout(
                template="plotly_white",
                height=350
            )

            st.plotly_chart(
                fig_missing,
                width="stretch"
            )

        # -------------------------------------------------

        elif len(numeric_cols) > 0:

            st.subheader(
                "Feature Variance"
            )

            variance = (

                chart_df[numeric_cols]
                .var()
                .sort_values(ascending=False)
                .head(10)
            )

            fig_var = px.bar(

                x=variance.values,

                y=variance.index,

                orientation="h",

                color=variance.values,

                color_continuous_scale=[
                    "#B5EAD7",
                    "#A8D8EA"
                ]
            )

            fig_var.update_layout(
                template="plotly_white",
                height=350
            )

            st.plotly_chart(
                fig_var,
                width="stretch"
            )

        # -------------------------------------------------

        else:

            st.subheader(
                "Duplicate Analysis"
            )

            duplicates = int(
                df.duplicated().sum()
            )

            clean_rows = len(df) - duplicates

            fig_dup = px.pie(

                names=[
                    "Clean Rows",
                    "Duplicate Rows"
                ],

                values=[
                    clean_rows,
                    duplicates
                ],

                color_discrete_sequence=[
                    "#B5EAD7",
                    "#FFD6E0"
                ]
            )

            fig_dup.update_layout(
                height=350
            )

            st.plotly_chart(
                fig_dup,
                width="stretch"
            )

    # =====================================================
    # PIE / FALLBACK
    # =====================================================

    with r1c3:

        if len(categorical_cols) > 0:

            st.subheader(
                "Category Breakdown"
            )

            pie_col = st.selectbox(

                "Categorical Feature",

                categorical_cols,

                key="pie"
            )

            pie_data = (

                chart_df[pie_col]
                .astype(str)
                .value_counts()
                .head(6)
            )

            fig_pie = px.pie(

                values=pie_data.values,

                names=pie_data.index,

                color_discrete_sequence=[

                    "#FFD6E0",
                    "#CDE7BE",
                    "#B5EAD7",
                    "#FFDAC1",
                    "#C7CEEA",
                    "#FFF1BA"
                ]
            )

            fig_pie.update_layout(
                height=350
            )

            st.plotly_chart(
                fig_pie,
                width="stretch"
            )

        # -------------------------------------------------

        elif len(numeric_cols) > 0:

            st.subheader(
                "Skewness Analysis"
            )

            skew_data = (

                chart_df[numeric_cols]
                .skew()
                .sort_values(ascending=False)
                .head(10)
            )

            fig_skew = px.bar(

                x=skew_data.index,

                y=skew_data.values,

                color=skew_data.values,

                color_continuous_scale=[
                    "#D5AAFF",
                    "#A8D8EA"
                ]
            )

            fig_skew.update_layout(
                template="plotly_white",
                height=350
            )

            st.plotly_chart(
                fig_skew,
                width="stretch"
            )

        # -------------------------------------------------

        else:

            st.subheader(
                "Memory Usage"
            )

            mem_usage = round(

                df.memory_usage(
                    deep=True
                ).sum() / 1024**2,

                2
            )

            mem_df = pd.DataFrame({

                "Metric": [
                    "Dataset Memory"
                ],

                "Value": [
                    mem_usage
                ]
            })

            fig_mem = px.bar(

                mem_df,

                x="Metric",

                y="Value",

                color="Value",

                color_continuous_scale=[
                    "#C7CEEA",
                    "#A8D8EA"
                ]
            )

            fig_mem.update_layout(
                template="plotly_white",
                height=350
            )

            st.plotly_chart(
                fig_mem,
                width="stretch"
            )

    st.write("")
    st.write("")

    # =====================================================
    # ROW 2
    # =====================================================

    r2c1, r2c2, r2c3 = st.columns(3)

    # =====================================================
    # CORRELATION
    # =====================================================

    with r2c1:

        if len(numeric_cols) > 1:

            st.subheader(
                "Correlation Heatmap"
            )

            # corr = (
            #     chart_df[numeric_cols[:15]]
            #     .corr()
            # )

            corr = (
                chart_df[numeric_cols[:15]]
                .corr(numeric_only=True)
            )

            if corr.empty:

                st.info(
                    "Correlation matrix unavailable."
                )

            else:

                fig_corr = px.imshow(

                    corr,

                    color_continuous_scale="RdBu",

                    aspect="auto"
                )

                fig_corr.update_layout(
                    height=350
                )

                st.plotly_chart(
                    fig_corr,
                    width="stretch"
                )

        else:

            st.info(
                "Not enough numeric columns."
            )

    # =====================================================
    # OUTLIER
    # =====================================================

    with r2c2:

        if len(numeric_cols) > 0:

            st.subheader(
                "Outlier Analysis"
            )

            outlier_col = st.selectbox(

                "Outlier Feature",

                numeric_cols,

                key="outlier"
            )

            fig_box = px.box(

                chart_df,

                y=outlier_col,

                color_discrete_sequence=[
                    "#D5AAFF"
                ]
            )

            fig_box.update_layout(
                height=350
            )

            st.plotly_chart(
                fig_box,
                width="stretch"
            )

        else:

            st.info(
                "No numeric columns available."
            )

    # =====================================================
    # MODEL BENCHMARK
    # =====================================================

    with r2c3:

        if (
            "analysis_result"
            in st.session_state
        ):

            # leaderboard = pd.DataFrame(

            #     st.session_state[
            #         "analysis_result"
            #     ][
            #         "model_leaderboard"
            #     ]
            # )
            analysis_result = st.session_state.get(
                "analysis_result",
                {}
            )

            leaderboard_data = analysis_result.get(
                "model_leaderboard",
                []
            )

            leaderboard = pd.DataFrame(
                leaderboard_data
            )

            numeric_metric_cols = leaderboard.select_dtypes(
                include=["number"]
            ).columns

            if len(numeric_metric_cols) > 0:

                metric_col = numeric_metric_cols[0]

                st.subheader(
                    "Model Benchmark"
                )

                fig_model = px.bar(

                    leaderboard,

                    x="model",

                    y=metric_col,

                    color="model",

                    color_discrete_sequence=[

                        "#FFB7B2",
                        "#FFDAC1",
                        "#E2F0CB",
                        "#B5EAD7",
                        "#C7CEEA",
                        "#D5AAFF"
                    ]
                )

                fig_model.update_layout(
                    template="plotly_white",
                    height=350,
                    showlegend=False
                )

                st.plotly_chart(
                    fig_model,
                    width="stretch"
                )

    st.write("")
    st.write("")

    # =====================================================
    # ADVANCED ANALYTICS
    # =====================================================

    st.subheader("Advanced Analytics")

    analytics_option = st.selectbox(

        "Choose Analytics",

        [

            "Feature Variance",

            "Skewness Analysis",

            "Class Imbalance",

            "Cardinality Analysis",

            "Outlier Percentage",

            "Dataset Quality Score"
        ]
    )

    # =====================================================
    # FEATURE VARIANCE
    # =====================================================

    if analytics_option == "Feature Variance":

        if len(numeric_cols) > 0:

            variance_df = pd.DataFrame({

                "Feature":
                numeric_cols,

                "Variance":
                chart_df[numeric_cols]
                .var()
                .values
            })

            st.dataframe(
                variance_df,
                use_container_width=True
            )

        else:

            st.info(
                "No numeric columns available."
            )

    # =====================================================
    # SKEWNESS ANALYSIS
    # =====================================================

    elif analytics_option == "Skewness Analysis":

        if len(numeric_cols) > 0:

            skew_df = pd.DataFrame({

                "Feature":
                numeric_cols,

                "Skewness":
                chart_df[numeric_cols]
                .skew()
                .values
            })

            st.dataframe(
                skew_df,
                use_container_width=True
            )

        else:

            st.info(
                "No numeric columns available."
            )

    # =====================================================
    # CLASS IMBALANCE
    # =====================================================

    elif analytics_option == "Class Imbalance":

        possible_targets = (

            categorical_cols
            if len(categorical_cols) > 0
            else numeric_cols
        )

        if len(possible_targets) > 0:

            imbalance_col = st.selectbox(

                "Target Column",

                possible_targets,

                key="imbalance"
            )

            imbalance_data = (
                chart_df[imbalance_col]
                .astype(str)
                .value_counts()
                .head(10)
            )

            fig_imbalance = px.bar(

                x=imbalance_data.index,

                y=imbalance_data.values,

                color=imbalance_data.values,

                color_continuous_scale="Sunset"
            )

            st.plotly_chart(

                fig_imbalance,

                use_container_width=True
            )

        else:

            st.info(
                "No suitable target columns found."
            )

    # =====================================================
    # CARDINALITY ANALYSIS
    # =====================================================

    elif analytics_option == "Cardinality Analysis":

        if len(categorical_cols) > 0:

            cardinality_data = {

                col:
                chart_df[col].nunique()

                for col in categorical_cols
            }

            cardinality_df = pd.DataFrame({

                "Column":
                list(cardinality_data.keys()),

                "Unique Values":
                list(cardinality_data.values())
            })

            st.dataframe(
                cardinality_df,
                use_container_width=True
            )

        else:

            st.info(
                "No categorical columns available."
            )

    # # =====================================================
    # # CORRELATION RANKING
    # # =====================================================

    # elif analytics_option == "Correlation Ranking":

    #     if len(numeric_cols) > 1:

    #         # corr_matrix = (
    #         #     chart_df[numeric_cols]
    #         #     .corr()
    #         #     .abs()
    #         # )

    #         # corr_pairs = (

    #         #     corr_matrix.unstack()
    #         #     .sort_values(ascending=False)
    #         # )

    #         corr_matrix = corr_matrix.values[
    #             np.tril_indices_from(corr_matrix)
    #         ] = np.nan

    #         corr_pairs = ( corr_matrix.unstack()
    #             .dropna()
    #             .sort_values(ascending=False)
    #         )

    #         corr_pairs = corr_pairs[
    #             corr_pairs < 1
    #         ]

    #         corr_df = pd.DataFrame({

    #             "Feature Pair":
    #             [f"{idx[0]} ↔ {idx[1]}" for idx in corr_pairs.index],

    #             "Correlation":
    #             corr_pairs.values
    #         })

    #         st.dataframe(

    #             corr_df.head(20),

    #             use_container_width=True
    #         )

        # else:

        #     st.info(
        #         "Not enough numeric columns."
        #     )

    # =====================================================
    # OUTLIER %
    # =====================================================

    elif analytics_option == "Outlier Percentage":

        if len(numeric_cols) > 0:

            outlier_stats = []

            for col in numeric_cols:

                q1 = chart_df[col].quantile(0.25)

                q3 = chart_df[col].quantile(0.75)

                iqr = q3 - q1

                lower = q1 - 1.5 * iqr

                upper = q3 + 1.5 * iqr

                outliers = (

                    (chart_df[col] < lower)
                    |
                    (chart_df[col] > upper)
                ).sum()

                # percentage = (
                #     outliers / len(chart_df)
                # ) * 100

                percentage = 0

                if len(chart_df) > 0:

                    percentage = (
                        outliers / len(chart_df)
                    ) * 100

                outlier_stats.append({

                    "Feature": col,

                    "Outlier %":
                    round(percentage, 2)
                })

            outlier_df = pd.DataFrame(
                outlier_stats
            )

            st.dataframe(
                outlier_df,
                use_container_width=True
            )

        else:

            st.info(
                "No numeric columns available."
            )

    # =====================================================
    # DATASET QUALITY SCORE
    # =====================================================

    elif analytics_option == "Dataset Quality Score":

        # missing_score = max(

        #     0,

        #     100 - (
        #         df.isnull().sum().sum()
        #         / df.size
        #     ) * 100
        # )

        # duplicate_score = max(

        #     0,

        #     100 - (
        #         df.duplicated().sum()
        #         / len(df)
        #     ) * 100
        # )

        # quality_score = round(

        #     (
        #         missing_score +
        #         duplicate_score
        #     ) / 2,

        #     2
        # )
        if df.size == 0:

            quality_score = 0

        else:

            missing_score = max(

                0,

                100 - (
                    df.isnull().sum().sum()
                    / df.size
                ) * 100
            )

            duplicate_score = max(

                0,

                100 - (
                    df.duplicated().sum()
                    / len(df)
                ) * 100
            )

            quality_score = round(

                (
                    missing_score +
                    duplicate_score
                ) / 2,

                2
            )

        fig_gauge = go.Figure(

            go.Indicator(

                mode="gauge+number",

                value=quality_score,

                title={
                    "text":
                    "Dataset Quality Score"
                },

                gauge={

                    "axis": {
                        "range": [0, 100]
                    },

                    "bar": {
                        "color": "#A8D8EA"
                    },

                    "steps": [

                        {
                            "range": [0, 50],
                            "color": "#FFD6E0"
                        },

                        {
                            "range": [50, 75],
                            "color": "#FFF1BA"
                        },

                        {
                            "range": [75, 100],
                            "color": "#B5EAD7"
                        }
                    ]
                }
            )
        )

        fig_gauge.update_layout(
            height=400
        )

        st.plotly_chart(
            fig_gauge,
            use_container_width=True
        )

    st.write("---")

    

    # =====================================================
    # DATA PREVIEW
    # =====================================================

    st.subheader(
        "Dataset Preview"
    )

    st.dataframe(

        df.sample(
            min(25, len(df))
        ),

        width="stretch"
    )

    st.write("")
    st.write("")

    # =====================================================
    # LEADERBOARD
    # =====================================================

    if (
        "analysis_result"
        in st.session_state
    ):

        st.subheader(
            "Model Leaderboard"
        )

        # leaderboard = pd.DataFrame(

        #     st.session_state[
        #         "analysis_result"
        #     ][
        #         "model_leaderboard"
        #     ]
        # )

        analysis_result = st.session_state.get(
            "analysis_result",
            {}
        )

        leaderboard_data = analysis_result.get(
            "model_leaderboard",
            []
        )

        leaderboard = pd.DataFrame(
            leaderboard_data
        )

        st.dataframe(
            leaderboard,
            width="stretch"
        )