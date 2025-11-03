import React, { useState } from "react";
import "./models.scss";
import router_functions from "../../Routes/routes";
import { parseDataset } from "../../utils/parseDataset";
import CustomNNModal from "../../utils/customnnmodals/customNNModal";

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
  const [showNNModal, setShowNNModal] = useState(false);
  const [nnConfig, setNNConfig] = useState(null);

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

  const handleModelChange = (e) => {
    const selected = e.target.value;
    setModelType(selected);
    if (selected === "Custom Deep Neural Network") setShowNNModal(true);
  };

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

      if (modelType === "Custom Deep Neural Network") {
        const combinedData = {
          target_column: targetColumn,
          model_config: nnConfig || {},
        };
        formData.append("request_data", JSON.stringify(combinedData));
      }

      const response = await router_functions.runModel(endpoint, formData);

      if (response.error) {
        setResults(response);
        setStatus(`${response.error}`);
        return;
      }

      setResults(response);
      setStatus("Model trained successfully!");

      // ✅ Save run to database for later comparison
      const username = localStorage.getItem("username") || "guest";
      const saveData = new FormData();
      saveData.append("username", username);
      saveData.append("dataset_name", dataset.name);
      saveData.append("model_type", response.model_type || modelType);
      saveData.append("target_column", targetColumn);
      saveData.append("metrics", JSON.stringify(response.metrics));

      await fetch("http://127.0.0.1:8000/save-model-result", {
        method: "POST",
        body: saveData,
      });
    } catch (err) {
      console.error("Error:", err);
      setStatus("Error training model. Please try again.");
    }
  }

  return (
    <div className="models-page">
      <h1>Model Workspace</h1>
      <p className="subtitle">
        Upload data, select your model, evaluate results, and visualize performance.
      </p>

      {/* Upload + Config Form */}
      <form className="model-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Upload Dataset (.txt, .csv, .xlsx)</label>
          <input type="file" accept=".txt,.csv,.xlsx,.xls" onChange={handleFileUpload} />
          {dataset && <p className="file-name">{dataset.name}</p>}
        </div>

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

        <div className="form-group">
          <label>Select Model Type</label>
          <select value={modelType} onChange={handleModelChange} required>
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

      {/* Results Section */}
      {results && (
        <section className="results-section">
          {"error" in results ? (
            <div className="error-box">
              <h2>Model Error</h2>
              <p>{results.error}</p>
            </div>
          ) : (
            <>
              <h2>{results.model_type || results.model}</h2>
              <p>{results.message || "Model ran successfully."}</p>

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
            </>
          )}
        </section>
      )}

      <CustomNNModal
        isOpen={showNNModal}
        onClose={() => setShowNNModal(false)}
        onSave={(config) => setNNConfig(config)}
      />
    </div>
  );
}
