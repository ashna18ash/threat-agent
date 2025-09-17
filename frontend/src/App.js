import React, { useState } from "react";
import "./App.css";

function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) {
      setError("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setError("");

    try {
      const res = await fetch("http://127.0.0.1:8000/upload-logs/", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }

      const data = await res.json();
      console.log("Backend response:", data);

      if (data.results && data.results.length > 0) {
        setResults(data.results);
      } else {
        setResults([]);
        setError("No threats detected or log file empty.");
      }
    } catch (err) {
      console.error("Error uploading file:", err);
      setError("Failed to upload or analyze file.");
    }

    setLoading(false);
  };

  // Count summary
  const summary = {
    High: results.filter((r) => r.severity === "High").length,
    Medium: results.filter((r) => r.severity === "Medium").length,
    Low: results.filter((r) => r.severity === "Low").length,
  };

  const severityBadge = (severity) => {
    const colors = {
      High: "badge badge-high",
      Medium: "badge badge-medium",
      Low: "badge badge-low",
    };
    return <span className={colors[severity]}>{severity}</span>;
  };

  return (
    <div className="dashboard">
      <h1>🛡 Threat Agent – Intelligence Dashboard</h1>
      <p>Upload your .log or .csv file to analyze security threats.</p>

      {/* File Upload */}
      <input type="file" onChange={handleUpload} className="upload-btn" />

      {loading && <p className="loading">Analyzing logs... please wait 🔍</p>}
      {error && <p className="error">{error}</p>}

      {/* Threat Summary */}
      {results.length > 0 && (
        <div className="summary">
          <div className="summary-card high">High: {summary.High}</div>
          <div className="summary-card medium">Medium: {summary.Medium}</div>
          <div className="summary-card low">Low: {summary.Low}</div>
        </div>
      )}

      {/* Results Table */}
      {results.length > 0 && (
        <div className="table-container">
          <table className="results-table">
            <thead>
              <tr>
                <th>Incident</th>
                <th>Log</th>
                <th>Threat Type</th>
                <th>Severity</th>
                <th>Mitigation</th>
              </tr>
            </thead>
            <tbody>
              {results.map((r, i) => (
                <tr key={i}>
                  <td>{r.incident}</td>
                  <td>{r.log}</td>
                  <td>{r.threat}</td>
                  <td>{severityBadge(r.severity)}</td>
                  <td>{r.mitigation}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;