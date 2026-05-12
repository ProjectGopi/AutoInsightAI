import json
from app.core.profiler import profile_dataset
from app.core.semantic_engine import analyze_semantics
from app.core.analytics_engine import analyze_relationships
from app.core.anomaly_engine import detect_anomalies
from app.core.kpi_engine import analyze_kpi_importance
from app.core.gap_engine import detect_gaps
from app.core.insight_engine import compute_insight_scores
from app.core.powerbi_engine import prepare_powerbi_export
from app.models.dataset_model import Dataset
from app.database import SessionLocal
from app.models.settings_model import Settings


def run_full_analysis(dataset_id: int, file_path: str):

    db = SessionLocal()
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    dataset.analysis_status = "processing"
    db.commit()

    try:
        # GET SETTINGS
        settings = db.query(Settings).first()
        anomaly_level = settings.anomaly_level if settings else "medium"

        # DETERMINE THRESHOLD
        if anomaly_level == "low":
            threshold = 3.5
        elif anomaly_level == "high":
            threshold = 2.0
        else:
            threshold = 3.0

        # RUN ENGINES (file_path based)
        profile_report = profile_dataset(file_path)
        semantic_report = analyze_semantics(file_path)
        relationship_report = analyze_relationships(file_path)
        anomaly_reports = detect_anomalies(file_path, threshold=threshold)
        kpi_report = analyze_kpi_importance(file_path, semantic_report)
        gap_report = detect_gaps(
            profile_report,
            semantic_report,
            relationship_report,
            anomaly_reports,
            kpi_report
        )
        insight_report = compute_insight_scores(
            profile_report,
            relationship_report,
            anomaly_reports,
            kpi_report
        )
        powerbi_report = prepare_powerbi_export(
            file_path,
            semantic_report,
            relationship_report
        )

        full_result = {
            "profile_summary": profile_report,
            "semantic_insights": semantic_report,
            "relationship_insights": relationship_report,
            "anomaly_insights": anomaly_reports,
            "kpi_insights": kpi_report,
            "gap_analysis": gap_report,
            "ranked_insights": insight_report
        }

        dataset.analysis_result = json.dumps(full_result)
        dataset.powerbi_result = json.dumps(powerbi_report)
        dataset.analysis_status = "completed"

        db.commit()

    except Exception as e:
        dataset.analysis_status = "failed"
        db.commit()
        print("Analysis error:", str(e))

    finally:
        db.close()