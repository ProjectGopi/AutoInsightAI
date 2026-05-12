import pandas as pd
import numpy as np


def analyze_relationships(file_path: str):

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format")

    numeric_df = df.select_dtypes(include=np.number)

    if numeric_df.shape[1] < 2:
        return {
            "strong_correlations": [],
            "message": "Not enough numeric columns for correlation analysis"
        }

    corr_matrix = numeric_df.corr()

    strong_pairs = []

    for col in corr_matrix.columns:
        for row in corr_matrix.index:
            if col != row:
                corr_value = corr_matrix.loc[row, col]
                if abs(corr_value) > 0.7:
                    strong_pairs.append({
                        "feature_1": row,
                        "feature_2": col,
                        "correlation": round(float(corr_value), 3)
                    })

    # Remove duplicate pairs
    unique_pairs = []
    seen = set()

    for pair in strong_pairs:
        key = tuple(sorted([pair["feature_1"], pair["feature_2"]]))
        if key not in seen:
            seen.add(key)
            unique_pairs.append(pair)

    return {
        "strong_correlations": unique_pairs,
        "total_numeric_features": numeric_df.shape[1]
    }