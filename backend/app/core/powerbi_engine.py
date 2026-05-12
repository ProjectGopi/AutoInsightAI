import pandas as pd


def prepare_powerbi_export(file_path, semantic_report, relationship_report):

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format")

    clean_path = file_path.replace(".csv", "_cleaned.csv")

    df_clean = df.copy()
    df_clean = df_clean.fillna(df_clean.median(numeric_only=True))

    df_clean.to_csv(clean_path, index=False)

    recommended_visuals = []

    # Revenue trend suggestion
    revenue_cols = semantic_report.get("revenue_columns", [])
    if revenue_cols:
        recommended_visuals.append({
            "type": "bar_chart",
            "x": revenue_cols[0],
            "y": revenue_cols[-1]
        })

    # Correlation-based suggestion
    strong_corr = relationship_report.get("strong_correlations", [])
    if strong_corr:
        pair = strong_corr[0]
        recommended_visuals.append({
            "type": "scatter_plot",
            "x": pair["feature_1"],
            "y": pair["feature_2"]
        })

    return {
        "clean_dataset_path": clean_path,
        "recommended_visuals": recommended_visuals
    }