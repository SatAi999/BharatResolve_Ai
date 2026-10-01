"use client";

import { useState, useEffect } from "react";
import Navbar from "@/components/layout/Navbar";
import { fetchSystemInsights } from "@/lib/api";
import { BarChart2, Shield, CheckCircle2, AlertCircle } from "lucide-react";

export default function InsightsPage() {
  const [insights, setInsights] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSystemInsights().then(setInsights).catch(console.error).finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <Navbar />

      <main className="flex-1 mx-auto w-full max-w-5xl p-6">
        <div className="mb-6">
          <div className="flex items-center space-x-2 text-xs font-bold text-emerald-600 uppercase tracking-wider">
            <BarChart2 className="h-4 w-4" />
            <span>System Analytics & Friction Insights</span>
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900 mt-1">System Painpoint Insights</h1>
          <p className="text-xs text-slate-500">
            Real aggregate metrics calculated strictly over stored database cases. Zero fabricated data.
          </p>
        </div>

        {loading ? (
          <div className="p-8 text-center text-xs text-slate-500">Loading metrics...</div>
        ) : insights && insights.total_cases > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
              <span className="text-xs font-bold text-slate-400 uppercase">Total Active Cases</span>
              <div className="text-3xl font-extrabold text-slate-900 mt-1">{insights.total_cases}</div>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
              <span className="text-xs font-bold text-slate-400 uppercase">Average Resolution Score</span>
              <div className="text-3xl font-extrabold text-emerald-600 mt-1">{insights.avg_resolution_score}</div>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
              <span className="text-xs font-bold text-slate-400 uppercase">Tool Execution Success Rate</span>
              <div className="text-3xl font-extrabold text-blue-600 mt-1">{Math.round(insights.tool_success_rate * 100)}%</div>
            </div>
          </div>
        ) : (
          <div className="rounded-2xl border border-slate-200 bg-white p-12 text-center shadow-xs">
            <AlertCircle className="h-10 w-10 text-slate-300 mx-auto mb-2" />
            <h3 className="text-sm font-bold text-slate-900">Insufficient Data</h3>
            <p className="text-xs text-slate-500 mt-1">Create your first case in the workspace to view live analytics.</p>
          </div>
        )}
      </main>
    </div>
  );
}
