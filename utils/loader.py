import os
import json

RESUMES_FOLDER = "resumes_parsed"

def load_parsed_resume(filename):
    filepath = os.path.join(RESUMES_FOLDER, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File {filename} not found in parsed resumes folder")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data