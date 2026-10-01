"use client";

import { useState, useEffect } from "react";
import Navbar from "@/components/layout/Navbar";
import { fetchIntegrations } from "@/lib/api";
import { Radio, Shield, CheckCircle2, AlertTriangle, XCircle, RefreshCw } from "lucide-react";

export default function IntegrationsPage() {
  const [integrations, setIntegrations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStatus();
  }, []);

  async function loadStatus() {
    setLoading(true);
    try {
      const data = await fetchIntegrations();
      setIntegrations(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <Navbar />

      <main className="flex-1 mx-auto w-full max-w-5xl p-6">
        <div className="mb-6 flex items-center justify-between">
          <div>
            <div className="flex items-center space-x-2 text-xs font-bold text-purple-600 uppercase tracking-wider">
              <Radio className="h-4 w-4" />
              <span>Real-World API & Service Status</span>
            </div>
            <h1 className="text-2xl font-extrabold text-slate-900 mt-1">Integration Health Center</h1>
            <p className="text-xs text-slate-500">
              Live status check across external public APIs, government portals, geocoders, and weather services.
            </p>
          </div>
          <button
            onClick={loadStatus}
            className="flex items-center space-x-1.5 rounded-lg border border-slate-300 bg-white px-3.5 py-2 text-xs font-bold text-slate-700 hover:bg-slate-100 transition"
          >
            <RefreshCw className={`h-3.5 w-3.5 ${loading ? "animate-spin" : ""}`} />
            <span>Check Health</span>
          </button>
        </div>

        {loading ? (
          <div className="p-8 text-center text-xs text-slate-500">Executing live health checks...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {integrations.map((ig, i) => (
              <div key={i} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-bold text-slate-900">{ig.display_name}</span>
                  <span
                    className={`flex items-center space-x-1 px-2.5 py-1 rounded text-xs font-bold ${
                      ig.status === "CONNECTED"
                        ? "bg-emerald-100 text-emerald-800"
                        : ig.status === "DEGRADED"
                        ? "bg-amber-100 text-amber-900"
                        : "bg-slate-100 text-slate-700"
                    }`}
                  >
                    {ig.status === "CONNECTED" ? (
                      <CheckCircle2 className="h-3.5 w-3.5 text-emerald-600" />
                    ) : (
                      <AlertTriangle className="h-3.5 w-3.5 text-amber-600" />
                    )}
                    <span>{ig.status}</span>
                  </span>
                </div>

                <div className="text-xs text-slate-600">
                  <span className="font-semibold text-slate-700">Capabilities:</span>{" "}
                  {ig.capabilities?.join(" • ")}
                </div>

                {ig.error_message && (
                  <p className="text-[11px] font-medium text-amber-800 bg-amber-50 p-2 rounded border border-amber-200">
                    Note: {ig.error_message}
                  </p>
                )}

                <p className="text-[10px] text-slate-400">
                  Last checked: {new Date(ig.last_health_check).toLocaleTimeString()}
                </p>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
