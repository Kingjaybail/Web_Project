import React, { useState } from "react";
import "./models.scss";
import router_functions from "../../Routes/routes";
import { parseDataset } from "../../utils/parseDataset"; 
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  ResponsiveContainer
} from "recharts";

export default function Models() {
  const [dataset, setDataset] = useState(null);
  const [modelType, setModelType] = useState("");
  const [status, setStatus] = useState(null);
  const [results, setResults] = useState(null);
  const [columns, setColumns] = useState([]);
  const [targetColumn, setTargetColumn] = useState("");

  const modelEndpointMap = {
    "Linear Regression": "linear-regression",
    "Logistic Regression": "logistic-regression",
    "Decision Tree": "decision-trees",
    "Random Forest": "random-forest",
    "Bagging": "bagging",
    "Boosting": "boosting",
    "Support Vector Machine (SVM)": "svm",
    "Custom Deep Neural Network": "deep-neural-network",
  };

  const availableModels = Object.keys(modelEndpointMap);

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

  async function handleSubmit(e) {
    e.preventDefault();
    setResults(null);
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
        <div className="form-group">
          <label>Upload Dataset (.txt, .csv, .xlsx)</label>
          <input type="file" accept=".txt,.csv,.xlsx,.xls" onChange={handleFileUpload} />
          {dataset && <p className="file-name">{dataset.name}</p>}
        </div>

        {columns.length > 0 && (
          <div className="form-group">
            <label>Select Target Column</label>
            <select value={targetColumn} onChange={(e) => setTargetColumn(e.target.value)} required>
              <option value="">-- Choose Target Column --</option>
              {columns.map((col) => (
                <option key={col} value={col}>
                  {col}
                </option>
              ))}
            </select>
          </div>
        )}

        <div className="form-group">
          <label>Select Model Type</label>
          <select value={modelType} onChange={(e) => setModelType(e.target.value)} required>
            <option value="">-- Choose a Model --</option>
            {availableModels.map((m) => (
              <option key={m} value={m}>
                {m}
              </option>
            ))}
          </select>
        </div>

        <button type="submit" className="submit-button">Run Model</button>
      </form>

      {status && <p className="status">{status}</p>}

      {results && (
        <section className="results-section">
          <h2>{results.model}</h2>
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
                    <td>
                      {Array.isArray(value)
                        ? `${value.length}x${value[0].length} matrix`
                        : value}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          {results.coefficients && (
            <>
              <h3>Feature Coefficients</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart
                  data={Object.entries(results.coefficients).map(([key, value]) => ({
                    feature: key,
                    coefficient: value,
                  }))}
                  margin={{ top: 10, right: 30, left: 10, bottom: 50 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="feature" angle={-45} textAnchor="end" height={70} />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="coefficient" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </>
          )}

          {results.predictions_preview && (
            <>
              <h3>Actual vs Predicted</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart
                  data={results.predictions_preview.map((p, i) => ({
                    index: i + 1,
                    actual: p.actual,
                    predicted: p.predicted,
                  }))}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="index" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="actual" stroke="#82ca9d" />
                  <Line type="monotone" dataKey="predicted" stroke="#8884d8" />
                </LineChart>
              </ResponsiveContainer>
            </>
          )}
        </section>
      )}
    </div>
  );
}
