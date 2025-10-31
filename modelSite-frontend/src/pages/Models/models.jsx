import React, { useState } from "react";
import "./models.scss";
import router_functions from "../../Routes/routes";
import { parseDataset } from "../../utils/parseDataset"; 

export default function Models() {
  const [dataset, setDataset] = useState(null);
  const [modelType, setModelType] = useState("");
  const [metrics, setMetrics] = useState([]);
  const [status, setStatus] = useState(null);
  const [results, setResults] = useState(null);

  const [columns, setColumns] = useState([]);       
  const [targetColumn, setTargetColumn] = useState(""); 

  const modelEndpointMap = {
    "Linear Regression": "linear-regression",
    "Logistic Regression": "logistic-regression",
    "Decision Tree": "decision-tree",
    "Random Forest": "random-forest",
    "Bagging": "bagging",
    "Boosting": "boosting",
    "Support Vector Machine (SVM)": "svm",
    "Custom Deep Neural Network": "dnn",
  };

  const availableModels = Object.keys(modelEndpointMap);
  const availableMetrics = [
    "Accuracy", "Precision", "Recall", "F1 Score", "ROC Curve", "Confusion Matrix"
  ];

  async function handleFileUpload(e) {
    const file = e.target.files[0];
    setDataset(file);
    setStatus("Parsing dataset...");

    try {
      const { columns } = await parseDataset(file);
      setColumns(columns);
      setStatus(`Parsed ${columns.length} columns successfully.`);
    } catch (err) {
      console.error("Error parsing dataset:", err);
      setStatus("Failed to parse dataset.");
    }
  }

  function handleMetricChange(metric) {
    setMetrics((prev) =>
      prev.includes(metric)
        ? prev.filter((m) => m !== metric)
        : [...prev, metric]
    );
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setResults(null)
    if (!dataset || !modelType || !targetColumn) {
      setStatus("Please upload a dataset, select a model, and choose a target column.");
      return;
    }

    setStatus("Training model...");

    try {
      const endpoint = modelEndpointMap[modelType];
      const formData = new FormData();
      formData.append("file", dataset);
      formData.append("target_column", targetColumn);
      formData.append("metrics", JSON.stringify(metrics));

      const response = await router_functions.runModel(endpoint, formData);
      setResults(response);
      setStatus("Model trained successfully!");
    } catch (err) {
      console.error(err);
      setStatus("Error training model. Please try again.");
    }
  }

  return (
    <div className="models-page">
      <h1>Model Workspace</h1>
      <p className="subtitle">
        Upload data, select your model, evaluate results, and visualize performance.
      </p>

      <form className="model-form" onSubmit={handleSubmit}>
        {/* Dataset Upload */}
        <div className="form-group">
          <label>Upload Dataset (.txt, .csv, .xlsx)</label>
          <input
            type="file"
            accept=".txt,.csv,.xlsx,.xls"
            onChange={handleFileUpload}
          />
          {dataset && <p className="file-name">{dataset.name}</p>}
        </div>

        {/* Target Column Selection */}
        {columns.length > 0 && (
          <div className="form-group">
            <label>Select Target Column</label>
            <select
              value={targetColumn}
              onChange={(e) => setTargetColumn(e.target.value)}
              required
            >
              <option value="">-- Choose Target Column --</option>
              {columns.map((col) => (
                <option key={col} value={col}>
                  {col}
                </option>
              ))}
            </select>
          </div>
        )}

        {/* Model Selection */}
        <div className="form-group">
          <label>Select Model Type</label>
          <select
            value={modelType}
            onChange={(e) => setModelType(e.target.value)}
            required
          >
            <option value="">-- Choose a Model --</option>
            {availableModels.map((m) => (
              <option key={m} value={m}>
                {m}
              </option>
            ))}
          </select>
        </div>

        {/* Metric Selection */}
        <div className="form-group">
          <label>Select Evaluation Metrics</label>
          <div className="checkbox-grid">
            {availableMetrics.map((metric) => (
              <label key={metric} className="checkbox-item">
                <input
                  type="checkbox"
                  checked={metrics.includes(metric)}
                  onChange={() => handleMetricChange(metric)}
                />
                {metric}
              </label>
            ))}
          </div>
        </div>

        <button type="submit" className="submit-button">
          Run Model
        </button>
      </form>

      {status && <p className="status">{status}</p>}

      {results && (
        <section className="results-section">
          <h2>Results Visualization</h2>
          <div className="charts-placeholder">
            <h3>{results.model}</h3>
            <p>{results.message}</p>

            {results.metrics && (
              <table className="results-table">
                <thead>
                  <tr>
                    <th>Metric</th>
                    <th>Value</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(results.metrics).map(([key, value]) => (
                    <tr key={key}>
                      <td>{key}</td>
                      <td>{value}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </section>
      )}
    </div>
  );
}
