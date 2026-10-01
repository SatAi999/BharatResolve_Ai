"use client";

import { useState, useEffect } from "react";
import Navbar from "@/components/layout/Navbar";
import { fetchPendingApprovals, decideApproval } from "@/lib/api";
import { CheckSquare, Shield, AlertTriangle, CheckCircle2, XCircle } from "lucide-react";

export default function ApprovalsPage() {
  const [approvals, setApprovals] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadApprovals();
  }, []);

  async function loadApprovals() {
    try {
      const data = await fetchPendingApprovals();
      setApprovals(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleDecide(id: string, decision: "APPROVED" | "REJECTED") {
    try {
      await decideApproval(id, decision);
      await loadApprovals();
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <Navbar />

      <main className="flex-1 mx-auto w-full max-w-5xl p-6">
        <div className="mb-6">
          <div className="flex items-center space-x-2 text-xs font-bold text-orange-600 uppercase tracking-wider">
            <CheckSquare className="h-4 w-4" />
            <span>Human-In-The-Loop Action Authorization</span>
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900 mt-1">Pending Action Approvals</h1>
          <p className="text-xs text-slate-500">
            Review and authorize agent actions requiring explicit permission before execution.
          </p>
        </div>

        {loading ? (
          <div className="p-8 text-center text-xs text-slate-500">Loading approvals...</div>
        ) : approvals.length === 0 ? (
          <div className="rounded-2xl border border-slate-200 bg-white p-12 text-center shadow-xs">
            <CheckCircle2 className="h-12 w-12 text-emerald-500 mx-auto mb-3" />
            <h3 className="text-sm font-bold text-slate-900">No Pending Approvals</h3>
            <p className="text-xs text-slate-500 mt-1">All agent actions have been authorized or auto-executed.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {approvals.map((ap) => (
              <div key={ap.id} className="rounded-2xl border border-amber-200 bg-amber-50/60 p-6 shadow-xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-bold text-slate-900">{ap.title}</span>
                    <span className="rounded bg-amber-200 px-2 py-0.5 text-[10px] font-bold text-amber-900">{ap.risk_level} RISK</span>
                  </div>
                  <p className="text-xs text-slate-700 mt-1">{ap.reason}</p>
                  <p className="text-[10px] text-slate-400 mt-2">Case ID: {ap.case_id}</p>
                </div>
                <div className="flex items-center space-x-2 shrink-0">
                  <button
                    onClick={() => handleDecide(ap.id, "APPROVED")}
                    className="flex items-center space-x-1 rounded-xl bg-emerald-600 px-4 py-2.5 text-xs font-bold text-white hover:bg-emerald-700 transition"
                  >
                    <CheckCircle2 className="h-4 w-4" />
                    <span>Approve</span>
                  </button>
                  <button
                    onClick={() => handleDecide(ap.id, "REJECTED")}
                    className="flex items-center space-x-1 rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-xs font-bold text-slate-700 hover:bg-slate-100 transition"
                  >
                    <XCircle className="h-4 w-4 text-slate-500" />
                    <span>Reject</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
