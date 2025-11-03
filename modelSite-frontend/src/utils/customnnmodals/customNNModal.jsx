import React, { useState } from "react";
import "./customNNModal.scss";

export default function CustomNNModal({ isOpen, onClose, onSave }) {
  const [layers, setLayers] = useState([{ units: 32, activation: "relu" }]);
  const [learningRate, setLearningRate] = useState(0.001);
  const [epochs, setEpochs] = useState(50);
  const [batchSize, setBatchSize] = useState(16);
  const [problemType, setProblemType] = useState("regression");

  if (!isOpen) return null;

  const handleLayerChange = (index, field, value) => {
    const updated = [...layers];
    updated[index][field] = field === "units" ? parseInt(value) || 0 : value;
    setLayers(updated);
  };

  const addLayer = () => {
    setLayers([...layers, { units: 16, activation: "relu" }]);
  };

  const removeLayer = (index) => {
    const updated = layers.filter((_, i) => i !== index);
    setLayers(updated);
  };

  const handleSave = () => {
    const config = {
      layers,
      learning_rate: parseFloat(learningRate),
      epochs: parseInt(epochs),
      batch_size: parseInt(batchSize),
      problem_type: problemType,
    };
    onSave(config);
    onClose();
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Configure Custom Neural Network</h2>

        <div className="modal-section">
          <label>Learning Rate:</label>
          <input
            type="number"
            step="0.0001"
            value={learningRate}
            onChange={(e) => setLearningRate(e.target.value)}
          />
        </div>

        <div className="modal-section">
          <label>Epochs:</label>
          <input
            type="number"
            value={epochs}
            onChange={(e) => setEpochs(e.target.value)}
          />
        </div>

        <div className="modal-section">
          <label>Batch Size:</label>
          <input
            type="number"
            value={batchSize}
            onChange={(e) => setBatchSize(e.target.value)}
          />
        </div>

        <div className="modal-section">
          <label>Problem Type:</label>
          <select value={problemType} onChange={(e) => setProblemType(e.target.value)}>
            <option value="regression">Regression</option>
            <option value="classification">Classification</option>
          </select>
        </div>

        <div className="modal-section layers-section">
          <label>Layers:</label>
          {layers.map((layer, index) => (
            <div key={index} className="layer-row">
              <input
                type="number"
                placeholder="Units"
                value={layer.units}
                onChange={(e) => handleLayerChange(index, "units", e.target.value)}
              />
              <select
                value={layer.activation}
                onChange={(e) => handleLayerChange(index, "activation", e.target.value)}
              >
                <option value="relu">ReLU</option>
                <option value="sigmoid">Sigmoid</option>
                <option value="tanh">Tanh</option>
              </select>
              <button type="button" onClick={() => removeLayer(index)}>
                ✖
              </button>
            </div>
          ))}
          <button type="button" onClick={addLayer} className="add-layer">
            + Add Layer
          </button>
        </div>

        <div className="modal-actions">
          <button onClick={handleSave} className="save-btn">Save</button>
          <button onClick={onClose} className="cancel-btn">Cancel</button>
        </div>
      </div>
    </div>
  );
}
