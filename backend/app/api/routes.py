# backend/app/api/routes.py

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Form

import pandas as pd
import numpy as np
import os
import time


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)
from sklearn.preprocessing import StandardScaler

from sklearn.model_selection import train_test_split

# =====================================================
# CLASSIFICATION MODELS
# =====================================================

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from sklearn.linear_model import LogisticRegression

from sklearn.tree import DecisionTreeClassifier

from sklearn.neighbors import KNeighborsClassifier

from sklearn.svm import SVC

# =====================================================
# REGRESSION MODELS
# =====================================================

from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

from sklearn.linear_model import (
    LinearRegression,
    Ridge,
    Lasso
)

from sklearn.tree import DecisionTreeRegressor

from sklearn.svm import SVR

# =====================================================
# METRICS
# =====================================================

from sklearn.metrics import (

    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,

    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# =====================================================
# SERVICES
# =====================================================

from backend.app.services.shap_service import (
    generate_shap_plot
)

from backend.app.services.reliability_service import (

    analyze_dataset,

    analyze_model_reliability,

    generate_reliability_report,

    analyze_feature_importance,

    analyze_correlations
)

from backend.app.services.model_comparison_service import (

    compare_classification_models,

    compare_regression_models
)

# =====================================================
# VISUALIZATION
# =====================================================

import matplotlib.pyplot as plt
import seaborn as sns

# =====================================================
# ROUTER
# =====================================================

router = APIRouter()

# =====================================================
# ANALYZE ROUTE
# =====================================================

@router.post("/analyze")
async def analyze_dataset_route(

    file: UploadFile = File(...),

    target_column: str = Form(...),

    model_name: str = Form(...)

):

    try:

        # =====================================================
        # LOAD DATASET
        # =====================================================

        df = pd.read_csv(file.file)

        # =====================================================
        # LARGE DATASET HANDLING
        # =====================================================

        original_shape = df.shape

        dataset_sampled = False

        if df.shape[0] > 100000:

            df = df.sample(
                100000,
                random_state=42
            )

            dataset_sampled = True

        # =====================================================
        # TARGET VALIDATION
        # =====================================================

        if target_column not in df.columns:

            return {
                "error":
                "Selected target column not found."
            }

        # =====================================================
        # DATASET ANALYSIS
        # =====================================================

        dataset_analysis = analyze_dataset(
            df,
            target_column
        )

        problem_type = dataset_analysis[
            "problem_type"
        ]

        # =====================================================
        # FEATURES + TARGET
        # =====================================================

        X = df.drop(columns=[target_column])

        y = df[target_column]

        # =====================================================
        # TARGET CLEANING
        # =====================================================

        try:

            y = pd.to_numeric(y)

        except:

            pass

        # =====================================================
        # DROP HIGH CARDINALITY COLUMNS
        # =====================================================

        high_cardinality_cols = []

        for col in X.select_dtypes(
            include="object"
        ).columns:

            if X[col].nunique() > 50:

                high_cardinality_cols.append(col)

        X = X.drop(
            columns=high_cardinality_cols,
            errors="ignore"
        )

        # =====================================================
        # HANDLE MISSING VALUES
        # =====================================================

        for col in X.columns:

            try:

                if pd.api.types.is_numeric_dtype(X[col]):

                    X[col] = X[col].fillna(
                        X[col].median()
                    )

                else:

                    X[col] = X[col].fillna(
                        X[col].mode()[0]
                    )

            except Exception:

                X[col] = X[col].astype(str)

                X[col] = X[col].fillna("Unknown")

        # =====================================================
        # ENCODING
        # =====================================================

        X = pd.get_dummies(X)

        scaler = StandardScaler()

        X = pd.DataFrame(

            scaler.fit_transform(X),

            columns=X.columns
            )

        # =====================================================
        # REMOVE CONSTANT COLUMNS
        # =====================================================

        constant_cols = [

            col for col in X.columns

            if X[col].nunique() <= 1
        ]

        X = X.drop(
            columns=constant_cols,
            errors="ignore"
        )

        # =====================================================
        # FEATURE LIMIT SAFETY
        # =====================================================

        if X.shape[1] > 1000:

            return {
                "error":
                "Too many generated features after encoding. "
                "Dataset likely contains excessive categorical values."
            }

        # =====================================================
        # TRAIN TEST SPLIT
        # =====================================================

        # X_train, X_test, y_train, y_test = (
        #     train_test_split(

        #         X,
        #         y,

        #         test_size=0.2,

        #         random_state=42
        #     )
        # )

        if problem_type == "classification":

            X_train, X_test, y_train, y_test = (
                train_test_split(
                    X,
                    y,
                    test_size=0.2,
                    random_state=42,
                    stratify=y
                )
            )

        else:

            X_train, X_test, y_train, y_test = (
                train_test_split(
                    X,
                    y,
                    test_size=0.2,
                    random_state=42
                )
            )

        # =====================================================
        # MODEL SELECTION
        # =====================================================

        if problem_type == "classification":

            if model_name == "RandomForest":

                model = RandomForestClassifier(
                    n_estimators=100,
                    random_state=42,
                    n_jobs=-1
                )

            elif model_name == "XGBoost":

                model = XGBClassifier(
                    eval_metric="logloss",
                    random_state=42
                )

            elif model_name == "LogisticRegression":

                # model = LogisticRegression(
                #     max_iter=1000
                # )
                model = LogisticRegression(
                  max_iter=3000,
                  solver="lbfgs"
                )
            elif model_name == "DecisionTree":

                model = DecisionTreeClassifier(
                    random_state=42
                )

            elif model_name == "KNN":

                model = KNeighborsClassifier()

            elif model_name == "SVC":

                model = SVC()

            else:

                return {
                    "error":
                    "Unsupported classification model"
                }

        else:

            if model_name == "RandomForest":

                model = RandomForestRegressor(
                    n_estimators=100,
                    random_state=42,
                    n_jobs=-1
                )

            elif model_name == "XGBoost":

                model = XGBRegressor(
                    random_state=42
                )

            elif model_name == "LinearRegression":

                model = LinearRegression()

            elif model_name == "Ridge":

                model = Ridge()

            elif model_name == "Lasso":

                model = Lasso()

            elif model_name == "DecisionTree":

                model = DecisionTreeRegressor(
                    random_state=42
                )

            elif model_name == "SVR":

                model = SVR()

            else:

                return {
                    "error":
                    "Unsupported regression model"
                }

        # =====================================================
        # TRAIN MODEL
        # =====================================================

        model.fit(
            X_train,
            y_train
        )

        # =====================================================
        # SCORES
        # =====================================================

        train_score = model.score(
            X_train,
            y_train
        )

        test_score = model.score(
            X_test,
            y_test
        )

        # =====================================================
        # PREDICTIONS
        # =====================================================

        y_pred = model.predict(X_test)

        # =====================================================
        # METRICS
        # =====================================================

        if problem_type == "classification":

            metrics = {

                "accuracy":
                accuracy_score(
                    y_test,
                    y_pred
                ),

                "precision":
                precision_score(
                    y_test,
                    y_pred,
                    average="weighted",
                    zero_division=0
                ),

                "recall":
                recall_score(
                    y_test,
                    y_pred,
                    average="weighted",
                    zero_division=0
                ),

                "f1":
                f1_score(
                    y_test,
                    y_pred,
                    average="weighted",
                    zero_division=0
                )
            }

        else:

            rmse = np.sqrt(

                mean_squared_error(
                    y_test,
                    y_pred
                )
            )

            metrics = {

                "mae":
                mean_absolute_error(
                    y_test,
                    y_pred
                ),

                "rmse":
                rmse,

                "r2":
                r2_score(
                    y_test,
                    y_pred
                )
            }

        # =====================================================
        # RELIABILITY ANALYSIS
        # =====================================================

        model_analysis = (
            analyze_model_reliability(

                train_score=train_score,

                test_score=test_score
            )
        )

        # =====================================================
        # FEATURE IMPORTANCE
        # =====================================================

        feature_analysis = analyze_feature_importance(
            model,
            X_train
        )

        # =====================================================
        # CORRELATION ANALYSIS
        # =====================================================

        correlation_analysis = analyze_correlations(
            X_train
        )

        # =====================================================
        # SHAP
        # =====================================================

        shap_path = None

        # try:

        #     X_test_sample = X_test.sample(

        #         min(200, len(X_test)),

        #         random_state=42
        #     )

        #     shap_path = generate_shap_plot(

        #         model,

        #         X_train,

        #         X_test_sample
        #     )

        # except Exception as e:

        #     print(
        #         f"SHAP ERROR: {str(e)}"
        #     )
        try:
            X_shap = X_test.sample(
                min(100, len(X_test)),
                random_state=42
            )

            shap_path = generate_shap_plot(
                model,
                X_shap
            )

        except Exception as e:

            print(
                f"SHAP ERROR: {str(e)}"
            )


        start = time.time()

        shap_path = generate_shap_plot(
            model,
            X_shap
        )

        print(
            "SHAP TIME:",
            round(time.time() - start, 2),
            "seconds"
        )

        # =====================================================
        # CONFUSION MATRIX
        # =====================================================

        cm_path = None

        if problem_type == "classification":

            try:

                cm = confusion_matrix(
                    y_test,
                    y_pred
                )

                plt.figure(figsize=(6, 4))

                sns.heatmap(

                    cm,

                    annot=True,

                    fmt="d",

                    cmap="Blues"
                )

                plt.title(
                    "Confusion Matrix"
                )

                plt.xlabel(
                    "Predicted"
                )

                plt.ylabel(
                    "Actual"
                )

                os.makedirs(
                    "static",
                    exist_ok=True
                )

                cm_path = "static/cm.png"

                plt.savefig(cm_path)

                plt.close()

            except Exception as e:

                print(
                    f"CM ERROR: {str(e)}"
                )

        # =====================================================
        # MODEL COMPARISON
        # =====================================================

        if problem_type == "classification":

            comparison_results = (
                compare_classification_models(

                    X_train,
                    X_test,

                    y_train,
                    y_test
                )
            )

        else:

            comparison_results = (
                compare_regression_models(

                    X_train,
                    X_test,

                    y_train,
                    y_test
                )
            )

        # =====================================================
        # FINAL REPORT
        # =====================================================

        llm_response = (
            generate_reliability_report(

                dataset_analysis=
                dataset_analysis,

                model_analysis=
                model_analysis,

                metrics=
                metrics,

                feature_analysis=
                feature_analysis,

                correlation_analysis=
                correlation_analysis
            )
        )

        # =====================================================
        # RETURN
        # =====================================================

        return {

            "problem_type":
            problem_type,

            "metrics":
            metrics,

            "llm":
            llm_response,

            "shap":
            (
            f"{BACKEND_URL}/{shap_path}"
             if shap_path else None
            ),

            "cm":
            (
             f"{BACKEND_URL}/{cm_path}"
             if cm_path else None
            ),

            "dataset_findings":
            dataset_analysis[
                "findings"
            ],

            "dataset_recommendations":
            dataset_analysis[
                "recommendations"
            ],

            "model_findings":
            model_analysis[
                "findings"
            ],

            "model_recommendations":
            model_analysis[
                "recommendations"
            ],

            "top_features":
            feature_analysis,

            "correlations":
            correlation_analysis,

            "removed_high_cardinality_columns":
            high_cardinality_cols,

            "removed_constant_columns":
            constant_cols,

            "model_leaderboard":
            comparison_results[
                "leaderboard"
            ],

            "best_model":
            comparison_results[
                "best_model"
            ],

            "dataset_sampled":
            dataset_sampled,

            "original_shape":
            original_shape
        }

    except Exception as e:

        return {
            "error": str(e)
        } 