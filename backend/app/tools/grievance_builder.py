import time
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from app.tools.base import BaseTool, ToolResult

class GrievanceBuilderInput(BaseModel):
    grievance_type: str = Field(..., description="CPGRAMS, RTI, CONSUMER_COURT, UTILITY_BOARD, SCHOLARSHIP_OFFICE")
    applicant_name: str = Field(..., description="Full legal name of citizen")
    target_authority: str = Field(..., description="Target department or authority e.g. 'State Electricity Distribution Co. Ltd.' or 'Ministry of Social Justice'")
    case_summary: str = Field(..., description="Detailed description of problem")
    application_ref_number: Optional[str] = Field(default=None, description="Reference application number if available")
    desired_relief: str = Field(..., description="Action demanded by citizen")

class GrievanceBuilderTool(BaseTool):
    name = "prepare_grievance"
    description = "Generates an official, legally structured grievance complaint, RTI application, or formal representation document for Indian government portals and consumer forums."
    input_schema = GrievanceBuilderInput
    risk_level = "MEDIUM"
    requires_approval = True

    async def execute(self, **kwargs) -> ToolResult:
        start_time = time.time()
        params = self.input_schema(**kwargs)

        document_content = f"""================================================================================
OFFICIAL GRIEVANCE REPRESENTATION / COMPLAINT FORM ({params.grievance_type})
================================================================================

TO:
The Nodal Officer / Competent Authority,
{params.target_authority}

DATE: {time.strftime('%Y-%m-%d')}
SUBJECT: Grievance regarding {params.case_summary[:80]}...

RESPECTED SIR / MADAM,

I, {params.applicant_name}, am submitting this formal grievance for your immediate intervention and resolution.

1. CASE REFERENCE / APPLICATION ID:
   {params.application_ref_number if params.application_ref_number else "N/A - Direct Complaint"}

2. STATEMENT OF FACTS & PROBLEM DETAILS:
   {params.case_summary}

3. GROUNDS FOR COMPLAINT:
   - Delay or procedural non-compliance beyond stipulated Citizens' Charter timeline.
   - Discrepancy between official status/records and physical fulfillment.

4. DEMANDED RELIEF / ACTION REQUESTED:
   {params.desired_relief}

I declare that the information provided above is true to the best of my knowledge.
Kindly provide an acknowledgement and official tracking number for this representation.

YOURS FAITHFULLY,
{params.applicant_name}
(Generated & Verified by BharatResolve AI Engine)
================================================================================"""

        duration = int((time.time() - start_time) * 1000)
        return ToolResult(
            success=True,
            tool_name=self.name,
            output={
                "grievance_type": params.grievance_type,
                "target_authority": params.target_authority,
                "applicant_name": params.applicant_name,
                "formatted_document": document_content,
                "word_count": len(document_content.split()),
                "status": "PREPARED_READY_FOR_SUBMISSION"
            },
            execution_time_ms=duration,
            source_attribution="BharatResolve AI Grievance Generator Engine",
            is_real_data=True
        )
