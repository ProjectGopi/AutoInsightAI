def compute_insight_scores(
    profile_report,
    relationship_report,
    anomaly_report,
    kpi_report
):

    insights = []

    data_quality_weight = profile_report.get("data_quality_score", 50) / 100

    # Correlation insight scoring
    for pair in relationship_report.get("strong_correlations", []):
        strength = abs(pair["correlation"])
        score = round(strength * data_quality_weight, 3)

        insights.append({
            "type": "correlation",
            "description": f"{pair['feature_1']} strongly related to {pair['feature_2']}",
            "score": score
        })

    # KPI importance scoring
    top_features = kpi_report.get("top_influencers", [])
    for feat in top_features:
        score = round(feat["importance"] * data_quality_weight, 3)

        insights.append({
            "type": "kpi_driver",
            "description": f"{feat['feature']} strongly influences target",
            "score": score
        })

    # Anomaly insight scoring
    anomaly_percentage = anomaly_report.get("anomaly_percentage", 0)
    anomaly_strength = anomaly_percentage / 100

    score = round(anomaly_strength * data_quality_weight, 3)

    insights.append({
        "type": "anomaly_risk",
        "description": f"{anomaly_percentage}% anomalies detected",
        "score": score
    })

    # Sort by score descending
    insights = sorted(insights, key=lambda x: x["score"], reverse=True)

    return {
        "ranked_insights": insights[:5],
        "total_insights_generated": len(insights)
    }