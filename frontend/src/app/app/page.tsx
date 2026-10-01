"use client";

import { useState, useEffect } from "react";
import Navbar from "@/components/layout/Navbar";
import CaseGraph from "@/components/graph/CaseGraph";
import { fetchCases, fetchCaseById, createCase, decideApproval, uploadDocument, deleteCase, CaseResponse } from "@/lib/api";
import {
  Shield, Plus, Send, Upload, CheckCircle2, AlertTriangle, FileText, Search, Clock, ChevronRight, User, Bot, AlertCircle, RefreshCw, Trash2
} from "lucide-react";

export default function WorkspacePage() {
  const [cases, setCases] = useState<CaseResponse[]>([]);
  const [activeCase, setActiveCase] = useState<CaseResponse | null>(null);
  const [inputProblem, setInputProblem] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [filterDomain, setFilterDomain] = useState<string>("");
  const [activeTab, setActiveTab] = useState<"intelligence" | "graph" | "approvals">("intelligence");

  useEffect(() => {
    loadCases();
  }, [filterDomain]);

  async function loadCases() {
    try {
      const data = await fetchCases(filterDomain || undefined);
      setCases(data);
      if (data.length > 0) {
        if (!activeCase) {
          setActiveCase(data[0]);
        } else {
          const matching = data.find(c => c.id === activeCase.id);
          if (matching) {
            setActiveCase(matching);
          } else {
            setActiveCase(data[0]);
          }
        }
      } else {
        setActiveCase(null);
      }
    } catch (err) {
      console.error("Failed to load cases", err);
    }
  }

  async function handleCreateCase(e: React.FormEvent) {
    e.preventDefault();
    if (!inputProblem.trim()) return;

    setLoading(true);
    try {
      const newCase = await createCase(inputProblem.trim());
      
      if (selectedFile && newCase.id) {
        await uploadDocument(newCase.id, selectedFile);
      }

      setInputProblem("");
      setSelectedFile(null);
      
      // Fetch fresh created case state & select it
      const freshCase = await fetchCaseById(newCase.id);
      setActiveCase(freshCase);
      await loadCases();
    } catch (err) {
      console.error("Failed to create case", err);
    } finally {
      setLoading(false);
    }
  }

  async function handleDeleteCase(caseId: string, e: React.MouseEvent) {
    e.stopPropagation();
    if (!confirm("Are you sure you want to delete this case?")) return;
    try {
      await deleteCase(caseId);
      if (activeCase?.id === caseId) {
        setActiveCase(null);
      }
      await loadCases();
    } catch (err) {
      console.error("Failed to delete case", err);
    }
  }

  async function handleApproval(approvalId: string, decision: "APPROVED" | "REJECTED") {
    try {
      await decideApproval(approvalId, decision);
      await loadCases();
      if (activeCase) {
        const fresh = await fetchCaseById(activeCase.id);
        setActiveCase(fresh);
      }
    } catch (err) {
      console.error("Failed to submit approval", err);
    }
  }

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col font-sans">
      <Navbar />

      <main className="flex-1 mx-auto w-full max-w-[1700px] p-4 gap-4 grid grid-cols-1 lg:grid-cols-12 overflow-hidden">
        {/* LEFT COLUMN: Cases List & Filters */}
        <div className="lg:col-span-3 flex flex-col rounded-xl border border-slate-200 bg-white shadow-xs overflow-hidden h-[calc(100vh-5rem)]">
          <div className="p-4 border-b border-slate-200 bg-slate-50/70 flex items-center justify-between">
            <div>
              <h2 className="text-sm font-bold text-slate-900 flex items-center space-x-1.5">
                <Shield className="h-4 w-4 text-orange-600" />
                <span>Active Cases</span>
              </h2>
              <p className="text-[11px] text-slate-500">{cases.length} cases tracked</p>
            </div>
            <button
              onClick={loadCases}
              className="p-1.5 text-slate-500 hover:text-slate-900 hover:bg-slate-200 rounded-md transition"
              title="Refresh Cases List"
            >
              <RefreshCw className="h-4 w-4" />
            </button>
          </div>

          <div className="p-2 border-b border-slate-200">
            <select
              value={filterDomain}
              onChange={(e) => setFilterDomain(e.target.value)}
              className="w-full rounded-lg border border-slate-200 bg-slate-50 p-2 text-xs font-semibold text-slate-700 outline-none focus:border-orange-500"
            >
              <option value="">All Problem Domains</option>
              <option value="Education">Education & Scholarships</option>
              <option value="Utilities">Utilities & Electricity</option>
              <option value="Citizen/GovTech">Citizen / GovTech</option>
              <option value="Agriculture">Agriculture</option>
              <option value="Financial Services">Financial Services</option>
            </select>
          </div>

          <div className="flex-1 overflow-y-auto divide-y divide-slate-100">
            {cases.length === 0 ? (
              <div className="p-6 text-center text-xs text-slate-500">
                No active cases found. Submit a problem below to get started.
              </div>
            ) : (
              cases.map((c) => (
                <div
                  key={c.id}
                  onClick={() => setActiveCase(c)}
                  className={`p-3 cursor-pointer transition flex items-center justify-between group ${
                    activeCase?.id === c.id ? "bg-orange-50/80 border-l-4 border-orange-600" : "hover:bg-slate-50"
                  }`}
                >
                  <div className="flex-1 pr-2">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">{c.domain}</span>
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          c.status === "RESOLVED"
                            ? "bg-emerald-100 text-emerald-800"
                            : c.status === "PENDING_APPROVAL"
                            ? "bg-amber-100 text-amber-900"
                            : "bg-blue-100 text-blue-800"
                        }`}
                      >
                        {c.status}
                      </span>
                    </div>
                    <h3 className="text-xs font-bold text-slate-900 mt-1 line-clamp-1">{c.title}</h3>
                    <div className="mt-2 flex items-center justify-between text-[11px] text-slate-500">
                      <span>Score: {c.resolution_score}</span>
                      <span>{new Date(c.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                    </div>
                  </div>

                  {/* Delete Action Button */}
                  <button
                    onClick={(e) => handleDeleteCase(c.id, e)}
                    className="p-1 text-slate-300 hover:text-red-600 hover:bg-red-50 rounded transition opacity-0 group-hover:opacity-100 shrink-0"
                    title="Delete Case"
                  >
                    <Trash2 className="h-3.5 w-3.5" />
                  </button>
                </div>
              ))
            )}
          </div>
        </div>

        {/* CENTER COLUMN: Case Conversation & Intake Panel */}
        <div className="lg:col-span-5 flex flex-col rounded-xl border border-slate-200 bg-white shadow-xs overflow-hidden h-[calc(100vh-5rem)]">
          <div className="p-4 border-b border-slate-200 bg-slate-50/70 flex items-center justify-between">
            <div>
              <h2 className="text-sm font-bold text-slate-900">
                {activeCase ? activeCase.title : "Case Conversation"}
              </h2>
              <span className="text-[11px] text-slate-500">
                {activeCase ? `Domain: ${activeCase.domain} • Risk: ${activeCase.risk_level}` : "Submit new problem"}
              </span>
            </div>
            {activeCase?.status === "PENDING_APPROVAL" && (
              <span className="flex items-center space-x-1 rounded bg-amber-100 px-2 py-1 text-xs font-bold text-amber-900 animate-pulse">
                <AlertCircle className="h-3.5 w-3.5" />
                <span>Approval Required</span>
              </span>
            )}
          </div>

          <div className="flex-1 p-4 overflow-y-auto space-y-4">
            {activeCase ? (
              <>
                <div className="flex items-start space-x-3">
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-slate-200 text-slate-700 font-bold text-xs shrink-0">
                    <User className="h-4 w-4" />
                  </div>
                  <div className="rounded-2xl rounded-tl-none bg-slate-100 p-3.5 text-xs text-slate-800 max-w-[85%]">
                    <p className="font-semibold text-slate-900 mb-1">Citizen Problem Statement:</p>
                    {activeCase.raw_input}
                  </div>
                </div>

                {activeCase.summary && (
                  <div className="flex items-start space-x-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-orange-600 text-white font-bold text-xs shrink-0">
                      <Bot className="h-4 w-4" />
                    </div>
                    <div className="rounded-2xl rounded-tl-none bg-orange-50/80 border border-orange-200 p-3.5 text-xs text-slate-800 max-w-[85%]">
                      <p className="font-bold text-orange-950 mb-1">Agent Commander Summary:</p>
                      {activeCase.summary}
                    </div>
                  </div>
                )}

                {/* Audit Event Activity Trace */}
                <div className="mt-4 border-t border-slate-100 pt-3">
                  <h4 className="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">Live Agent Operational Events</h4>
                  <div className="space-y-1.5 max-h-48 overflow-y-auto pr-1">
                    {activeCase.audit_events.map((ev, i) => (
                      <div key={i} className="flex items-center justify-between text-[11px] p-2 rounded bg-slate-50 border border-slate-100">
                        <span className="font-semibold text-slate-700 flex items-center space-x-1.5">
                          <CheckCircle2 className="h-3.5 w-3.5 text-emerald-600" />
                          <span>{ev.event_type}</span>
                        </span>
                        <span className="text-slate-400 text-[10px]">
                          {ev.created_at ? new Date(ev.created_at).toLocaleTimeString() : ""}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            ) : (
              <div className="p-8 text-center text-slate-500">
                <Shield className="h-10 w-10 text-slate-300 mx-auto mb-2" />
                <p className="text-sm font-semibold">Select a case or submit a new problem below.</p>
              </div>
            )}
          </div>

          {/* New Case / Response Intake Form */}
          <form onSubmit={handleCreateCase} className="p-3 border-t border-slate-200 bg-slate-50">
            <div className="flex items-center space-x-2">
              <input
                type="text"
                value={inputProblem}
                onChange={(e) => setInputProblem(e.target.value)}
                placeholder="Tell BharatResolve your problem (English, Hindi, Hinglish)..."
                className="flex-1 rounded-lg border border-slate-300 bg-white px-3.5 py-2.5 text-xs text-slate-900 placeholder:text-slate-400 outline-none focus:border-orange-500"
              />
              <label className="cursor-pointer p-2.5 rounded-lg border border-slate-300 bg-white text-slate-600 hover:bg-slate-100 transition" title="Attach Document">
                <Upload className="h-4 w-4" />
                <input
                  type="file"
                  onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
                  className="hidden"
                />
              </label>
              <button
                type="submit"
                disabled={loading}
                className="flex items-center space-x-1.5 rounded-lg bg-orange-600 px-4 py-2.5 text-xs font-bold text-white hover:bg-orange-700 transition disabled:opacity-50 cursor-pointer"
              >
                {loading ? <RefreshCw className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                <span>Investigate</span>
              </button>
            </div>
            {selectedFile && (
              <div className="mt-2 text-[11px] font-semibold text-blue-600 flex items-center space-x-1">
                <FileText className="h-3.5 w-3.5" />
                <span>Attached: {selectedFile.name}</span>
              </div>
            )}
          </form>
        </div>

        {/* RIGHT COLUMN: Case Intelligence Panel */}
        <div className="lg:col-span-4 flex flex-col rounded-xl border border-slate-200 bg-white shadow-xs overflow-hidden h-[calc(100vh-5rem)]">
          <div className="p-2 border-b border-slate-200 bg-slate-50 flex items-center space-x-2 text-xs font-bold text-slate-700">
            <button
              onClick={() => setActiveTab("intelligence")}
              className={`px-3 py-1.5 rounded-md transition cursor-pointer ${activeTab === "intelligence" ? "bg-white text-orange-600 shadow-xs" : "hover:bg-slate-200"}`}
            >
              Intelligence
            </button>
            <button
              onClick={() => setActiveTab("graph")}
              className={`px-3 py-1.5 rounded-md transition cursor-pointer ${activeTab === "graph" ? "bg-white text-orange-600 shadow-xs" : "hover:bg-slate-200"}`}
            >
              State Graph
            </button>
            <button
              onClick={() => setActiveTab("approvals")}
              className={`px-3 py-1.5 rounded-md transition cursor-pointer ${activeTab === "approvals" ? "bg-white text-orange-600 shadow-xs" : "hover:bg-slate-200"}`}
            >
              Approvals ({activeCase?.approvals.filter(a => a.status === "PENDING").length || 0})
            </button>
          </div>

          <div className="flex-1 p-4 overflow-y-auto space-y-4">
            {activeCase ? (
              activeTab === "graph" ? (
                <CaseGraph caseData={activeCase} />
              ) : activeTab === "approvals" ? (
                <div className="space-y-3">
                  <h3 className="text-xs font-bold text-slate-900">Pending Human Approvals</h3>
                  {activeCase.approvals.filter(a => a.status === "PENDING").length === 0 ? (
                    <p className="text-xs text-slate-500">No pending approvals for this case.</p>
                  ) : (
                    activeCase.approvals.filter(a => a.status === "PENDING").map((ap) => (
                      <div key={ap.id} className="rounded-xl border border-amber-200 bg-amber-50/70 p-4 space-y-3">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-bold text-amber-950">{ap.title}</span>
                          <span className="rounded bg-amber-200 px-2 py-0.5 text-[10px] font-bold text-amber-900">{ap.risk_level} RISK</span>
                        </div>
                        <p className="text-xs text-amber-900">{ap.reason}</p>
                        <div className="flex items-center space-x-2 pt-2">
                          <button
                            onClick={() => handleApproval(ap.id, "APPROVED")}
                            className="flex-1 rounded-lg bg-emerald-600 px-3 py-2 text-xs font-bold text-white hover:bg-emerald-700 transition cursor-pointer"
                          >
                            Approve Action
                          </button>
                          <button
                            onClick={() => handleApproval(ap.id, "REJECTED")}
                            className="flex-1 rounded-lg border border-slate-300 bg-white px-3 py-2 text-xs font-bold text-slate-700 hover:bg-slate-100 transition cursor-pointer"
                          >
                            Reject
                          </button>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              ) : (
                /* Intelligence Tab */
                <>
                  {/* Case Score Overview */}
                  <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 flex items-center justify-between">
                    <div>
                      <span className="text-[10px] font-bold text-slate-400 uppercase">Case Resolution Score</span>
                      <div className="text-2xl font-extrabold text-slate-900 mt-0.5">{activeCase.resolution_score} <span className="text-xs text-slate-400 font-normal">/ 1.0</span></div>
                    </div>
                    <div className="text-right">
                      <span className="text-[10px] font-bold text-slate-400 uppercase">Confidence</span>
                      <div className="text-sm font-bold text-emerald-600 mt-0.5">{Math.round(activeCase.confidence_score * 100)}%</div>
                    </div>
                  </div>

                  {/* Gathered Evidence List */}
                  <div>
                    <h3 className="text-xs font-bold text-slate-900 mb-2 flex items-center justify-between">
                      <span>Verified Evidence ({activeCase.evidence_items.length})</span>
                      <span className="text-[10px] text-slate-400">No Evidence = No Claim</span>
                    </h3>
                    <div className="space-y-2">
                      {activeCase.evidence_items.map((ev, i) => (
                        <div key={i} className="rounded-lg border border-slate-200 bg-white p-3 text-xs shadow-xs">
                          <div className="flex items-center justify-between font-bold text-slate-900">
                            <span className="line-clamp-1">{ev.source_title}</span>
                            <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800">{ev.status}</span>
                          </div>
                          <p className="text-slate-600 mt-1 line-clamp-2">{ev.claim_supported}</p>
                          {ev.source_url && (
                            <a href={ev.source_url} target="_blank" rel="noreferrer" className="text-[10px] font-semibold text-orange-600 hover:underline mt-1 block">
                              Source Link ↗
                            </a>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Resolution Plan Steps */}
                  <div>
                    <h3 className="text-xs font-bold text-slate-900 mb-2">Resolution Plan Steps</h3>
                    <div className="space-y-1.5">
                      {activeCase.plans[0]?.steps.map((st) => (
                        <div key={st.step_number} className="flex items-center justify-between p-2.5 rounded-lg border border-slate-200 bg-white text-xs">
                          <div className="flex items-center space-x-2">
                            <span className="flex h-5 w-5 items-center justify-center rounded-full bg-slate-100 text-[10px] font-bold text-slate-700">
                              {st.step_number}
                            </span>
                            <span className="font-semibold text-slate-800">{st.title}</span>
                          </div>
                          <span className={`text-[10px] font-bold ${st.status === "COMPLETED" ? "text-emerald-600" : "text-amber-600"}`}>
                            {st.status}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </>
              )
            ) : (
              <div className="p-8 text-center text-xs text-slate-400">Select a case to view intelligence data.</div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
