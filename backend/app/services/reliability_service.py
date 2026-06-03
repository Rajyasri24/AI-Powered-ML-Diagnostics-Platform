# =====================================================
# backend/app/services/reliability_service.py
# FINAL PRODUCTION VERSION
# =====================================================

import numpy as np
import pandas as pd


# =====================================================
# DATASET ANALYSIS
# =====================================================

def analyze_dataset(
    df,
    target_column
):

    findings = []
    recommendations = []

    num_rows = df.shape[0]
    num_cols = df.shape[1]

    findings.append(
        f"Dataset contains {num_rows} rows and {num_cols} columns."
    )

    # =====================================================
    # MISSING VALUES
    # =====================================================

    total_cells = max(
        1,
        df.shape[0] * df.shape[1]
    )

    missing_percentage = (

        df.isnull()
        .sum()
        .sum()

        / total_cells

    ) * 100

    if missing_percentage > 0:

        findings.append(
            f"Dataset has {missing_percentage:.2f}% missing values."
        )

    if missing_percentage > 15:

        recommendations.append(
            "Use imputation techniques to handle missing values."
        )

    # =====================================================
    # DUPLICATES
    # =====================================================

    duplicate_count = int(
        df.duplicated().sum()
    )

    if duplicate_count > 0:

        findings.append(
            f"Dataset contains {duplicate_count} duplicate rows."
        )

        recommendations.append(
            "Remove duplicate rows before training."
        )

    # =====================================================
    # SMALL DATASET
    # =====================================================

    if num_rows < 500:

        findings.append(
            "Small dataset detected."
        )

        recommendations.append(
            "Use cross-validation for better reliability."
        )

    # =====================================================
    # HIGH DIMENSIONALITY
    # =====================================================

    if num_cols > num_rows:

        findings.append(
            "High dimensional dataset detected."
        )

        recommendations.append(
            "Apply PCA or feature selection."
        )

    # =====================================================
    # TARGET ANALYSIS
    # =====================================================

    target = df[target_column]

    unique_classes = target.nunique()

    # =====================================================
    # CLASSIFICATION
    # =====================================================

    if unique_classes <= 10:

        problem_type = "classification"

        findings.append(
            f"Classification problem with {unique_classes} classes."
        )

        distribution = (
            target
            .value_counts(normalize=True)
        )

        max_ratio = distribution.max()

        if max_ratio > 0.80:

            findings.append(
                "Class imbalance detected."
            )

            recommendations.append(
                "Use SMOTE or class weights."
            )

    # =====================================================
    # REGRESSION
    # =====================================================

    else:

        problem_type = "regression"

        findings.append(
            "Regression problem detected."
        )

    # =====================================================
    # NUMERIC DATA
    # =====================================================

    numeric_df = df.select_dtypes(
        include=np.number
    )

    # =====================================================
    # OUTLIER ANALYSIS
    # =====================================================

    outlier_count = 0

    try:

        limited_numeric = numeric_df.iloc[
            :5000
        ]

        for col in limited_numeric.columns:

            series = (
                limited_numeric[col]
                .dropna()
            )

            if len(series) < 5:
                continue

            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)

            iqr = q3 - q1

            if iqr == 0:
                continue

            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            outliers = (

                (series < lower)
                |
                (series > upper)

            ).sum()

            outlier_count += int(outliers)

        if outlier_count > 0:

            findings.append(
                f"Potential outliers detected: {outlier_count}"
            )

            recommendations.append(
                "Use robust scaling or outlier treatment."
            )

    except:
        pass

    # =====================================================
    # CONSTANT COLUMNS
    # =====================================================

    constant_columns = []

    for col in df.columns:

        if df[col].nunique() <= 1:

            constant_columns.append(col)

    if len(constant_columns) > 0:

        findings.append(
            f"{len(constant_columns)} constant feature(s) detected."
        )

        recommendations.append(
            "Remove low-information columns."
        )

    # =====================================================
    # RETURN
    # =====================================================

    return {

        "problem_type":
        problem_type,

        "findings":
        list(set(findings)),

        "recommendations":
        list(set(recommendations))
    }


# =====================================================
# MODEL RELIABILITY
# =====================================================

