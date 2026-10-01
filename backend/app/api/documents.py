import os
import uuid
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.db import Document, Case
from app.tools.registry import tool_registry

router = APIRouter(prefix="/api/documents", tags=["Documents"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(
    case_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    file_ext = os.path.splitext(file.filename)[1]
    saved_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, saved_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    doc = Document(
        case_id=case_id,
        file_name=file.filename,
        file_path=os.path.abspath(file_path),
        mime_type=file.content_type or "application/octet-stream",
        file_size=os.path.getsize(file_path),
        document_type="PDF" if file_ext.lower() == ".pdf" else "IMAGE",
        status="UPLOADED"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # Immediately run Document OCR Tool
    ocr_result = await tool_registry.execute_tool("extract_document_intelligence", {
        "file_path": doc.file_path,
        "file_type": doc.document_type
    })

    if ocr_result.success:
        doc.ocr_text = ocr_result.output.get("extracted_text")
        doc.extracted_fields = ocr_result.output.get("extracted_fields")
        doc.status = "PROCESSED"
        db.commit()

    return {
        "document_id": doc.id,
        "file_name": doc.file_name,
        "status": doc.status,
        "extracted_fields": doc.extracted_fields,
        "ocr_preview": (doc.ocr_text or "")[:300]
    }

@router.get("")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).order_by(Document.created_at.desc()).all()
    return [
        {
            "id": d.id,
            "case_id": d.case_id,
            "file_name": d.file_name,
            "mime_type": d.mime_type,
            "file_size": d.file_size,
            "document_type": d.document_type,
            "status": d.status,
            "extracted_fields": d.extracted_fields,
            "ocr_preview": (d.ocr_text or "")[:300],
            "created_at": d.created_at.isoformat() if d.created_at else None
        }
        for d in docs
    ]
