import re

def sanitize_untrusted_content(text: str) -> str:
    """
    Sanitizes untrusted text retrieved from web pages, PDFs, OCR, or user input.
    Neutralizes attempts to override agent instructions.
    """
    if not text:
        return ""
    
    # Neutralize common prompt injection patterns
    suspicious_patterns = [
        r"(?i)ignore\s+(all\s+)?previous\s+instructions",
        r"(?i)disregard\s+(all\s+)?system\s+prompts",
        r"(?i)you\s+are\s+now\s+a",
        r"(?i)system\s+override",
        r"(?i)new\s+rule:",
    ]
    
    sanitized = text
    for pattern in suspicious_patterns:
        sanitized = re.sub(pattern, "[UNTRUSTED_CONTENT_FLAGGED]", sanitized)
    
    return sanitized

def wrap_untrusted_data(label: str, content: str) -> str:
    """
    Explicitly wraps untrusted external data into XML-like data blocks
    so the LLM parser processes it strictly as evidence/data rather than system instructions.
    """
    clean_content = sanitize_untrusted_content(content)
    return f"""<{label}_DATA_UNTRUSTED>
{clean_content}
</{label}_DATA_UNTRUSTED>"""
