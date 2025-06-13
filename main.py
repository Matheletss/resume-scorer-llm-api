from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
import os
from utils.scorer import score_resume_against_jd

app = FastAPI(title="Resume Scorer API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PARSED_RESUMES_DIR = "resumes_parsed"

class JobDescription(BaseModel):
    title: str
    description: str

def load_job_description(filepath="job_description/job_description.txt"):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/resumes")
def list_parsed_resumes():
    try:
        files = [f for f in os.listdir(PARSED_RESUMES_DIR) if f.endswith(".json")]
        return {"resumes": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/score/{resume_file}")
def score_resume(resume_file: str):
    file_path = os.path.join(PARSED_RESUMES_DIR, resume_file)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Resume file not found")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        messages = data["messages"]
        parsed_resume = messages[-1]["content"]

        job_description = load_job_description()

        # ✅ Extract candidate name for file naming
        candidate_name = data.get("name", "unknown")

        return score_resume_against_jd(parsed_resume, job_description, candidate_name)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

