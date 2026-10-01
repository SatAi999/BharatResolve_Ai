"use client";

import { CaseResponse } from "@/lib/api";
import { CheckCircle, AlertTriangle, FileText, Search, Shield, Play } from "lucide-react";

interface CaseGraphProps {
  caseData: CaseResponse;
}

export default function CaseGraph({ caseData }: CaseGraphProps) {
  const nodes = [
    { id: "problem", label: "Citizen Problem", type: "input", status: "DONE", details: caseData.raw_input.slice(0, 40) + "..." },
    { id: "intent", label: `Domain: ${caseData.domain}`, type: "intent", status: "DONE", details: caseData.intent },
    { id: "documents", label: "Document Intelligence", type: "document", status: caseData.entities.length > 0 ? "DONE" : "PENDING", details: `${caseData.entities.length} fields extracted` },
    { id: "evidence", label: "Evidence Engine", type: "evidence", status: caseData.evidence_items.length > 0 ? "DONE" : "PENDING", details: `${caseData.evidence_items.length} citations verified` },
    { id: "action", label: "Permitted Action", type: "action", status: caseData.actions.length > 0 ? "DONE" : "WAITING", details: caseData.actions[0]?.action_name || "Action Prepared" },
    { id: "verification", label: "Verification Gate", type: "verification", status: caseData.resolution_score > 0.5 ? "DONE" : "PENDING", details: `Score: ${caseData.resolution_score}` },
    { id: "outcome", label: `Result: ${caseData.status}`, type: "outcome", status: caseData.status === "RESOLVED" ? "DONE" : "IN_PROGRESS", details: caseData.summary || "Agent State active" }
  ];

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-4 flex items-center justify-between border-b border-slate-100 pb-3">
        <div>
          <h3 className="text-sm font-bold text-slate-900 flex items-center space-x-2">
            <Shield className="h-4 w-4 text-orange-600" />
            <span>Interactive Case State Graph</span>
          </h3>
          <p className="text-xs text-slate-500">Live node dependencies from problem intake to verified evidence</p>
        </div>
        <span className="rounded-full bg-slate-100 px-2.5 py-1 text-[11px] font-semibold text-slate-700">
          7 Execution Nodes
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-7 gap-2 relative">
        {nodes.map((node, index) => (
          <div key={node.id} className="relative flex flex-col items-center">
            <div
              className={`w-full flex flex-col items-center justify-center p-3 rounded-lg border text-center transition ${
                node.status === "DONE"
                  ? "bg-emerald-50/70 border-emerald-300 text-emerald-950"
                  : node.status === "IN_PROGRESS"
                  ? "bg-amber-50 border-amber-300 text-amber-950 animate-pulse"
                  : "bg-slate-50 border-slate-200 text-slate-600"
              }`}
            >
              <div className="mb-1.5 flex h-7 w-7 items-center justify-center rounded-full bg-white shadow-xs border border-slate-200">
                {node.status === "DONE" ? (
                  <CheckCircle className="h-4 w-4 text-emerald-600" />
                ) : (
                  <Play className="h-3.5 w-3.5 text-orange-600" />
                )}
              </div>
              <span className="text-xs font-semibold leading-tight">{node.label}</span>
              <span className="mt-1 text-[10px] text-slate-500 line-clamp-1">{node.details}</span>
            </div>
            {index < nodes.length - 1 && (
              <div className="hidden md:block absolute -right-2.5 top-1/2 -translate-y-1/2 z-10">
                <span className="text-slate-300 font-bold text-xs">→</span>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
