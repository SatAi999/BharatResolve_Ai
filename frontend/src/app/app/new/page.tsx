"use client";

import { useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import { createCase, checkCounterfactual, uploadDocument } from "@/lib/api";
import { Shield, Upload, Send, AlertTriangle, CheckCircle2, ArrowRight } from "lucide-react";

function NewCaseForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const initialPrompt = searchParams.get("prompt") || "";

  const [problemText, setProblemText] = useState(initialPrompt);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [precheckResult, setPrecheckResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function handleRunPrecheck() {
    if (!problemText.trim()) return;
    setLoading(true);
    try {
      const res = await checkCounterfactual(problemText, {}, selectedFile ? 1 : 0);
      setPrecheckResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmitCase(e: React.FormEvent) {
    e.preventDefault();
    if (!problemText.trim()) return;

    setLoading(true);
    try {
      const newCase = await createCase(problemText.trim());
      if (selectedFile && newCase.id) {
        await uploadDocument(newCase.id, selectedFile);
      }
      router.push("/app");
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmitCase} className="space-y-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div>
          <label className="block text-xs font-bold text-slate-700 uppercase mb-2">
            Problem Description (English, Hindi, Hinglish)
          </label>
          <textarea
            rows={5}
            value={problemText}
            onChange={(e) => setProblemText(e.target.value)}
            placeholder="Describe what happened e.g. 'My scholarship was approved on NSP but DBT payment has not reached my bank account...'"
            className="w-full rounded-xl border border-slate-300 p-4 text-sm text-slate-900 placeholder:text-slate-400 outline-none focus:border-orange-500"
          />
        </div>

        <div>
          <label className="block text-xs font-bold text-slate-700 uppercase mb-2">
            Attach Supporting Document (PDF / Bill / Receipt / Certificate)
          </label>
          <input
            type="file"
            onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
            className="block w-full text-xs text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-orange-50 file:text-orange-700 hover:file:bg-orange-100"
          />
        </div>

        <div className="flex items-center space-x-3 pt-2">
          <button
            type="button"
            onClick={handleRunPrecheck}
            disabled={loading || !problemText.trim()}
            className="rounded-xl border border-slate-300 bg-white px-5 py-3 text-xs font-bold text-slate-700 hover:bg-slate-50 transition disabled:opacity-50"
          >
            Check Before Submit
          </button>
          <button
            type="submit"
            disabled={loading || !problemText.trim()}
            className="flex-1 flex items-center justify-center space-x-2 rounded-xl bg-orange-600 px-6 py-3 text-xs font-bold text-white hover:bg-orange-700 transition disabled:opacity-50"
          >
            <span>Launch Agentic Investigation</span>
            <ArrowRight className="h-4 w-4" />
          </button>
        </div>
      </form>

      {/* Counterfactual Precheck Output Card */}
      {precheckResult && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
            <span className="text-xs font-bold text-slate-900 flex items-center space-x-2">
              <AlertTriangle className="h-4 w-4 text-amber-500" />
              <span>Counterfactual Prevention Check Result</span>
            </span>
            <span className={`px-2.5 py-1 rounded text-xs font-bold ${precheckResult.status === "READY" ? "bg-emerald-100 text-emerald-800" : "bg-amber-100 text-amber-900"}`}>
              Status: {precheckResult.status}
            </span>
          </div>

          {precheckResult.recommendations.length > 0 && (
            <div className="space-y-2">
              <h4 className="text-xs font-bold text-slate-700 uppercase">Recommendations to prevent rejection:</h4>
              {precheckResult.recommendations.map((rec: string, i: number) => (
                <div key={i} className="flex items-start space-x-2 text-xs text-slate-700 bg-amber-50/50 p-2.5 rounded-lg border border-amber-200">
                  <CheckCircle2 className="h-4 w-4 text-amber-600 mt-0.5 shrink-0" />
                  <span>{rec}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default function NewCasePage() {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <Navbar />

      <main className="flex-1 mx-auto w-full max-w-4xl p-6">
        <div className="mb-6">
          <div className="flex items-center space-x-2 text-xs font-bold text-orange-600 uppercase tracking-wider">
            <Shield className="h-4 w-4" />
            <span>New Case Intake & Counterfactual Prevention</span>
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900 mt-1">Submit Your Problem</h1>
          <p className="text-xs text-slate-500">
            Tell BharatResolve your issue in plain language. Use "Check Before Submit" to detect missing fields and rejection risks.
          </p>
        </div>

        <Suspense fallback={<div className="p-8 text-center text-xs text-slate-500">Loading intake form...</div>}>
          <NewCaseForm />
        </Suspense>
      </main>
    </div>
  );
}
