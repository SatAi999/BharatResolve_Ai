export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface CaseResponse {
  id: string;
  title: string;
  raw_input: string;
  normalized_problem: string | null;
  domain: string;
  intent: string;
  language: string;
  urgency: string;
  status: string;
  risk_level: string;
  confidence_score: number;
  resolution_score: number;
  summary: string | null;
  created_at: string;
  updated_at: string;
  messages: Array<{
    id: string;
    sender: string;
    content: string;
    message_type: string;
    created_at: string;
  }>;
  entities: Array<{
    entity_type: string;
    entity_value: string;
    confidence: number;
    source: string;
  }>;
  evidence_items: Array<{
    id?: string;
    source_type: string;
    source_title: string;
    source_url?: string;
    claim_supported: string;
    confidence: number;
    status: string;
    retrieved_at?: string;
  }>;
  plans: Array<{
    id?: string;
    objective: string;
    status: string;
    steps: Array<{
      id?: string;
      step_number: number;
      title: string;
      description?: string;
      action_type: string;
      risk_level: string;
      status: string;
      result_summary?: string;
    }>;
  }>;
  actions: Array<{
    id?: string;
    action_name: string;
    description: string;
    risk_level: string;
    requires_approval: boolean;
    status: string;
    payload?: any;
    output_result?: any;
  }>;
  approvals: Array<{
    id: string;
    case_id: string;
    action_id?: string;
    title: string;
    reason: string;
    risk_level: string;
    status: string;
    approved_by?: string;
    decision_notes?: string;
    requested_at: string;
  }>;
  verification_results: Array<{
    id?: string;
    verification_type: string;
    status: string;
    details?: any;
    verified_at?: string;
  }>;
  audit_events: Array<{
    id?: string;
    event_type: string;
    actor: string;
    payload?: any;
    created_at?: string;
  }>;
}

export async function createCase(raw_input: string, language: string = "en"): Promise<CaseResponse> {
  const res = await fetch(`${API_BASE_URL}/api/cases`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ raw_input, language })
  });
  if (!res.ok) throw new Error(`Failed to create case: ${res.statusText}`);
  return res.json();
}

export async function fetchCases(domain?: string, status?: string): Promise<CaseResponse[]> {
  let url = `${API_BASE_URL}/api/cases`;
  const params = new URLSearchParams();
  if (domain) params.append("domain", domain);
  if (status) params.append("status", status);
  if (params.toString()) url += `?${params.toString()}`;

  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch cases");
  return res.json();
}

export async function fetchCaseById(id: string): Promise<CaseResponse> {
  const res = await fetch(`${API_BASE_URL}/api/cases/${id}`);
  if (!res.ok) throw new Error(`Failed to fetch case ${id}`);
  return res.json();
}

export async function decideApproval(approval_id: string, decision: "APPROVED" | "REJECTED", notes?: string) {
  const res = await fetch(`${API_BASE_URL}/api/approvals/${approval_id}/decide`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ approval_id, decision, notes, approved_by: "Citizen User" })
  });
  if (!res.ok) throw new Error("Failed to submit approval decision");
  return res.json();
}

export async function fetchPendingApprovals() {
  const res = await fetch(`${API_BASE_URL}/api/approvals`);
  if (!res.ok) throw new Error("Failed to fetch approvals");
  return res.json();
}

export async function checkCounterfactual(problem_statement: string, extracted_fields: any = {}, documents_count: number = 0) {
  const res = await fetch(`${API_BASE_URL}/api/counterfactual/check`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ problem_statement, extracted_fields, documents_count })
  });
  if (!res.ok) throw new Error("Failed counterfactual check");
  return res.json();
}

export async function fetchIntegrations() {
  const res = await fetch(`${API_BASE_URL}/api/integrations`);
  if (!res.ok) throw new Error("Failed to fetch integrations");
  return res.json();
}

export async function fetchSystemInsights() {
  const res = await fetch(`${API_BASE_URL}/api/insights`);
  if (!res.ok) throw new Error("Failed to fetch system insights");
  return res.json();
}

export async function uploadDocument(case_id: string, file: File) {
  const formData = new FormData();
  formData.append("case_id", case_id);
  formData.append("file", file);

  const res = await fetch(`${API_BASE_URL}/api/documents/upload`, {
    method: "POST",
    body: formData
  });
  if (!res.ok) throw new Error("Failed to upload document");
  return res.json();
}
