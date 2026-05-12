def detect_gaps(profile_report, semantic_report, relationship_report, anomaly_report, kpi_report):
    
    gaps = []

    # 1️⃣ High correlation redundancy
    strong_corr = relationship_report.get("strong_correlations", [])
    if strong_corr:
        for pair in strong_corr:
            if abs(pair["correlation"]) > 0.95:
                gaps.append(
                    f"High redundancy detected between {pair['feature_1']} and {pair['feature_2']} (correlation {pair['correlation']})"
                )

    # 2️⃣ Missing business metric
    revenue_cols = semantic_report.get("revenue_columns", [])
    if revenue_cols and not any("cost" in col.lower() for col in profile_report["columns"]):
        gaps.append("Revenue detected but no cost column found. Profit analysis not possible.")

    # 3️⃣ High anomaly concentration
    anomaly_percentage = anomaly_report.get("anomaly_percentage", 0)
    if anomaly_percentage > 10:
        gaps.append("High anomaly percentage detected. Data reliability risk.")

    # 4️⃣ Weak feature diversity
    kpi_top = kpi_report.get("top_influencers", [])
    if kpi_top:
        if kpi_top[0]["importance"] > 0.8:
            gaps.append("Target heavily dependent on single feature. Model robustness risk.")

    if not gaps:
        gaps.append("No major structural gaps detected.")

    return {
        "detected_gaps": gaps,
        "total_gaps": len(gaps)
    }