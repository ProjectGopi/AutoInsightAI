import pandas as pd
import numpy as np


def analyze_semantics(file_path: str):

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format")

    semantic_report = {
        "id_columns": [],
        "revenue_columns": [],
        "percentage_columns": [],
        "datetime_columns": [],
        "potential_target_columns": []
    }

    for col in df.columns:

        col_lower = col.lower()

        #ID detection
        uniqueness_ratio = df[col].nunique() / len(df)

        if uniqueness_ratio > 0.95:
            if (
                not pd.api.types.is_float_dtype(df[col])
                and not any(keyword in col_lower for keyword in ["revenue", "price", "amount"])
            ):
                semantic_report["id_columns"].append(col)

        # Revenue detection (name-based)
        if any(keyword in col_lower for keyword in ["revenue", "sales", "amount", "price"]):
            if pd.api.types.is_numeric_dtype(df[col]):
                semantic_report["revenue_columns"].append(col)

        # Percentage detection
        if "%" in col_lower or "percent" in col_lower:
            semantic_report["percentage_columns"].append(col)

        # Datetime detection
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            semantic_report["datetime_columns"].append(col)

        # Potential target column (binary or low unique numeric)
        if pd.api.types.is_numeric_dtype(df[col]):
            if df[col].nunique() <= 10:
                semantic_report["potential_target_columns"].append(col)

    return semantic_report