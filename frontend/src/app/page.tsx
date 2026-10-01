"use client";

import Link from "next/link";
import { useState } from "react";
import Navbar from "@/components/layout/Navbar";
import { ShieldCheck, ArrowRight, CheckCircle2, FileSearch, Scale, Zap, Lock, Cpu, Globe } from "lucide-react";

export default function LandingPage() {
  const [selectedScenario, setSelectedScenario] = useState(0);

  const scenarios = [
    {
      domain: "Education & Scholarships",
      title: "Scenario A: NSP Scholarship Disbursement Failure",
      prompt: "My scholarship was approved 3 months ago on the National Scholarship Portal, but the DBT payment has not reached my bank account.",
      evidence: [
        { type: "Official Search", text: "CPGRAMS NSP grievance portal Nodal Officer details retrieved" },
        { type: "Web Citation", text: "PFMS public payment status guide cited (gov.in)" },
        { type: "Document Check", text: "NSP Application ID & Student Aadhaar Name verified" }
      ],
      action: "Generate CPGRAMS Nodal Appeal Representation",
      risk: "MEDIUM (Requires Citizen Approval)"
    },
    {
      domain: "Utilities & Energy",
      title: "Scenario B: Electricity Bill Sudden Anomaly",
      prompt: "My monthly electricity bill for June jumped from ₹1,200 to ₹18,400 without any change in meter or usage.",
      evidence: [
        { type: "Deterministic Math", text: "1,433% billing unit anomaly calculated vs 6-month baseline" },
        { type: "Live Weather API", text: "Open-Meteo temperature history verified (No extreme heatwave surge)" },
        { type: "Policy Check", text: "State Electricity Regulatory Commission billing error rules cited" }
      ],
      action: "Prepare Executive Engineer Billing Dispute Application",
      risk: "MEDIUM (Requires Citizen Approval)"
    },
    {
      domain: "Logistics & Public Service",
      title: "Scenario C: Postal Delivery Exception",
      prompt: "Speed Post parcel containing original birth certificate shows 'Delivery Attempted - Recipient Absent' when I was present at home.",
      evidence: [
        { type: "OSM Geocoding", text: "Head Post Office pincode & delivery hub geocoded" },
        { type: "Tracking Inspection", text: "Postal tracking timestamp mismatch flagged" }
      ],
      action: "Dispatch Urgent Postal Superintendent Complaint",
      risk: "MEDIUM (Requires Citizen Approval)"
    }
  ];

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans">
      <Navbar />

      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-orange-50/60 via-white to-slate-50 pt-16 pb-20 border-b border-slate-200">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center space-x-2 rounded-full border border-orange-200 bg-orange-50 px-3.5 py-1.5 text-xs font-semibold text-orange-800 shadow-xs mb-6">
            <span className="flex h-2 w-2 rounded-full bg-orange-600 animate-ping"></span>
            <span>PRODUCTION AGENTIC CASE RESOLUTION ENGINE FOR INDIA</span>
          </div>

          <h1 className="text-4xl font-extrabold tracking-tight text-slate-900 sm:text-6xl max-w-4xl mx-auto leading-tight">
            Don't search for the right portal. <br />
            <span className="text-orange-600">Tell BharatResolve the problem.</span>
          </h1>

          <p className="mt-6 text-lg leading-8 text-slate-600 max-w-2xl mx-auto">
            An agentic AI case-resolution platform that autonomously investigates real-world problems, gathers official evidence, checks policy rules, plans actions, and verifies outcomes.
          </p>

          <div className="mt-8 flex items-center justify-center space-x-4">
            <Link
              href="/app/new"
              className="flex items-center space-x-2 rounded-xl bg-orange-600 px-6 py-3.5 text-base font-bold text-white shadow-lg shadow-orange-600/25 hover:bg-orange-700 transition"
            >
              <span>Resolve a Problem</span>
              <ArrowRight className="h-5 w-5" />
            </Link>
            <Link
              href="/app"
              className="rounded-xl border border-slate-300 bg-white px-6 py-3.5 text-base font-semibold text-slate-700 shadow-xs hover:bg-slate-50 hover:text-slate-900 transition"
            >
              Open Command Center
            </Link>
          </div>

          <div className="mt-12 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto text-left">
            <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-xs">
              <span className="text-xs font-bold text-slate-400 uppercase">Architecture</span>
              <p className="text-sm font-bold text-slate-800 mt-1">StateGraph Orchestrated</p>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-xs">
              <span className="text-xs font-bold text-slate-400 uppercase">Integrations</span>
              <p className="text-sm font-bold text-slate-800 mt-1">Real APIs & Public Web</p>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-xs">
              <span className="text-xs font-bold text-slate-400 uppercase">Human Policy Gate</span>
              <p className="text-sm font-bold text-slate-800 mt-1">Stateful Approval Interruption</p>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-xs">
              <span className="text-xs font-bold text-slate-400 uppercase">Verification</span>
              <p className="text-sm font-bold text-slate-800 mt-1">Deterministic Code Rules</p>
            </div>
          </div>
        </div>
      </section>

      {/* Interactive Scenario Explorer */}
      <section className="py-16 bg-white border-b border-slate-200">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-10">
            <h2 className="text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl">
              Live Agent Execution Walkthrough
            </h2>
            <p className="text-sm text-slate-600 mt-2">
              Select a scenario to see how BharatResolve AI perceives, investigates, and resolves real Indian citizen pain points.
            </p>
          </div>

          <div className="flex flex-wrap justify-center gap-3 mb-8">
            {scenarios.map((sc, idx) => (
              <button
                key={idx}
                onClick={() => setSelectedScenario(idx)}
                className={`px-5 py-2.5 rounded-lg text-sm font-semibold transition ${
                  selectedScenario === idx
                    ? "bg-orange-600 text-white shadow-md"
                    : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                }`}
              >
                {sc.domain}
              </button>
            ))}
          </div>

          <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 md:p-8 shadow-sm">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <span className="text-xs font-bold text-orange-600 uppercase tracking-wider">Citizen Problem Input</span>
                <h3 className="text-lg font-bold text-slate-900 mt-1">{scenarios[selectedScenario].title}</h3>
                <div className="mt-3 rounded-lg border border-slate-200 bg-white p-4 text-sm text-slate-800 italic">
                  "{scenarios[selectedScenario].prompt}"
                </div>

                <div className="mt-6">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Gathered Real Evidence</span>
                  <div className="mt-2 space-y-2">
                    {scenarios[selectedScenario].evidence.map((ev, i) => (
                      <div key={i} className="flex items-start space-x-2.5 rounded-md border border-slate-200 bg-white p-3 text-xs">
                        <CheckCircle2 className="h-4 w-4 text-emerald-600 mt-0.5 shrink-0" />
                        <div>
                          <span className="font-bold text-slate-900">[{ev.type}]</span>{" "}
                          <span className="text-slate-700">{ev.text}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="flex flex-col justify-between border-t md:border-t-0 md:border-l border-slate-200 pt-6 md:pt-0 md:pl-8">
                <div>
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Generated Resolution Action</span>
                  <div className="mt-2 rounded-xl border border-orange-200 bg-orange-50/60 p-4">
                    <p className="text-sm font-bold text-orange-950">{scenarios[selectedScenario].action}</p>
                    <p className="text-xs text-orange-700 mt-1 font-medium">Risk Status: {scenarios[selectedScenario].risk}</p>
                  </div>

                  <div className="mt-6">
                    <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Agent Execution Loop</span>
                    <div className="mt-2 space-y-2 text-xs text-slate-600">
                      <div className="flex items-center justify-between p-2 rounded bg-white border border-slate-200">
                        <span>1. Intent & Domain Classification</span>
                        <span className="font-semibold text-emerald-600">Completed</span>
                      </div>
                      <div className="flex items-center justify-between p-2 rounded bg-white border border-slate-200">
                        <span>2. Real API / Public Web Investigation</span>
                        <span className="font-semibold text-emerald-600">Completed</span>
                      </div>
                      <div className="flex items-center justify-between p-2 rounded bg-white border border-slate-200">
                        <span>3. Human Approval Gate</span>
                        <span className="font-semibold text-orange-600">State Interrupt</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="mt-6">
                  <Link
                    href={`/app/new?prompt=${encodeURIComponent(scenarios[selectedScenario].prompt)}`}
                    className="w-full flex items-center justify-center space-x-2 rounded-lg bg-slate-900 px-4 py-3 text-sm font-bold text-white hover:bg-slate-800 transition"
                  >
                    <span>Run This Case Live</span>
                    <ArrowRight className="h-4 w-4" />
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto border-t border-slate-200 bg-white py-8 text-center text-xs text-slate-500">
        <p>BharatResolve AI - Enterprise Agentic AI Case-Resolution Engine for India. Built with Google Antigravity & LangGraph.</p>
      </footer>
    </div>
  );
}
