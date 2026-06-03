# =====================================================
# backend/app/services/monitoring_service.py
# PRODUCTION-READY CONFUSION MATRIX
# =====================================================

import os

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix


# =====================================================
# CONFUSION MATRIX PLOT
# =====================================================

def confusion_plot(
    y_true,
    y_pred
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
        # COMPUTE MATRIX
        # =====================================================

        cm = confusion_matrix(
            y_true,
            y_pred
        )

        # =====================================================
        # IMAGE PATH
        # =====================================================

        path = os.path.join(
            "static",
            "cm.png"
        )

        # =====================================================
        # CLEAN FIGURE
        # =====================================================

        plt.figure(
            figsize=(8, 6)
        )

        sns.heatmap(

            cm,

            annot=True,

            fmt="d",

            cmap="Blues",

            cbar=True
        )

        plt.title(
            "Confusion Matrix"
        )

        plt.xlabel(
            "Predicted Label"
        )

        plt.ylabel(
            "True Label"
        )

        plt.tight_layout()

        # =====================================================
        # SAVE
        # =====================================================

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
            "CONFUSION MATRIX ERROR:",
            str(e)
        )

        return None