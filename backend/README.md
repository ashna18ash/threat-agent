# 🚨 Threat Agent – AI Cybersecurity Log Analyzer

This project analyzes system logs and classifies them into threat categories (Insider Threat, Phishing/Malware, Benign).
It uses **FastAPI** for backend and a simple **HTML/CSS frontend** for visualization.

---

## 📊 Sample Output

Here’s how the results look for `sample1.log`:

### Summary Cards
- 🔴 High: 1  
- 🟠 Medium: 1  
- 🟢 Low: 1  

### Table Output

![Threat Table](assets/output.png)

---

## ⚡ How to Run Locally

### Backend (FastAPI)
```bash
cd backend
uvicorn main:app --reload
