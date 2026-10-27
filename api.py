"""Optional FastAPI service. Run with: uvicorn api:app --host 127.0.0.1 --port 8000"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
from backend import process_document, save_record, list_records, get_record

app = FastAPI(title="Intelligent Document Processing API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Intelligent Document Processing API", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/process")
async def process(file: UploadFile = File(...)):
    name = Path(file.filename or "document").name
    try:
        raw = await file.read()
        result = process_document(raw, name)
        record_id = save_record(name, result)
        result["record_id"] = record_id
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Processing failed: {type(exc).__name__}: {exc}")

@app.get("/documents")
def documents():
    return list_records()

@app.get("/documents/{record_id}")
def document(record_id: int):
    result = get_record(record_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return result
