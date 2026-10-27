# Intelligent Document Processing System

A Python project that reads PDF and image documents, extracts text, identifies useful invoice fields, validates extracted values, and lets users review/export the result. It includes a Streamlit interface, a FastAPI REST API, and SQLite storage for reviewed results.

## Features
- Upload PDF, PNG, JPG, and JPEG documents (maximum 10 MB).
- Extract embedded text from digital PDFs.
- Use EasyOCR for images and scanned PDFs when the OCR dependencies are installed.
- Extract invoice number, date, company name, email, phone, total amount, and currency with configurable regex rules.
- Flag missing or suspicious fields for manual review.
- Edit extracted fields in the UI.
- Export results to JSON or CSV.
- Save reviewed results to a local SQLite database.
- Optional FastAPI endpoints and interactive API docs.

## Requirements
- Python 3.10–3.12 recommended.
- Internet access the first time EasyOCR is used because its OCR models may need to download.
- OCR model startup can take a little time. CPU mode is configured to avoid CUDA setup issues.

## Run on Windows
Open Command Prompt or Anaconda Prompt in this project folder.

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

The Streamlit page normally opens at `http://localhost:8501`.

### Run the API (optional)
Open a second terminal in the same folder and activate the environment, then run:

```bash
uvicorn api:app --host 127.0.0.1 --port 8000
```

API health check: `http://127.0.0.1:8000/health`  
Interactive docs: `http://127.0.0.1:8000/docs`

If port 8000 is busy, change it to `--port 8001`.

## How to use
1. Open the Streamlit app.
2. Upload a PDF or image.
3. Click **Extract information**.
4. Check the extracted fields and validation warnings.
5. Correct any inaccurate values.
6. Download JSON/CSV, or save the reviewed result to local history.

## Important notes
- OCR and regex extraction are not perfect. Always review values, especially dates, totals, and company names.
- The field extraction patterns are intended as a solid demo baseline, not a universal invoice parser. Customize `backend.py` for your document formats.
- For a scanned PDF, OCR requires EasyOCR and its model weights. If OCR cannot start, the UI will show an empty extraction result or warning; digital PDFs can still be read without OCR.
- The local SQLite database and uploads/data are created at runtime and excluded from GitHub.
- Do not upload confidential customer documents, API keys, passwords, or personal data to a public repository.

## Project structure
```text
intelligent_document_processing_system/
├── app.py             # Streamlit user interface
├── backend.py         # OCR, extraction, validation, SQLite storage
├── api.py             # Optional FastAPI endpoints
├── requirements.txt
├── README.md
├── .gitignore
└── data/              # Created locally at runtime; ignored by Git
```

## GitHub upload
Upload the project files to a repository. Include `app.py`, `backend.py`, `api.py`, `requirements.txt`, `README.md`, and `.gitignore`. Do not upload `.venv`, `data`, database files, logs, or private documents.
