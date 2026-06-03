import warnings
import numpy as np
import pandas as pd
import time
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    LabelEncoder,
    StandardScaler
)
from sklearn.exceptions import ConvergenceWarning
from sklearn.impute import SimpleImputer

from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor
)
from sklearn.svm import LinearSVC
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

import warnings

from sklearn.exceptions import ConvergenceWarning

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# =====================================================
# WARNINGS CLEANUP
# =====================================================

warnings.filterwarnings(
    "ignore",
    category=ConvergenceWarning
) 

warnings.filterwarnings(
    "ignore",
    category=FutureWarning
)

warnings.filterwarnings(
    "ignore",
    category=UserWarning
)

warnings.filterwarnings(
    "ignore",
    category=RuntimeWarning
)

warnings.filterwarnings(
    "ignore",
    category=ConvergenceWarning
)

# =====================================================
# SAFE PREPROCESSING
# =====================================================

def clean_features(df):

    df = df.copy()

    df.replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True
    )

    numeric_cols = df.select_dtypes(
        include=np.number
    ).columns

    categorical_cols = df.select_dtypes(
        exclude=np.number
    ).columns

    # =====================================================
    # NUMERIC
    # =====================================================

    for col in numeric_cols:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

        median = df[col].median()

        df[col] = df[col].fillna(median)

    # =====================================================
    # CATEGORICAL
    # =====================================================

    for col in categorical_cols:

        df[col] = (
            df[col]
            .astype(str)
            .fillna("Unknown")
        )

        le = LabelEncoder()

        df[col] = le.fit_transform(
            df[col]
        )

    return df

# =====================================================
# CLASSIFICATION MODEL COMPARISON
# =====================================================

def compare_classification_models(
    X_train,
    X_test,
    y_train,
    y_test
):

    # =====================================================
    # CLEAN FEATURES
    # =====================================================

    X_train = clean_features(X_train)

    X_test = clean_features(X_test)

    # =====================================================
    # LABEL ENCODING
    # =====================================================

    label_encoder = LabelEncoder()

    y_train_encoded = label_encoder.fit_transform(
        y_train
    )

    y_test_encoded = label_encoder.transform(
        y_test
    )

    class_mapping = dict(

        zip(

            label_encoder.classes_,

            label_encoder.transform(
                label_encoder.classes_
            )
        )
    )

    num_classes = len(
        np.unique(y_train_encoded)
    )

    # =====================================================
    # MODELS
    # =====================================================

    models = {

        "RandomForest": Pipeline([

            (
                "model",
                RandomForestClassifier(
                    n_estimators=100,
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
                KNeighborsClassifier( n_neighbors=5,
    n_jobs=-1)
            )
        ]),

        "SVM": Pipeline([

            (
                "scaler",
                StandardScaler()
            ),

            (
                "model",
                LinearSVC(
                max_iter=2000,
                random_state=42
                )
            )
        ])
    }

    leaderboard = []

    best_model = None

    best_score = -1

    # =====================================================
    # TRAINING LOOP
    # =====================================================

    for model_name, model in models.items():
        start = time.time()
        try:

            # =====================================================
            # XGBOOST
            # =====================================================

            if model_name == "XGBoost":

                model.fit(
                    X_train,
                    y_train_encoded
                )

                y_pred = model.predict(
                    X_test
                )

                accuracy = accuracy_score(
                    y_test_encoded,
                    y_pred
                )

                f1 = f1_score(

                    y_test_encoded,

                    y_pred,

                    average="weighted",

                    zero_division=0
                )

            # =====================================================
            # OTHER MODELS
            # =====================================================

            else:

                model.fit(
                    X_train,
                    y_train
                )

                y_pred = model.predict(
                    X_test
                )

                accuracy = accuracy_score(
                    y_test,
                    y_pred
                )

                f1 = f1_score(

                    y_test,

                    y_pred,

                    average="weighted",

                    zero_division=0
                )

            result = {

                "model":
                model_name,

                "accuracy":
                round(float(accuracy), 4),

                "f1":
                round(float(f1), 4)
            }
            print(
            f"{model_name} finished in "
            f"{round(time.time() - start, 2)} sec"
            )

            leaderboard.append(result)

            if accuracy > best_score:

                best_score = accuracy

                best_model = model_name

        except Exception as e:

            leaderboard.append({

                "model":
                model_name,

                "error":
                str(e)
            })

    # =====================================================
    # SORT
    # =====================================================

    leaderboard = sorted(

        leaderboard,

        key=lambda x:
        x.get("accuracy", 0),

        reverse=True
    )

    return {

        "leaderboard":
        leaderboard,

        "best_model":
        best_model,

        "class_mapping":
        class_mapping
    }

# =====================================================
# REGRESSION MODEL COMPARISON
# =====================================================

def compare_regression_models(
    X_train,
    X_test,
    y_train,
    y_test
):

    # =====================================================
    # CLEAN FEATURES
    # =====================================================

    X_train = clean_features(X_train)

    X_test = clean_features(X_test)

    models = {

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
                # SVR()  
                SVR(
                kernel="linear"
                )
            )
        ])
    }

    leaderboard = []

    best_model = None

    best_score = -999999

    # =====================================================
    # TRAIN LOOP
    # =====================================================

    for model_name, model in models.items():

        try:

            model.fit(
                X_train,
                y_train
            )

            y_pred = model.predict(
                X_test
            )

            mae = mean_absolute_error(
                y_test,
                y_pred
            )

            rmse = np.sqrt(

                mean_squared_error(
                    y_test,
                    y_pred
                )
            )

            r2 = r2_score(
                y_test,
                y_pred
            )

            result = {

                "model":
                model_name,

                "mae":
                round(float(mae), 4),

                "rmse":
                round(float(rmse), 4),

                "r2":
                round(float(r2), 4)
            }

            leaderboard.append(result)

            if r2 > best_score:

                best_score = r2

                best_model = model_name

        except Exception as e:

            leaderboard.append({

                "model":
                model_name,

                "error":
                str(e)
            })

    leaderboard = sorted(

        leaderboard,

        key=lambda x:
        x.get("r2", -999999),

        reverse=True
    )

    return {

        "leaderboard":
        leaderboard,

        "best_model":
        best_model
    }