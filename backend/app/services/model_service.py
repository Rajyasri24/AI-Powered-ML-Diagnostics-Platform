# =====================================================
# backend/services/model_service.py
# PRODUCTION-READY MODEL REGISTRY
# =====================================================

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor
)

from xgboost import (
    XGBClassifier,
    XGBRegressor
)

from sklearn.linear_model import (
    LogisticRegression,
    LinearRegression,
    Ridge,
    Lasso
)

from sklearn.tree import (
    DecisionTreeClassifier,
    DecisionTreeRegressor
)

from sklearn.neighbors import KNeighborsClassifier

from sklearn.svm import (
    SVC,
    SVR
)


# =====================================================
# CLASSIFICATION MODELS
# =====================================================

CLASSIFICATION_MODELS = {

    "RandomForest": Pipeline([

        (
            "model",
            RandomForestClassifier(

                n_estimators=200,

                random_state=42,

                n_jobs=-1
            )
        )
    ]),

    "XGBoost": Pipeline([

        (
            "model",
            XGBClassifier(

                eval_metric="mlogloss",

                random_state=42,

                n_estimators=200,

                max_depth=6,

                learning_rate=0.05,

                subsample=0.8,

                colsample_bytree=0.8,

                n_jobs=-1
            )
        )
    ]),

    "LogisticRegression": Pipeline([

        (
            "scaler",
            StandardScaler()
        ),

        (
            "model",
            LogisticRegression(

                max_iter=3000,

                solver="saga",

                random_state=42
            )
        )
    ]),

    "DecisionTree": Pipeline([

        (
            "model",
            DecisionTreeClassifier(
                random_state=42
            )
        )
    ]),

    "KNN": Pipeline([

        (
            "scaler",
            StandardScaler()
        ),

        (
            "model",
            KNeighborsClassifier()
        )
    ]),

    "SVM": Pipeline([

        (
            "scaler",
            StandardScaler()
        ),

        (
            "model",
            SVC(
                probability=True
            )
        )
    ])
}


# =====================================================
# REGRESSION MODELS
# =====================================================

REGRESSION_MODELS = {

    "RandomForest": Pipeline([

        (
            "model",
            RandomForestRegressor(

                n_estimators=200,

                random_state=42,

                n_jobs=-1
            )
        )
    ]),

    "XGBoost": Pipeline([

        (
            "model",
            XGBRegressor(

                random_state=42,

                n_estimators=200,

                max_depth=6,

                learning_rate=0.05,

                subsample=0.8,

                colsample_bytree=0.8,

                n_jobs=-1
            )
        )
    ]),

    "LinearRegression": Pipeline([

        (
            "scaler",
            StandardScaler()
        ),

        (
            "model",
            LinearRegression()
        )
    ]),

    "Ridge": Pipeline([

        (
            "scaler",
            StandardScaler()
        ),

        (
            "model",
            Ridge()
        )
    ]),

    "Lasso": Pipeline([

        (
            "scaler",
            StandardScaler()
        ),

        (
            "model",
            Lasso()
        )
    ]),

    "DecisionTree": Pipeline([

        (
            "model",
            DecisionTreeRegressor(
                random_state=42
            )
        )
    ]),

    "SVR": Pipeline([

        (
            "scaler",
            StandardScaler()
        ),

        (
            "model",
            SVR()
        )
    ])
}


# =====================================================
# GET MODEL
# =====================================================

def get_model(
    model_name,
    problem_type
):

    # =====================================================
    # CLASSIFICATION
    # =====================================================

    if problem_type == "classification":

        if model_name in CLASSIFICATION_MODELS:

            return CLASSIFICATION_MODELS[
                model_name
            ]

        raise ValueError(
            f"Unsupported classification model: {model_name}"
        )

    # =====================================================
    # REGRESSION
    # =====================================================

    elif problem_type == "regression":

        if model_name in REGRESSION_MODELS:

            return REGRESSION_MODELS[
                model_name
            ]

        raise ValueError(
            f"Unsupported regression model: {model_name}"
        )

    # =====================================================
    # INVALID
    # =====================================================

    else:

        raise ValueError(
            f"Invalid problem type: {problem_type}"
        )


# =====================================================
# AVAILABLE MODELS
# =====================================================

def get_available_models():

    return {

        "classification":
        list(
            CLASSIFICATION_MODELS.keys()
        ),

        "regression":
        list(
            REGRESSION_MODELS.keys()
        )
    }