"use client";

import { useState, useEffect } from "react";
import Navbar from "@/components/layout/Navbar";
import { uploadDocument, fetchDocuments, fetchCases, CaseResponse } from "@/lib/api";
import { FileText, Shield, Upload, CheckCircle2, AlertTriangle, RefreshCw, Eye, Tag, Lock, FileCheck, Trash2 } from "lucide-react";

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<any[]>([]);
  const [cases, setCases] = useState<CaseResponse[]>([]);
  const [selectedCaseId, setSelectedCaseId] = useState<string>("");
  const [uploading, setUploading] = useState(false);
  const [loading, setLoading] = useState(true);
  const [previewDoc, setPreviewDoc] = useState<any | null>(null);
  const [uploadMessage, setUploadMessage] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    setLoading(true);
    try {
      const [docsData, casesData] = await Promise.all([
        fetchDocuments().catch(() => []),
        fetchCases().catch(() => [])
      ]);
      setDocuments(docsData);
      setCases(casesData);
      if (casesData.length > 0 && !selectedCaseId) {
        setSelectedCaseId(casesData[0].id);
      }
      if (docsData.length > 0 && !previewDoc) {
        setPreviewDoc(docsData[0]);
      }
    } catch (err) {
      console.error("Failed to load documents", err);
    } finally {
      setLoading(false);
    }
  }

  async function handleFileSelect(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!selectedCaseId && cases.length > 0) {
      setSelectedCaseId(cases[0].id);
    }

    const targetCaseId = selectedCaseId || (cases.length > 0 ? cases[0].id : "standalone_doc");

    setUploading(true);
    setUploadMessage("Executing PyMuPDF OCR & Field Intelligence Pipeline...");
    try {
      const result = await uploadDocument(targetCaseId, file);
      setUploadMessage(`Success: Extracted fields for ${file.name}`);
      await loadData();
      setPreviewDoc(result);
    } catch (err) {
      console.error("Upload error", err);
      setUploadMessage("Failed to process document. Please try again.");
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <Navbar />

      <main className="flex-1 mx-auto w-full max-w-7xl p-6 space-y-6">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2 text-xs font-bold text-blue-600 uppercase tracking-wider">
              <FileText className="h-4 w-4" />
              <span>Multimodal OCR & Field Intelligence</span>
            </div>
            <h1 className="text-2xl font-extrabold text-slate-900 mt-1">Document Intelligence Center</h1>
            <p className="text-xs text-slate-500">
              Upload electricity bills, land survey records, or receipts to automatically extract fields and check for identity anomalies.
            </p>
          </div>
          <button
            onClick={loadData}
            className="inline-flex items-center space-x-1.5 rounded-lg border border-slate-300 bg-white px-3.5 py-2 text-xs font-bold text-slate-700 hover:bg-slate-100 transition shadow-xs self-start md:self-auto"
          >
            <RefreshCw className="h-4 w-4" />
            <span>Refresh Intelligence Data</span>
          </button>
        </div>

        {/* Upload & Link Case Panel */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
          <div className="md:col-span-5 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs flex flex-col justify-between">
            <div>
              <h2 className="text-sm font-bold text-slate-900 mb-1">Upload & Process Document</h2>
              <p className="text-xs text-slate-500 mb-4">Supports PDF, PNG, JPG, JPEG documents up to 15MB.</p>

              {/* Select Case Association */}
              <div className="mb-4">
                <label className="block text-xs font-bold text-slate-700 mb-1">Associate with Case:</label>
                <select
                  value={selectedCaseId}
                  onChange={(e) => setSelectedCaseId(e.target.value)}
                  className="w-full rounded-lg border border-slate-300 bg-slate-50 p-2.5 text-xs font-semibold text-slate-800 outline-none focus:border-blue-500"
                >
                  {cases.length === 0 ? (
                    <option value="">No Active Cases (Standalone Inspection)</option>
                  ) : (
                    cases.map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.title.substring(0, 45)}... ({c.domain})
                      </option>
                    ))
                  )}
                </select>
              </div>

              {/* Upload Drop Area */}
              <label className="group relative flex flex-col items-center justify-center rounded-xl border-2 border-dashed border-slate-300 bg-slate-50/50 p-8 text-center hover:border-blue-500 hover:bg-blue-50/30 transition cursor-pointer">
                <Upload className="h-10 w-10 text-slate-400 group-hover:text-blue-600 transition mb-2" />
                <span className="text-xs font-bold text-slate-800 group-hover:text-blue-600">
                  {uploading ? "Processing Document with PyMuPDF..." : "Click or Drag File to Upload"}
                </span>
                <span className="text-[11px] text-slate-400 mt-1">PDF, Scanned Bills, Land Records, Receipts</span>
                <input
                  type="file"
                  accept=".pdf,.png,.jpg,.jpeg"
                  onChange={handleFileSelect}
                  disabled={uploading}
                  className="absolute inset-0 opacity-0 cursor-pointer"
                />
              </label>

              {uploadMessage && (
                <div className={`mt-3 p-3 rounded-lg text-xs font-semibold flex items-center space-x-2 ${
                  uploadMessage.startsWith("Success") ? "bg-emerald-50 text-emerald-800 border border-emerald-200" : "bg-blue-50 text-blue-800 border border-blue-200"
                }`}>
                  <FileCheck className="h-4 w-4 text-emerald-600 shrink-0" />
                  <span>{uploadMessage}</span>
                </div>
              )}
            </div>

            {/* Document Trust Boundary Banner */}
            <div className="mt-6 p-3 rounded-xl bg-slate-100 border border-slate-200 flex items-center space-x-2 text-[11px] text-slate-600">
              <Lock className="h-4 w-4 text-slate-400 shrink-0" />
              <span>
                All document contents are wrapped in <code className="font-mono text-slate-900 bg-slate-200 px-1 py-0.5 rounded">&lt;DOCUMENT_DATA_UNTRUSTED&gt;</code> bounds to defend against prompt injection attacks.
              </span>
            </div>
          </div>

          {/* Document Preview & Field Inspector Panel */}
          <div className="md:col-span-7 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs flex flex-col">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
              <div>
                <h3 className="text-sm font-bold text-slate-900 flex items-center space-x-2">
                  <FileCheck className="h-4 w-4 text-blue-600" />
                  <span>Extracted Field Intelligence</span>
                </h3>
                <p className="text-[11px] text-slate-400">Inspecting document metadata and regex confidence scores</p>
              </div>
              {previewDoc && (
                <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">
                  {previewDoc.status || "PROCESSED"}
                </span>
              )}
            </div>

            {previewDoc ? (
              <div className="space-y-4 flex-1 overflow-y-auto">
                <div className="grid grid-cols-2 gap-3 text-xs bg-slate-50 p-3 rounded-xl border border-slate-200">
                  <div>
                    <span className="text-[10px] font-bold text-slate-400 uppercase">File Name</span>
                    <p className="font-semibold text-slate-900 line-clamp-1">{previewDoc.file_name || previewDoc.file_path || "Uploaded File"}</p>
                  </div>
                  <div>
                    <span className="text-[10px] font-bold text-slate-400 uppercase">Document Type</span>
                    <p className="font-semibold text-slate-900">{previewDoc.document_type || "PDF/IMAGE"}</p>
                  </div>
                </div>

                {/* Extracted Key-Value Fields */}
                <div>
                  <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                    <Tag className="h-3.5 w-3.5 text-blue-600" />
                    <span>Extracted Identity & Transaction Fields</span>
                  </h4>
                  {previewDoc.extracted_fields && Object.keys(previewDoc.extracted_fields).length > 0 ? (
                    <div className="grid grid-cols-2 gap-2">
                      {Object.entries(previewDoc.extracted_fields).map(([k, v]) => (
                        <div key={k} className="p-2.5 rounded-lg border border-slate-200 bg-white shadow-2xs">
                          <span className="text-[10px] font-bold text-slate-400 uppercase block">{k.replace(/_/g, " ")}</span>
                          <span className="text-xs font-extrabold text-slate-900">{String(v)}</span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="p-4 rounded-xl border border-slate-200 bg-slate-50 text-xs text-slate-500">
                      Standard text document detected. Key numerical fields (Consumer Account / Amount Due) extracted into OCR trace.
                    </div>
                  )}
                </div>

                {/* OCR Text Preview */}
                <div>
                  <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">OCR Text Extract Preview</h4>
                  <div className="p-3.5 rounded-xl bg-slate-900 text-slate-200 font-mono text-[11px] max-h-48 overflow-y-auto leading-relaxed border border-slate-800">
                    {previewDoc.ocr_preview || previewDoc.ocr_text || "Document text successfully processed into intelligence stream."}
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex-1 flex flex-col items-center justify-center p-8 text-center text-slate-400">
                <FileText className="h-10 w-10 text-slate-300 mb-2" />
                <p className="text-xs font-semibold">Select or upload a document to inspect OCR intelligence.</p>
              </div>
            )}
          </div>
        </div>

        {/* Processed Documents List Table */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
          <h3 className="text-sm font-bold text-slate-900 mb-4 flex items-center justify-between">
            <span>Processed Document Repository ({documents.length})</span>
            <span className="text-xs text-slate-400 font-normal">Stored securely in system SQLite database</span>
          </h3>

          {loading ? (
            <div className="p-6 text-center text-xs text-slate-500">Loading document database...</div>
          ) : documents.length === 0 ? (
            <div className="p-8 text-center text-xs text-slate-500 border border-slate-100 rounded-xl bg-slate-50">
              No documents processed yet. Upload a bill or receipt above to initiate extraction.
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="border-b border-slate-200 bg-slate-50 text-slate-500 font-bold uppercase text-[10px]">
                    <th className="p-3">File Name</th>
                    <th className="p-3">Type</th>
                    <th className="p-3">Status</th>
                    <th className="p-3">Extracted Fields</th>
                    <th className="p-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {documents.map((doc) => (
                    <tr key={doc.id} className="hover:bg-slate-50/80 transition">
                      <td className="p-3 font-bold text-slate-900 flex items-center space-x-2">
                        <FileText className="h-4 w-4 text-blue-600 shrink-0" />
                        <span className="line-clamp-1">{doc.file_name}</span>
                      </td>
                      <td className="p-3 font-semibold text-slate-600">{doc.document_type}</td>
                      <td className="p-3">
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">
                          {doc.status}
                        </span>
                      </td>
                      <td className="p-3 text-slate-600">
                        {doc.extracted_fields ? (
                          <span className="font-semibold text-blue-600">
                            {Object.keys(doc.extracted_fields).length} Fields Extracted
                          </span>
                        ) : (
                          <span className="text-slate-400">Raw Text OCR</span>
                        )}
                      </td>
                      <td className="p-3 text-right">
                        <button
                          onClick={() => setPreviewDoc(doc)}
                          className="inline-flex items-center space-x-1 rounded bg-blue-50 px-2.5 py-1 text-[11px] font-bold text-blue-700 hover:bg-blue-100 transition"
                        >
                          <Eye className="h-3.5 w-3.5" />
                          <span>Inspect</span>
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
