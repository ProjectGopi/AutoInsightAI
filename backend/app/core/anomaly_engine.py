import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest


def detect_anomalies(file_path: str, threshold=3.0):

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format")

    numeric_df = df.select_dtypes(include=np.number)

    if numeric_df.shape[1] < 2:
        return {
            "message": "Not enough numeric features for anomaly detection"
        }

    # Fill missing values
    numeric_df = numeric_df.fillna(numeric_df.median())

    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )

    model.fit(numeric_df)

    predictions = model.predict(numeric_df)

    anomaly_count = int((predictions == -1).sum())
    total_rows = numeric_df.shape[0]

    anomaly_percentage = (anomaly_count / total_rows) * 100

    # Simple confidence heuristic
    confidence_score = round(1 - (anomaly_percentage / 100), 3)

    return {
        "total_anomalies": anomaly_count,
        "anomaly_percentage": round(anomaly_percentage, 2),
        "confidence_score": confidence_score
    }