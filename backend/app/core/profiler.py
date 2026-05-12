import pandas as pd
import numpy as np


def profile_dataset(file_path: str):

    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path, encoding="utf-8")
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format")

    except Exception as e:
        raise Exception(f"File reading error: {str(e)}")

    profile = {}

    profile["num_rows"] = df.shape[0]
    profile["num_columns"] = df.shape[1]
    profile["columns"] = list(df.columns)

    # Detect column types
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include="object").columns.tolist()
    datetime_cols = df.select_dtypes(include="datetime").columns.tolist()

    profile["numeric_columns"] = numeric_cols
    profile["categorical_columns"] = categorical_cols
    profile["datetime_columns"] = datetime_cols

    # Missing values
    total_missing = df.isnull().sum().sum()
    total_cells = df.shape[0] * df.shape[1]
    missing_percentage = (total_missing / total_cells) * 100

    profile["total_missing_percentage"] = float(missing_percentage)

    # Duplicate rows
    duplicate_rows = df.duplicated().sum()
    profile["duplicate_rows"] = int(duplicate_rows)

    # Numeric statistics
    numeric_stats = {}
    for col in numeric_cols:
        numeric_stats[col] = {
            "mean": float(df[col].mean()),
            "std": float(df[col].std()),
            "min": float(df[col].min()),
            "max": float(df[col].max()),
            "skewness": float(df[col].skew())
        }

    profile["numeric_statistics"] = numeric_stats

    # Simple Data Quality Score
    quality_score = 100
    quality_score -= missing_percentage * 0.5
    quality_score -= (duplicate_rows / df.shape[0]) * 50

    profile["data_quality_score"] = round(max(0, quality_score), 2)

    return profile