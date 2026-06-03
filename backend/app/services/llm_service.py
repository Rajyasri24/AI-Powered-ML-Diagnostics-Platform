# backend/app/services/llm_service.py

from typing import Dict


def generate_dynamic_explanation(context: Dict):

    explanation = []

    # ---------------------------------------------------
    # BASIC DATASET INFO
    # ---------------------------------------------------

    explanation.append(
        f"Dataset contains {context['samples']} rows "
        f"and {context['features']} features."
    )

    explanation.append(
        f"Model used: {context['model_name']}."
    )

    explanation.append(
        f"Detected problem type: {context['problem']}."
    )

    # ---------------------------------------------------
    # CLASSIFICATION ANALYSIS
    # ---------------------------------------------------

    if context["problem"] == "classification":

        accuracy = context.get("accuracy", 0)
        precision = context.get("precision", 0)
        recall = context.get("recall", 0)
        f1 = context.get("f1", 0)

        explanation.append(
            f"Accuracy: {round(accuracy, 4)}"
        )

        explanation.append(
            f"Precision: {round(precision, 4)}"
        )

        explanation.append(
            f"Recall: {round(recall, 4)}"
        )

        explanation.append(
            f"F1 Score: {round(f1, 4)}"
        )

        train_accuracy = context.get("train_accuracy", 0)
        test_accuracy = context.get("test_accuracy", 0)

        if train_accuracy - test_accuracy > 0.10:

            explanation.append(
                "Possible overfitting detected because "
                "training accuracy is significantly higher "
                "than testing accuracy."
            )

        if accuracy < 0.60:

            explanation.append(
                "Classification performance is relatively low. "
                "Feature engineering or additional training data "
                "may improve results."
            )

    # ---------------------------------------------------
    # REGRESSION ANALYSIS
    # ---------------------------------------------------

    else:

        rmse = context.get("rmse", 0)
        r2 = context.get("r2", 0)

        explanation.append(
            f"RMSE: {round(rmse, 4)}"
        )

        explanation.append(
            f"R² Score: {round(r2, 4)}"
        )

        if r2 < 0.50:

            explanation.append(
                "The model explains less than 50% of variance, "
                "indicating weak predictive performance."
            )

        if rmse > 50:

            explanation.append(
                "Prediction error is relatively high. "
                "Feature scaling or better features may help."
            )

    # ---------------------------------------------------
    # SHAP ANALYSIS
    # ---------------------------------------------------

    top_feature = context.get("top_feature")

    if top_feature:

        explanation.append(
            f"SHAP analysis indicates that "
            f"'{top_feature}' is the most influential feature."
        )

    # ---------------------------------------------------
    # MISSING VALUES
    # ---------------------------------------------------

    missing_values = context.get("missing_values", 0)

    if missing_values > 0:

        explanation.append(
            f"The dataset contains {missing_values} missing values. "
            f"Handling missing data may improve model performance."
        )

    # ---------------------------------------------------
    # FINAL SUGGESTIONS
    # ---------------------------------------------------

    explanation.append(
        "Recommended next steps include hyperparameter tuning, "
        "cross-validation, and advanced feature engineering."
    )

    return "\n\n".join(explanation)