import React, { useState } from "react";
import axios from "axios";
import "./UploadFormComponent.css";

const UploadFormComponent = () => {
  const [files, setFiles] = useState({
    ipynb: null,
    pkl: null,
    dataset: null,
  });

  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleFileChange = (e) => {
    setFiles({ ...files, [e.target.name]: e.target.files[0] });
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("ipynb", files.ipynb);
    formData.append("pkl", files.pkl);
    formData.append("dataset", files.dataset);

    try {
      const response = await axios.post("http://127.0.0.1:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      alert("Upload Successful!");
      console.log(response.data);
      setUploadSuccess(true); // Enable "Generate" button after successful upload
    } catch (error) {
      console.error("Upload failed", error);
      alert("Upload failed. Check console for details.");
    }
  };

  const handleGenerate = async () => {
    if (!uploadSuccess) {
      alert("Please upload the required files first.");
      return;
    }

    setIsGenerating(true);

    try {
      const response = await axios.post("http://127.0.0.1:8000/generate", {}); // Endpoint to generate backend & frontend

      alert("Backend & Frontend Generation Successful!");
      console.log(response.data);
    } catch (error) {
      console.error("Generation failed", error);
      alert("Generation failed. Check console for details.");
    }

    setIsGenerating(false);
  };

  return (
    <div className="upload-container">
      <h2>Upload Model Files</h2>

      <label>
        <strong>Jupyter Notebook File (.ipynb)</strong>
      </label>
      <input type="file" name="ipynb" onChange={handleFileChange} accept=".ipynb" />

      <label>
        <strong>Model Weights File (.pkl)</strong>
      </label>
      <input type="file" name="pkl" onChange={handleFileChange} accept=".pkl" />

      <label>
        <strong>Dataset File (.csv, .xlsx)</strong>
      </label>
      <input type="file" name="dataset" onChange={handleFileChange} accept=".csv, .xlsx" />

      <button onClick={handleUpload}>Upload</button>

      {/* Generate Button (Only enabled after upload) */}
      <button onClick={handleGenerate} disabled={!uploadSuccess || isGenerating}>
        {isGenerating ? "Generating..." : "Generate Backend & Frontend"}
      </button>
    </div>
  );
};

export default UploadFormComponent;
