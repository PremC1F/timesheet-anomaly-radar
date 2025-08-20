"""
FastAPI service for Timesheet Anomaly Radar demo.

This service reads a synthetic timesheet dataset, identifies rows flagged as
anomalies, and exposes a couple of endpoints:

 - GET /api/health: returns a simple status check.
 - GET /api/anomalies: returns a list of anomaly records, optionally filtered
   by team or date.
 - POST /api/decision: accepts a decision on an anomaly record. Decisions
   are appended to a CSV file for later analysis. This endpoint accepts
   JSON body with fields: record_id (int), decision (str), and an optional
   note (str).

The dataset is loaded from ``data.csv`` in the same directory. If you make
changes to the dataset, restart the service to pick up those changes.

To run this app locally:

1. Install dependencies:
    pip install fastapi uvicorn pandas pydantic
2. Start the server:
    uvicorn app:app --reload
3. Access the API at http://localhost:8000/api/anomalies

This file is intentionally lightweight—no advanced model training here. It
serves as a companion API to be consumed by a Rippling App Studio app.
"""

from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import os


DATA_PATH = os.path.join(os.path.dirname(__file__), "data.csv")
DECISIONS_PATH = os.path.join(os.path.dirname(__file__), "decisions.csv")


class Decision(BaseModel):
    record_id: int
    decision: str
    note: Optional[str] = None


app = FastAPI(
    title="Timesheet Anomaly Radar API",
    description="API for detecting and managing timesheet anomalies",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


def load_data() -> pd.DataFrame:
    """Load the timesheet dataset from CSV into a DataFrame."""
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        raise RuntimeError(f"Dataset not found at {DATA_PATH}")
    return df


@app.get("/api/health", tags=["Health"])
def health_check():
    """Return a simple health status."""
    return {"status": "ok"}


@app.get("/api/anomalies", tags=["Anomalies"])
def get_anomalies(team: Optional[str] = None, date: Optional[str] = None) -> List[dict]:
    """
    Return a list of anomaly records.

    Query parameters:
    - team: filter by team name (case-insensitive)
    - date: filter by ISO date string (YYYY-MM-DD)

    Returns a list of dictionaries keyed by field names. Only rows where the
    ``anomaly`` column equals 1 are included.
    """
    df = load_data()
    # Filter to anomalies
    anomalies = df[df["anomaly"] == 1].copy()
    # Apply optional filters
    if team:
        anomalies = anomalies[anomalies["team"].str.lower() == team.lower()]
    if date:
        anomalies = anomalies[anomalies["date"] == date]
    # Select relevant fields
    fields = [
        "record_id",
        "employee_id",
        "employee_name",
        "team",
        "date",
        "scheduled_start",
        "scheduled_end",
        "actual_start",
        "actual_end",
        "location",
        "anomaly_reason",
        "anomaly_score",
    ]
    result = anomalies[fields].to_dict(orient="records")
    return result


@app.post("/api/decision", tags=["Decisions"])
def post_decision(decision: Decision):
    """
    Record a decision on a given anomaly record.

    The decision is appended to ``decisions.csv`` with a timestamp. This
    endpoint always returns ``{"status": "recorded"}`` on success.
    """
    # Load dataset to ensure record_id exists
    df = load_data()
    if decision.record_id not in df["record_id"].values:
        raise HTTPException(status_code=404, detail="record_id not found")

    # Append decision to file
    row = {
        "record_id": decision.record_id,
        "decision": decision.decision,
        "note": decision.note or "",
    }
    # Create file if it doesn't exist
    if not os.path.exists(DECISIONS_PATH):
        decisions_df = pd.DataFrame([row])
        decisions_df.to_csv(DECISIONS_PATH, index=False)
    else:
        decisions_df = pd.read_csv(DECISIONS_PATH)
        decisions_df = pd.concat([decisions_df, pd.DataFrame([row])], ignore_index=True)
        decisions_df.to_csv(DECISIONS_PATH, index=False)

    return {"status": "recorded"}
