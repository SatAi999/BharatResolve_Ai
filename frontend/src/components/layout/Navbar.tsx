"use client";

import Link from "next/link";
import { ShieldCheck, Plus, CheckSquare, Activity, BarChart2, Radio, FileText, Settings } from "lucide-react";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-200 bg-white/95 backdrop-blur shadow-sm">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center space-x-6">
          <Link href="/" className="flex items-center space-x-3 group">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-orange-600 text-white shadow-md shadow-orange-600/20 group-hover:bg-orange-700 transition">
              <ShieldCheck className="h-6 w-6" />
            </div>
            <div>
              <div className="flex items-center space-x-1.5">
                <span className="text-xl font-bold tracking-tight text-slate-900">BHARATRESOLVE</span>
                <span className="rounded bg-orange-100 px-1.5 py-0.5 text-xs font-semibold text-orange-700">AI</span>
              </div>
              <p className="text-[10px] font-medium text-slate-500 uppercase tracking-wider">Agentic Case Resolution Engine</p>
            </div>
          </Link>

          <nav className="hidden md:flex items-center space-x-1 pl-4 border-l border-slate-200 text-sm font-medium text-slate-600">
            <Link href="/app" className="px-3 py-2 rounded-md hover:bg-slate-100 hover:text-slate-900 transition">
              Workspace
            </Link>
            <Link href="/app/approvals" className="flex items-center space-x-1 px-3 py-2 rounded-md hover:bg-slate-100 hover:text-slate-900 transition">
              <CheckSquare className="h-4 w-4 text-orange-600" />
              <span>Approvals</span>
            </Link>
            <Link href="/app/documents" className="flex items-center space-x-1 px-3 py-2 rounded-md hover:bg-slate-100 hover:text-slate-900 transition">
              <FileText className="h-4 w-4 text-blue-600" />
              <span>Documents</span>
            </Link>
            <Link href="/app/insights" className="flex items-center space-x-1 px-3 py-2 rounded-md hover:bg-slate-100 hover:text-slate-900 transition">
              <BarChart2 className="h-4 w-4 text-emerald-600" />
              <span>Insights</span>
            </Link>
            <Link href="/app/integrations" className="flex items-center space-x-1 px-3 py-2 rounded-md hover:bg-slate-100 hover:text-slate-900 transition">
              <Radio className="h-4 w-4 text-purple-600" />
              <span>Integrations</span>
            </Link>
          </nav>
        </div>

        <div className="flex items-center space-x-3">
          <Link
            href="/app/new"
            className="flex items-center space-x-2 rounded-lg bg-orange-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-orange-700 transition"
          >
            <Plus className="h-4 w-4" />
            <span>Resolve Problem</span>
          </Link>
        </div>
      </div>
    </header>
  );
}
