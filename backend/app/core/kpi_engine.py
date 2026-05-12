import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder


def analyze_kpi_importance(file_path: str, semantic_report: dict):

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format")

    numeric_df = df.select_dtypes(include=np.number)

    # Choose target automatically
    potential_targets = semantic_report.get("potential_target_columns", [])

    if not potential_targets:
        return {"message": "No suitable target column found"}

    # Remove obvious time columns
    filtered_targets = [
        col for col in potential_targets
        if "year" not in col.lower()
        and "id" not in col.lower()
    ]

    if not filtered_targets:
        filtered_targets = potential_targets

    # Choose target with highest variance
    variance_scores = {}

    for col in filtered_targets:
        if col in numeric_df.columns:
            variance_scores[col] = numeric_df[col].var()

    if not variance_scores:
        return {"message": "No valid numeric target found"}

    target = max(variance_scores, key=variance_scores.get)

    if target not in numeric_df.columns:
        return {"message": "Selected target not numeric"}

    X = numeric_df.drop(columns=[target], errors="ignore")
    y = numeric_df[target]

    if X.shape[1] < 2:
        return {"message": "Not enough features for importance analysis"}

    X = X.fillna(X.median())
    y = y.fillna(y.median())

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    importances = model.feature_importances_

    feature_importance_list = []

    for feature, importance in zip(X.columns, importances):
        feature_importance_list.append({
            "feature": feature,
            "importance": round(float(importance), 4)
        })

    feature_importance_list = sorted(
        feature_importance_list,
        key=lambda x: x["importance"],
        reverse=True
    )

    return {
        "selected_target": target,
        "top_influencers": feature_importance_list[:5]
    }