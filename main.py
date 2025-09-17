from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import csv

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-logs/")
async def upload_logs(file: UploadFile = File(...)):
    if not (file.filename.endswith(".log") or file.filename.endswith(".csv")):
        return {"error": "Only .log or .csv files are allowed"}

    content = await file.read()
    lines = content.decode("utf-8").splitlines()

    if file.filename.endswith(".csv"):
        reader = csv.reader(lines)
        logs = [",".join(row) for row in reader]
    else:
        logs = lines

    results = []
    for idx, log in enumerate(logs[:5]):
        if "login" in log.lower():
            threat = "Insider Threat"
            severity = "Medium"
            mitigation = "Enable MFA, review login attempts"
        elif "suspicious" in log.lower() or "exe" in log.lower():
            threat = "Phishing / Malware"
            severity = "High"
            mitigation = "Block sender IP, reset accounts"
        else:
            threat = "Benign"
            severity = "Low"
            mitigation = "No action required"

        results.append({
            "incident": idx + 1,
            "log": log,
            "threat": threat,
            "severity": severity,
            "mitigation": mitigation
        })

    return {"results": results}