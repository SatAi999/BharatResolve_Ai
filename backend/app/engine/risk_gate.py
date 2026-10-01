from typing import Dict, Any, Tuple

def evaluate_action_risk(action_name: str, payload: Dict[str, Any]) -> Tuple[str, bool, str]:
    """
    Evaluates the risk level of an agent action.
    Returns: (risk_level, requires_human_approval, reason)
    """
    name_lower = action_name.lower()
    
    # CRITICAL Risk Actions
    if any(k in name_lower for k in ["financial_disbursement", "legal_binding_submission", "delete_account", "identity_change"]):
        return ("CRITICAL", True, "Action involves financial, legal, or sensitive identity modification.")

    # HIGH Risk Actions
    if any(k in name_lower for k in ["submit_official_complaint", "pay_fee", "transfer_case"]):
        return ("HIGH", True, "Action interacts directly with external official portals with permanent impact.")

    # MEDIUM Risk Actions
    if any(k in name_lower for k in ["prepare_grievance", "send_prepared_communication", "generate_rti"]):
        return ("MEDIUM", True, "Action creates formal documentation or dispatches communication.")

    # LOW Risk Actions (Auto-permitted)
    return ("LOW", False, "Read-only investigation, document extraction, or local verification.")
