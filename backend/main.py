from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import csv

app = FastAPI()

# -------------------------------------------------
# Root endpoint (health check)
# -------------------------------------------------
@app.get("/")
async def root():
    return {"message": "Threat Agent backend is running 🚀"}

# -------------------------------------------------
# Allow frontend access (CORS)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins in dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Upload logs endpoint (with safe decoding + fixed classification)
# -------------------------------------------------
@app.post("/upload-logs/")
async def upload_logs(file: UploadFile = File(...)):
    if not (file.filename.endswith(".log") or file.filename.endswith(".csv")):
        return {"error": "Only .log or .csv files are allowed"}

    # Read uploaded file
    content = await file.read()

    # Safe decoding (UTF-8 first, fallback to latin-1 for Windows files)
    try:
        lines = content.decode("utf-8").splitlines()
    except UnicodeDecodeError:
        lines = content.decode("latin-1").splitlines()

    # Debug print (you will see this in your terminal)
    print("DEBUG: filename =", file.filename)
    print("DEBUG: size =", len(content))
    print("DEBUG: first line =", lines[0] if lines else "EMPTY FILE")

    # Parse CSV vs LOG
    if file.filename.endswith(".csv"):
        reader = csv.reader(lines)
        logs = [",".join(row) for row in reader]
    else:
        logs = lines

    # If empty file
    if not logs:
        return {"results": []}

    # Simple classification (fixed: clean line before checking)
    results = []
    for idx, log in enumerate(logs[:5]):  # only first 5 lines
        clean_log = log.strip().lower()   # 🔥 normalize log line

        if "login" in clean_log:
            threat = "Insider Threat"
            severity = "Medium"
            mitigation = "Enable MFA, review login attempts"
        elif "suspicious" in clean_log or "exe" in clean_log:
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