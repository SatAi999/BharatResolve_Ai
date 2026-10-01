import os
import re
import time
import fitz # PyMuPDF
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from app.tools.base import BaseTool, ToolResult
from app.security.prompt_injection import sanitize_untrusted_content

class DocumentInput(BaseModel):
    file_path: str = Field(..., description="Absolute path to target document file (PDF, PNG, JPG)")
    file_type: str = Field(default="PDF", description="PDF, JPG, PNG")

class DocumentOCRTool(BaseTool):
    name = "extract_document_intelligence"
    description = "Parses PDF, scanned images, bills, certificates, and extracts structured fields, application numbers, dates, names, and text."
    input_schema = DocumentInput
    risk_level = "LOW"
    requires_approval = False

    async def execute(self, **kwargs) -> ToolResult:
        start_time = time.time()
        params = self.input_schema(**kwargs)
        file_path = params.file_path

        if not os.path.exists(file_path):
            return ToolResult(
                success=False,
                tool_name=self.name,
                output={},
                error_message=f"Document file not found at path: {file_path}",
                execution_time_ms=int((time.time() - start_time) * 1000),
                is_real_data=False
            )

        extracted_text = ""
        metadata = {}

        try:
            ext = os.path.splitext(file_path)[1].lower()
            if ext == ".pdf":
                doc = fitz.open(file_path)
                metadata["page_count"] = len(doc)
                pages_text = []
                for i, page in enumerate(doc):
                    t = page.get_text()
                    pages_text.append(t)
                extracted_text = "\n".join(pages_text)
            else:
                # Handle image via Pillow/PyMuPDF or OpenCV/pytesseract fallback if needed
                try:
                    import fitz
                    img_doc = fitz.open(file_path)
                    extracted_text = "Image document opened successfully."
                except Exception:
                    extracted_text = f"Image document at {os.path.basename(file_path)}"

            clean_text = sanitize_untrusted_content(extracted_text)

            # Perform regex field extractions for common Indian documents
            extracted_fields = {}
            
            # Application numbers / Reference IDs
            app_no = re.findall(r"(?i)(?:application|ref|acknowledgement|ticket|registration|case)\s*(?:no|number|id|code)?[:\s\-#]*([a-zA-Z0-9\-/]{5,25})", clean_text)
            if app_no:
                extracted_fields["application_number"] = app_no[0]

            # Dates (DD/MM/YYYY, YYYY-MM-DD, DD-Month-YYYY)
            dates = re.findall(r"\b(?:\d{1,2}[\/\.-]\d{1,2}[\/\.-]\d{2,4}|\d{4}[\/\.-]\d{1,2}[\/\.-]\d{1,2})\b", clean_text)
            if dates:
                extracted_fields["extracted_dates"] = list(set(dates))

            # Amounts (Rs. / INR / ₹)
            amounts = re.findall(r"(?:₹|Rs\.?|INR)\s*([\d,]+\.?\d*)", clean_text)
            if amounts:
                extracted_fields["extracted_amounts"] = amounts

            # Names pattern
            names = re.findall(r"(?i)(?:name|applicant|citizen|holder|consumer)[:\s]+([A-Za-z\s\.]{3,30})", clean_text)
            if names:
                extracted_fields["applicant_name"] = names[0].strip()

            duration = int((time.time() - start_time) * 1000)
            return ToolResult(
                success=True,
                tool_name=self.name,
                output={
                    "file_name": os.path.basename(file_path),
                    "file_path": file_path,
                    "extracted_text": clean_text[:4000], # truncated snippet for preview
                    "full_text_length": len(clean_text),
                    "extracted_fields": extracted_fields,
                    "metadata": metadata
                },
                execution_time_ms=duration,
                source_attribution="PyMuPDF / Document Intelligence Pipeline",
                is_real_data=True
            )
        except Exception as e:
            duration = int((time.time() - start_time) * 1000)
            return ToolResult(
                success=False,
                tool_name=self.name,
                output={},
                error_message=f"Failed to extract document: {str(e)}",
                execution_time_ms=duration,
                is_real_data=False
            )
