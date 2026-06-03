# =====================================================
# backend/services/shap_services.py
# FINAL PRODUCTION-READY VERSION
# =====================================================

import os
import shap
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# =====================================================
# SHAP PLOT GENERATOR
# =====================================================

def generate_shap_plot(
    model,
    X
):

    try:

        # =====================================================
        # CREATE STATIC FOLDER
        # =====================================================

        os.makedirs(
            "static",
            exist_ok=True
        )

        # =====================================================
        # SAMPLE LARGE DATASETS
        # =====================================================

        # if len(X) > 100:

        #     X = X.sample(
        #         100,
        #         random_state=42
        #     )

        # =====================================================
        # CLEAN NAN / INF
        # =====================================================

        # X = X.replace(
        #     [np.inf, -np.inf],
        #     np.nan
        # )

        X = pd.DataFrame(X)

        X = X.apply(
            pd.to_numeric,
            errors="coerce"
        )

        X = X.replace(
            [np.inf, -np.inf],
            np.nan
        )

        X = X.fillna(0)

        X = X.astype(float)


        # =====================================================
        # TREE EXPLAINER
        # =====================================================

        try:

            explainer = shap.TreeExplainer(
                model
            )

            shap_values = explainer.shap_values(
                X,
                check_additivity=False
            )

        # =====================================================
        # GENERAL EXPLAINER FALLBACK
        # =====================================================

        except Exception:

            explainer = shap.Explainer(
                model,
                X
            )

            shap_values = explainer(
                X
            )

        # =====================================================
        # HANDLE MULTI-CLASS OUTPUT
        # =====================================================

        if isinstance(
            shap_values,
            list
        ):

            shap_values = shap_values[0]

        # =====================================================
        # SAVE IMAGE PATH
        # =====================================================

        path = os.path.join(
            "static",
            "shap.png"
        )

        # =====================================================
        # PLOT
        # =====================================================

        plt.figure(
            figsize=(12, 7)
        )

        shap.summary_plot(

            shap_values,

            X,

            show=False
        )

        plt.tight_layout()

        plt.savefig(

            path,

            bbox_inches="tight",

            dpi=300
        )

        plt.close()

        return path

    # =====================================================
    # FAIL SAFELY
    # =====================================================

    except Exception as e:

        print(
            "SHAP ERROR:",
            str(e)
        )

        return None