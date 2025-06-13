import os
import json
from datetime import datetime

def save_scoring_output(candidate_name: str, scoring_output: str, output_dir="scored_outputs"):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Format filename with timestamp and candidate name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = candidate_name.replace(" ", "_").lower()
    filename = f"{timestamp}_{safe_name}.json"
    file_path = os.path.join(output_dir, filename)

    try:
        # If output is string (from OpenAI), convert it to proper JSON
        if isinstance(scoring_output, str):
            scoring_output = json.loads(scoring_output)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(scoring_output, f, indent=2, ensure_ascii=False)

        return {"status": "success", "path": file_path}
    except Exception as e:
        return {"status": "error", "message": str(e)}
