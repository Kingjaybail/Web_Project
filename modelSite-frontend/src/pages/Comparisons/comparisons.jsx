import React, { useEffect, useState } from "react";
import "./comparisons.scss";
import {
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  ResponsiveContainer,
} from "recharts";

export default function Comparisons() {
  const [comparisonResults, setComparisonResults] = useState([]);
  const [groupedResults, setGroupedResults] = useState({});
  const [status, setStatus] = useState("Loading...");

  // Fetch user history from backend
  useEffect(() => {
    async function loadHistory() {
      const username = localStorage.getItem("username");
      if (!username) {
        setStatus("Please log in to view comparisons.");
        return;
      }
        console.log(username)
      try {
        const res = await fetch(`http://127.0.0.1:8000/model-history/${username}`);
        const data = await res.json();

        if (data.history && data.history.length > 0) {
          setComparisonResults(data.history);
          setStatus("Comparison data loaded successfully.");

          // Group by dataset name
          const grouped = data.history.reduce((acc, item) => {
            const key = item.dataset_name || "Unknown Dataset";
            if (!acc[key]) acc[key] = [];
            acc[key].push(item);
            return acc;
          }, {});
          setGroupedResults(grouped);
        } else {
          setComparisonResults([]);
          setGroupedResults({});
          setStatus("No saved model results found.");
        }
      } catch (err) {
        console.error("Failed to load model history:", err);
        setStatus("Error loading comparisons.");
      }
    }

    loadHistory();
  }, []);

  // Clear history handler
  async function handleClearHistory() {
    const username = localStorage.getItem("username");
    if (!username) {
      alert("You must be logged in to clear history.");
      return;
    }

    if (!window.confirm("Are you sure you want to delete all your saved comparisons?")) return;

    try {
      const res = await fetch(`http://127.0.0.1:8000/clear-model-history/${username}`, {
        method: "DELETE",
      });
      const data = await res.json();

      if (data.error) {
        alert("Error clearing history: " + data.error);
      } else {
        alert(data.message);
        setComparisonResults([]);
        setGroupedResults({});
        setStatus("All saved comparisons cleared.");
      }
    } catch (err) {
      console.error("Failed to clear model history:", err);
      setStatus("Error clearing comparisons.");
    }
  }

  return (
    <div className="comparisons-page">
      <h1>Model Comparisons</h1>
      <p className="subtitle">
        Compare performance of your trained models grouped by dataset.
      </p>

      <p className="status">{status}</p>

      {/* Loop through dataset groups */}
      {Object.entries(groupedResults).map(([dataset, models]) => (
        <div key={dataset} className="dataset-group">
          <h2 className="dataset-title">{dataset}</h2>

          {/* Bar Chart for this dataset */}
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={models}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="model" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="metric_value" fill="#82ca9d" name="Accuracy / R² / (1/MSE)" />
              </BarChart>
            </ResponsiveContainer>


          {/* Metrics table */}
          <table className="metrics-table">
            <thead>
              <tr>
                <th>Model</th>
                <th>Primary Metric</th>
                <th>Full Metrics</th>
              </tr>
            </thead>
            <tbody>
              {models.map((m, i) => (
                <tr key={i}>
                  <td>{m.model}</td>
                  <td>{m.metric?.toFixed(4)}</td>
                  <td>
                    {typeof m.metrics === "string"
                      ? m.metrics
                      : JSON.stringify(m.metrics, null, 2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}

      {comparisonResults.length > 0 && (
        <button className="clear-button" onClick={handleClearHistory}>
          Clear All Comparisons
        </button>
      )}
    </div>
  );
}
