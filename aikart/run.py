import os
import sys
import json
import asyncio
import traceback

# Ensure backend modules are in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.db.session import SessionLocal, Base, engine
from app.models.db import Case, CaseMessage
from app.engine.state_graph import orchestrator

# Initialize DB tables
Base.metadata.create_all(bind=engine)

async def main():
    try:
        input_data = {}
        
        # 1. Read input from /aikart/input.json or AIKART_INPUT env var
        input_file = "/aikart/input.json"
        if os.path.exists(input_file):
            with open(input_file, "r", encoding="utf-8") as f:
                input_data = json.load(f)
        elif os.getenv("AIKART_INPUT"):
            try:
                input_data = json.loads(os.getenv("AIKART_INPUT", "{}"))
            except Exception:
                input_data = {"problem_statement": os.getenv("AIKART_INPUT")}
        else:
            input_data = {"problem_statement": "My scholarship was approved but I have not received payment."}

        raw_problem = input_data.get("problem_statement") or input_data.get("prompt") or input_data.get("description") or "Citizen Grievance Investigation"
        
        case_id = None
        with SessionLocal() as db:
            case = Case(
                title=raw_problem[:60] + "...",
                raw_input=raw_problem,
                language=input_data.get("language", "en"),
                status="CREATED"
            )
            db.add(case)
            db.commit()
            db.refresh(case)
            case_id = case.id

            msg = CaseMessage(case_id=case_id, sender="user", content=raw_problem)
            db.add(msg)
            db.commit()

        # 2. Execute workflow
        final_state = await orchestrator.execute_case_workflow(case_id)

        # 3. Generate Markdown Report
        with SessionLocal() as db:
            c = db.query(Case).filter(Case.id == case_id).first()

            report_markdown = f"""# BHARATRESOLVE AI - CASE RESOLUTION REPORT

**Case ID:** `{c.id}`  
**Domain:** `{c.domain}`  
**Intent:** `{c.intent}`  
**Resolution Score:** `{c.resolution_score}` (Scale 0.0 - 1.0)  
**Status:** `{c.status}`  
**Urgency:** `{c.urgency}`  

---

## 1. PROBLEM SUMMARY
{c.normalized_problem or c.raw_input}

---

## 2. GATHERED EVIDENCE & INVESTIGATION
"""
            if c.evidence_items:
                for idx, ev in enumerate(c.evidence_items, 1):
                    report_markdown += f"{idx}. **[{ev.source_type.upper()}]** {ev.source_title}: {ev.claim_supported} (Status: `{ev.status}`)\n"
            else:
                report_markdown += "_No evidence items collected. Status forced to UNVERIFIED under anti-hallucination guard._\n"

            report_markdown += """
---

## 3. RESOLUTION PLAN & EXECUTED ACTIONS
"""
            if c.actions:
                for idx, act in enumerate(c.actions, 1):
                    report_markdown += f"{idx}. **Action:** `{act.action_name}` - Status: `{act.status}` (Risk: `{act.risk_level}`)\n"
            else:
                report_markdown += "_No autonomous actions executed._\n"

            report_markdown += f"""
---

## 4. EXECUTIVE SUMMARY
{c.summary or 'Case investigation completed and verified.'}

*Generated autonomously by BharatResolve AI Case-Resolution Engine.*
"""

        output_payload = {
            "format": "markdown",
            "response": report_markdown
        }

        output_dir = "/aikart"
        if os.path.exists(output_dir):
            output_file = os.path.join(output_dir, "output.json")
        else:
            output_file = "output.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_payload, f, indent=2)

        print(f"aiKart execution completed successfully. Output written to {output_file}")
        sys.exit(0)

    except Exception as e:
        print(f"FATAL: aiKart execution error: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
