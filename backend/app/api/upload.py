import os
import pandas as pd
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.dataset_model import Dataset
from app.core.profiler import profile_dataset
from app.core.semantic_engine import analyze_semantics
from app.core.analytics_engine import analyze_relationships
from app.core.anomaly_engine import detect_anomalies
from app.core.kpi_engine import analyze_kpi_importance
from app.core.gap_engine import detect_gaps
from app.core.insight_engine import compute_insight_scores
from app.core.powerbi_engine import prepare_powerbi_export
from fastapi import BackgroundTasks
from app.services.analysis_service import run_full_analysis
from app.models.settings_model import Settings

router = APIRouter()

UPLOAD_DIRECTORY = "uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):

    file_location = f"uploaded_files/{file.filename}"

    with open(file_location, "wb") as f:
        f.write(await file.read())

    db = SessionLocal()

    dataset = Dataset(
        filename=file.filename,
        filepath=file_location,
        analysis_status="uploaded"
    )

    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    db.close()

    return {
        "message": "File uploaded successfully",
        "dataset_id": dataset.id,
        "status": "uploaded"
    }

@router.post("/analyze/{dataset_id}")
def analyze_dataset(dataset_id: int, background_tasks: BackgroundTasks):

    db = SessionLocal()
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        return {"error": "Dataset not found"}

    background_tasks.add_task(
        run_full_analysis,
        dataset_id,
        dataset.filepath
    )

    db.close()

    return {
        "message": "Analysis started",
        "dataset_id": dataset_id,
        "status": "processing"
    }

@router.get("/results/{dataset_id}")
def get_results(dataset_id: int):

    db = SessionLocal()
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        return {"error": "Dataset not found"}

    db.close()

    import json

    return {
        "dataset_id": dataset_id,
        "status": dataset.analysis_status,
        "results": json.loads(dataset.analysis_result) if dataset.analysis_result else None
    }

@router.get("/powerbi/{dataset_id}")
def get_powerbi_export(dataset_id: int):

    db = SessionLocal()
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        return {"error": "Dataset not found"}

    db.close()

    import json

    return {
        "dataset_id": dataset_id,
        "status": dataset.analysis_status,
        "results": json.loads(dataset.analysis_result) if dataset.analysis_result else None
    }

@router.get("/datasets")
def get_all_datasets():

    db = SessionLocal()
    datasets = db.query(Dataset).all()

    result = []
    for dataset in datasets:
        result.append({
            "id": dataset.id,
            "filename": dataset.filename,
            "status": dataset.analysis_status
        })

    db.close()
    return result

@router.delete("/datasets/{dataset_id}")
def delete_dataset(dataset_id: int):

    db = SessionLocal()
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        db.close()
        return {"error": "Dataset not found"}

    # Delete file from disk
    if os.path.exists(dataset.filepath):
        os.remove(dataset.filepath)

    db.delete(dataset)
    db.commit()
    db.close()

    return {"message": "Dataset deleted successfully"}

@router.get("/settings")
def get_settings():
    db = SessionLocal()
    settings = db.query(Settings).first()

    if not settings:
        settings = Settings()
        db.add(settings)
        db.commit()
        db.refresh(settings)

    db.close()

    return {
        "anomaly_level": settings.anomaly_level,
        "auto_analyze": settings.auto_analyze,
        "default_target": settings.default_target,
        "dark_mode": settings.dark_mode
    }


@router.put("/settings")
def update_settings(data: dict):
    db = SessionLocal()
    settings = db.query(Settings).first()

    if not settings:
        settings = Settings()

    settings.anomaly_level = data.get("anomaly_level")
    settings.auto_analyze = data.get("auto_analyze")
    settings.default_target = data.get("default_target")
    settings.dark_mode = data.get("dark_mode")

    db.add(settings)
    db.commit()
    db.close()

    return {"message": "Settings updated successfully"}