import React, { useState } from 'react';
import { Upload, FileText, X } from 'lucide-react';

const UploadOdds = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      const fileType = selectedFile.name.split('.').pop().toLowerCase();
      if (fileType === 'json' || fileType === 'csv') {
        setFile(selectedFile);
        setError(null);
        setSuccess(null);
      } else {
        setError('Only JSON and CSV files are supported');
        setFile(null);
      }
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const data = await response.json();
      
      // Show success message
      console.log('Upload successful:', data);
      setSuccess(`✅ Upload successful! Found ${data.count || 0} arbitrage opportunit${data.count === 1 ? 'y' : 'ies'}. Switching to results...`);
      
      // Wait a moment to show success message, then switch views
      setTimeout(() => {
        onUploadSuccess(data);
        setFile(null);
        setSuccess(null);
      }, 1500);
    } catch (err) {
      setError(err.message || 'Failed to upload file');
    } finally {
      setUploading(false);
    }
  };

  const clearFile = () => {
    setFile(null);
    setError(null);
    setSuccess(null);
  };

  return (
    <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
      <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
        <Upload size={20} />
        Upload Odds Data
      </h2>

      <div className="space-y-4">
        <div className="border-2 border-dashed border-slate-600 rounded-lg p-6 text-center hover:border-green-400 transition">
          <input
            type="file"
            id="file-upload"
            accept=".json,.csv"
            onChange={handleFileChange}
            className="hidden"
          />
          <label
            htmlFor="file-upload"
            className="cursor-pointer flex flex-col items-center"
          >
            <Upload size={48} className="text-slate-400 mb-3" />
            <p className="text-slate-300 mb-1">
              Click to upload or drag and drop
            </p>
            <p className="text-sm text-slate-500">
              JSON or CSV files only
            </p>
          </label>
        </div>

        {file && (
          <div className="bg-slate-700 rounded-lg p-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <FileText className="text-green-400" size={24} />
              <div>
                <p className="font-medium text-white">{file.name}</p>
                <p className="text-sm text-slate-400">
                  {(file.size / 1024).toFixed(2)} KB
                </p>
              </div>
            </div>
            <button
              onClick={clearFile}
              className="text-slate-400 hover:text-red-400 transition"
            >
              <X size={20} />
            </button>
          </div>
        )}

        {error && (
          <div className="bg-red-900/30 border border-red-500 rounded-lg p-3">
            <p className="text-red-400 text-sm">{error}</p>
          </div>
        )}

        {success && (
          <div className="bg-green-900/30 border border-green-500 rounded-lg p-3">
            <p className="text-green-400 text-sm">{success}</p>
          </div>
        )}

        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className={`w-full py-3 rounded font-semibold transition ${
            !file || uploading
              ? 'bg-slate-600 cursor-not-allowed'
              : 'bg-green-600 hover:bg-green-700'
          }`}
        >
          {uploading ? 'Uploading...' : 'Upload and Analyze'}
        </button>

        <div className="bg-slate-900/50 rounded p-4 text-sm text-slate-400">
          <p className="font-semibold text-slate-300 mb-2">Expected JSON format:</p>
          <pre className="bg-slate-950 rounded p-3 overflow-x-auto text-xs">
{`{
  "games": [
    {
      "match": "Team A vs Team B",
      "sport": "NBA",
      "date": "2025-10-15",
      "bookmakers": [
        {
          "name": "DraftKings",
          "home": 2.10,
          "away": 1.80
        },
        {
          "name": "FanDuel",
          "home": 1.95,
          "away": 1.95
        }
      ]
    }
  ]
}`}
          </pre>
        </div>
      </div>
    </div>
  );
};

export default UploadOdds;

