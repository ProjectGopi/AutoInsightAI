from fastapi import FastAPI
from app.database import engine, Base
from app.models import dataset_model
from app.api import upload
from fastapi.middleware.cors import CORSMiddleware
from app.database import SessionLocal
from app.models.dataset_model import Dataset
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AutoInsight AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(upload.router)

@app.get("/")
def root():
    return {"message": "AutoInsight AI Backend Running Successfully"}

@app.get("/datasets")
def get_all_datasets():
    db = SessionLocal()
    datasets = db.query(Dataset).all()

    result = []
    for dataset in datasets:
        result.append({
            "id": dataset.id,
            "filename": dataset.filename,
            "status": dataset.status
        })

    db.close()
    return result