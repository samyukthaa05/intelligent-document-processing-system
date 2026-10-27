"""Document extraction backend shared by Streamlit and FastAPI."""
import os, re, json, sqlite3, uuid
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
DB_PATH = DATA_DIR / "documents.db"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def _db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        created_at TEXT NOT NULL,
        result_json TEXT NOT NULL
    )""")
    conn.commit()
    return conn

def _pdf_text(raw: bytes) -> str:
    try:
        import fitz
        doc = fitz.open(stream=raw, filetype="pdf")
        return "\n".join(page.get_text("text") for page in doc).strip()
    except Exception:
        try:
            import pdfplumber, io
            with pdfplumber.open(io.BytesIO(raw)) as pdf:
                return "\n".join((p.extract_text() or "") for p in pdf.pages).strip()
        except Exception:
            return ""

def _image_ocr(raw: bytes) -> tuple[str, list]:
    """Use EasyOCR lazily; gracefully return a helpful message if unavailable."""
    try:
        import easyocr
        import numpy as np
        from PIL import Image
        import io
        image = Image.open(io.BytesIO(raw)).convert("RGB")
        arr = np.array(image)
        # EasyOCR model is initialized only when an image actually needs OCR.
        reader = easyocr.Reader(["en"], gpu=False, verbose=False)
        entries = reader.readtext(arr, detail=1, paragraph=False)
        text = "\n".join(str(item[1]) for item in entries)
        confidences = [float(item[2]) for item in entries if len(item) > 2]
        return text, confidences
    except Exception as exc:
        return "", [f"OCR unavailable: {type(exc).__name__}: {exc}"]

def _extract_fields(text: str) -> dict:
    def first(patterns):
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.I | re.M)
            if match:
                return match.group(1).strip(" \t:#")
        return ""
    invoice_number = first([
        r"(?:invoice\s*(?:no\.?|number|#|id))\s*[:#\-]?\s*([A-Z0-9][A-Z0-9\/\-]+)",
        r"\b(INV[-/ ]?\d{3,})\b"
    ])
    invoice_date = first([
        r"(?:invoice\s*date|date)\s*[:#\-]?\s*([0-3]?\d[\s./\-]+[A-Za-z]{3,9}[\s,./\-]+\d{2,4})",
        r"(?:invoice\s*date|date)\s*[:#\-]?\s*(\d{1,4}[./\-]\d{1,2}[./\-]\d{2,4})"
    ])
    email = first([r"\b([A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,})\b"])
    phone = first([r"(?:phone|mobile|tel(?:ephone)?)\s*[:#\-]?\s*(\+?\d[\d\s().\-]{7,}\d)", r"\b(\+?\d[\d\s().\-]{8,}\d)\b"])
    amount = first([
        r"(?:grand\s*total|total\s*amount|invoice\s*total|amount\s*due|total)\s*[:\-]?\s*(?:₹|INR|Rs\.?|USD|\$|€)?\s*([0-9,]+(?:\.\d{1,2})?)",
        r"(?:₹|INR|Rs\.?|\$|€)\s*([0-9,]+(?:\.\d{1,2})?)"
    ])
    currency = "INR" if re.search(r"₹|\bINR\b|\bRs\.?", text, re.I) else ("USD" if re.search(r"\$|\bUSD\b", text, re.I) else ("EUR" if "€" in text else ""))
    # Heuristic customer/vendor name: prefer a line near the top containing company suffix.
    company = ""
    for line in text.splitlines()[:18]:
        clean = re.sub(r"\s+", " ", line).strip(" :,-")
        if re.search(r"\b(Pvt\.?\s?Ltd\.?|Private Limited|Limited|Ltd\.?|LLP|Inc\.?|Corporation|Company)\b", clean, re.I) and len(clean) > 4:
            company = clean[:180]
            break
    return {
        "document_type": "invoice" if re.search(r"\binvoice\b", text, re.I) else "business document",
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
        "company_name": company,
        "email": email,
        "phone": phone,
        "total_amount": amount.replace(",", "") if amount else "",
        "currency": currency,
    }

def _validate(fields: dict) -> dict:
    issues = []
    if not fields.get("invoice_number"):
        issues.append("Invoice number not detected; review manually.")
    if not fields.get("invoice_date"):
        issues.append("Invoice date not detected; review manually.")
    if not fields.get("total_amount"):
        issues.append("Total amount not detected; review manually.")
    if fields.get("total_amount"):
        try:
            if float(fields["total_amount"]) < 0:
                issues.append("Total amount is negative; verify the value.")
        except ValueError:
            issues.append("Total amount is not numeric; review manually.")
    if fields.get("email") and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", fields["email"]):
        issues.append("Email format looks invalid.")
    return {"is_valid": len(issues) == 0, "issues": issues}

def process_document(raw: bytes, filename: str) -> dict:
    if not raw:
        raise ValueError("The uploaded file is empty.")
    if len(raw) > 10 * 1024 * 1024:
        raise ValueError("Maximum supported file size is 10 MB.")
    suffix = Path(filename).suffix.lower()
    if suffix not in {".pdf", ".png", ".jpg", ".jpeg"}:
        raise ValueError("Unsupported file type. Upload PDF, PNG, JPG, or JPEG.")
    ocr_confidences = []
    if suffix == ".pdf":
        text = _pdf_text(raw)
        # Scanned PDFs need OCR. Convert pages to images only if text extraction is empty.
        if not text.strip():
            try:
                import fitz, numpy as np
                from PIL import Image
                import io
                doc = fitz.open(stream=raw, filetype="pdf")
                chunks = []
                for page in doc:
                    pix = page.get_pixmap(matrix=fitz.Matrix(1.7, 1.7), alpha=False)
                    png_bytes = pix.tobytes("png")
                    chunk, conf = _image_ocr(png_bytes)
                    chunks.append(chunk)
                    ocr_confidences.extend(conf)
                text = "\n".join(chunks)
            except Exception:
                pass
    else:
        text, ocr_confidences = _image_ocr(raw)
    fields = _extract_fields(text)
    warnings = [x for x in ocr_confidences if isinstance(x, str)]
    return {
        "filename": Path(filename).name,
        "processed_at": datetime.now().isoformat(timespec="seconds"),
        "text": text,
        "fields": fields,
        "validation": _validate(fields),
        "ocr": {"engine": "EasyOCR (if installed)", "confidence_values": [x for x in ocr_confidences if isinstance(x, float)], "warnings": warnings},
    }

def save_record(filename: str, result: dict) -> int:
    conn = _db()
    try:
        cur = conn.execute("INSERT INTO documents(filename, created_at, result_json) VALUES(?,?,?)",
                           (Path(filename).name, datetime.now().isoformat(timespec="seconds"), json.dumps(result, ensure_ascii=False)))
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()

def list_records() -> list:
    conn = _db()
    try:
        rows = conn.execute("SELECT id, filename, created_at FROM documents ORDER BY id DESC").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def get_record(record_id: int):
    conn = _db()
    try:
        row = conn.execute("SELECT result_json FROM documents WHERE id=?", (record_id,)).fetchone()
        return json.loads(row["result_json"]) if row else None
    finally:
        conn.close()

def delete_all_records():
    conn = _db()
    try:
        conn.execute("DELETE FROM documents")
        conn.commit()
    finally:
        conn.close()
