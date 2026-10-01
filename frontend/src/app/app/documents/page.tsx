"use client";

import Navbar from "@/components/layout/Navbar";
import { FileText, Shield, Upload, CheckCircle2, AlertTriangle } from "lucide-react";

export default function DocumentsPage() {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <Navbar />

      <main className="flex-1 mx-auto w-full max-w-5xl p-6">
        <div className="mb-6">
          <div className="flex items-center space-x-2 text-xs font-bold text-blue-600 uppercase tracking-wider">
            <FileText className="h-4 w-4" />
            <span>Document Intelligence & Field Extraction</span>
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900 mt-1">Document Intelligence Center</h1>
          <p className="text-xs text-slate-500">
            PyMuPDF OCR & regex field extraction pipeline. Automatically detects identity conflicts and application numbers.
          </p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center shadow-xs">
          <Upload className="h-12 w-12 text-slate-300 mx-auto mb-3" />
          <h3 className="text-sm font-bold text-slate-900">Upload PDF or Image Document</h3>
          <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
            Upload bills, certificates, or acknowledgement receipts to extract structured fields and cross-check across case records.
          </p>
        </div>
      </main>
    </div>
  );
}