def analyze_model_reliability(

    train_score,
    test_score
):

    findings = []
    recommendations = []

    gap = train_score - test_score

    # =====================================================
    # OVERFITTING
    # =====================================================

    if gap > 0.10:

        findings.append(
            "Potential overfitting detected."
        )

        recommendations.append(
            "Reduce model complexity or apply regularization."
        )

    # =====================================================
    # UNDERFITTING
    # =====================================================

    if (

        train_score < 0.60
        and
        test_score < 0.60

    ):

        findings.append(
            "Potential underfitting detected."
        )

        recommendations.append(
            "Try more expressive models or better features."
        )

    return {

        "findings":
        findings,

        "recommendations":
        recommendations
    }


# =====================================================
# FEATURE IMPORTANCE
# =====================================================

def analyze_feature_importance(
    model,
    X_train
):

    try:

        actual_model = model

        # =====================================================
        # PIPELINE SUPPORT
        # =====================================================

        if hasattr(
            model,
            "named_steps"
        ):

            actual_model = list(
                model.named_steps.values()
            )[-1]

        # =====================================================
        # FEATURE IMPORTANCE
        # =====================================================

        if hasattr(
            actual_model,
            "feature_importances_"
        ):

            importance = (
                actual_model.feature_importances_
            )

            feature_importance = pd.DataFrame({

                "feature":
                X_train.columns,

                "importance":
                importance
            })

            feature_importance = (

                feature_importance
                .sort_values(
                    by="importance",
                    ascending=False
                )
            )

            return (

                feature_importance
                .head(10)
                .to_dict(
                    orient="records"
                )
            )

        return []

    except:

        return []


# =====================================================
# CORRELATION ANALYSIS
# =====================================================

def analyze_correlations(
    X_train
):

    try:

        numeric_df = X_train.select_dtypes(
            include=np.number
        )

        # =====================================================
        # TOO SMALL
        # =====================================================

        if numeric_df.shape[1] < 2:

            return []

        # =====================================================
        # LIMIT HUGE MATRICES
        # =====================================================

        limited_df = numeric_df.iloc[
            :5000,
            :30
        ]

        corr_matrix = (
            limited_df.corr().abs()
        )

        high_corr = []

        columns = corr_matrix.columns

        for i in range(len(columns)):

            for j in range(i):

                corr_value = corr_matrix.iloc[i, j]

                if corr_value > 0.90:

                    high_corr.append({

                        "feature_1":
                        columns[i],

                        "feature_2":
                        columns[j],

                        "correlation":
                        round(
                            float(corr_value),
                            4
                        )
                    })

        return high_corr[:15]

    except:

        return []


# =====================================================
# FINAL REPORT GENERATOR
# =====================================================

def generate_reliability_report(

    dataset_analysis,
    model_analysis,
    metrics,
    feature_analysis,
    correlation_analysis
):

    report = []

    report.append(
        "AI Model Reliability Report"
    )

    report.append("")

    # =====================================================
    # DATASET FINDINGS
    # =====================================================

    report.append(
        "Dataset Findings:"
    )

    for finding in dataset_analysis[
        "findings"
    ]:

        report.append(
            f"- {finding}"
        )

    report.append("")

    # =====================================================
    # MODEL FINDINGS
    # =====================================================

    report.append(
        "Model Findings:"
    )

    for finding in model_analysis[
        "findings"
    ]:

        report.append(
            f"- {finding}"
        )

    report.append("")

    # =====================================================
    # METRICS
    # =====================================================

    report.append(
        "Performance Metrics:"
    )

    for key, value in metrics.items():

        report.append(
            f"- {key}: {value}"
        )

    report.append("")

    # =====================================================
    # FEATURE IMPORTANCE
    # =====================================================

    if feature_analysis:

        report.append(
            "Top Important Features:"
        )

        for item in feature_analysis:

            report.append(
                f"- {item['feature']} ({item['importance']:.4f})"
            )

        report.append("")

    # =====================================================
    # CORRELATION ANALYSIS
    # =====================================================

    if correlation_analysis:

        report.append(
            "High Correlations Detected:"
        )

        for item in correlation_analysis:

            report.append(
                f"- {item['feature_1']} and "
                f"{item['feature_2']} "
                f"({item['correlation']:.2f})"
            )

        report.append("")

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    report.append(
        "Recommendations:"
    )

    combined = (

        dataset_analysis[
            "recommendations"
        ]

        +

        model_analysis[
            "recommendations"
        ]
    )

    combined = list(set(combined))

    if combined:

        for rec in combined:

            report.append(
                f"- {rec}"
            )

    else:

        report.append(
            "- No major reliability issues detected."
        )

    return "\n".join(report)