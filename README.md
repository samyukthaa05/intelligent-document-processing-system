# 📄 Intelligent Document Processing System

An Intelligent Document Processing (IDP) application that extracts useful information from invoices and business documents using Optical Character Recognition (OCR), text processing, and rule-based field extraction.

The application provides a Streamlit user interface for uploading documents, reviewing extracted information, validating fields, and exporting structured results. It also includes an optional FastAPI backend and SQLite storage for reviewed records.

## 📌 Table of Contents

* [Overview](#-overview)
* [Problem Statement](#-problem-statement)
* [Objectives](#-objectives)
* [Features](#-features)
* [System Architecture](#-system-architecture)
* [Technology Stack](#-technology-stack)
* [Project Structure](#-project-structure)
* [Installation and Setup](#-installation-and-setup)
* [How to Use](#-how-to-use)
* [API Endpoints](#-api-endpoints)
* [Testing](#-testing)
* [Limitations](#-limitations)
* [Future Enhancements](#-future-enhancements)
* [Contributing](#-contributing)

## 🔍 Overview

Businesses receive invoices and other documents in different formats, making manual data entry time-consuming and error-prone.

This project demonstrates how document processing can be simplified by extracting text, identifying important fields, validating the results, and converting the information into structured data.

Users can upload PDF or image documents, inspect the extracted information, correct inaccurate values, and export the reviewed data.

## 🎯 Problem Statement

Manual processing of invoices and business documents requires considerable time and effort. Important information such as invoice numbers, dates, company names, email addresses, and total amounts must often be entered manually.

The proposed system automates the initial extraction and validation process, helping users reduce repetitive work and organize document information more efficiently.

## 🎯 Objectives

* Automate text extraction from digital documents and supported images.
* Apply OCR to read text from images and scanned documents.
* Extract important invoice fields using configurable patterns.
* Validate extracted information and identify missing or suspicious values.
* Provide a user-friendly interface for reviewing and correcting results.
* Export structured information in JSON and CSV formats.
* Store reviewed results in a local SQLite database.
* Provide optional REST API endpoints for document processing.

## ✨ Features

### 1. Document Upload

* Supports PDF, PNG, JPG, and JPEG files.
* Enforces the application's 10 MB upload limit.
* Accepts digital documents and supported scanned documents.

### 2. Text Extraction and OCR

* Extracts embedded text from digital PDFs.
* Uses EasyOCR for supported image-based documents when the required OCR dependencies and models are available.
* Supports image processing through the document extraction pipeline.

### 3. Invoice Field Extraction

The system attempts to identify fields such as:

* Invoice number
* Invoice date
* Company or customer name
* Email address
* Phone number
* Total amount
* Currency

Extraction uses configurable, rule-based patterns. Results may vary depending on the document layout and quality.

### 4. Data Validation

* Checks extracted fields against configured validation rules.
* Identifies missing or suspicious values.
* Allows users to review and correct extracted information.

### 5. Interactive User Interface

* Built with Streamlit.
* Provides document upload and extraction workflows.
* Displays extracted text and structured fields.
* Supports reviewing and editing extracted values.
* Provides processing status and validation feedback.

### 6. Export and Storage

* Exports reviewed results to JSON and CSV.
* Stores reviewed records in a local SQLite database.
* Provides a saved-history interface for previously stored results.

### 7. REST API

* Includes an optional FastAPI backend.
* Provides document-processing and saved-record endpoints.
* Supports API health checks and interactive API documentation.

## 🏗️ System Architecture

The system follows a modular document-processing pipeline.

```text
                 ┌──────────────────────────┐
                 │      User / Document     │
                 │      PDF or Image        │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │   Streamlit User         │
                 │   Interface (app.py)     │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │   Document Processing    │
                 │   and Text Extraction    │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │   OCR / PDF Text Reading │
                 │   EasyOCR / PyMuPDF      │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │   Invoice Field          │
                 │   Extraction              │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │   Validation and         │
                 │   Manual Review          │
                 └────────────┬─────────────┘
                              │
                 ┌────────────┴─────────────┐
                 ▼                          ▼
       ┌──────────────────┐       ┌──────────────────┐
       │ JSON / CSV Export│       │ SQLite Storage   │
       └──────────────────┘       └──────────────────┘
```

An optional FastAPI interface exposes document-processing and record-management functionality through REST endpoints.

## 🛠️ Technology Stack

| Technology                | Purpose                             |
| ------------------------- | ----------------------------------- |
| Python                    | Core application logic              |
| Streamlit                 | Interactive user interface          |
| EasyOCR                   | Optical Character Recognition       |
| PyMuPDF                   | Digital PDF text extraction         |
| Pillow                    | Image handling                      |
| FastAPI                   | Optional REST API                   |
| Uvicorn                   | API server                          |
| SQLite                    | Local data storage                  |
| Pandas                    | Structured data handling and export |
| Pytest-compatible testing | Backend test execution              |

## 📂 Project Structure

```text
intelligent-document-processing-system/
│
├── app.py                 # Streamlit user interface
├── backend.py             # Extraction, validation and storage
├── api.py                 # FastAPI endpoints
├── requirements.txt       # Python dependencies
├── test_backend.py        # Backend tests
├── sample_invoice.txt     # Sample invoice text
├── README.md              # Project documentation
├── .gitignore             # Excluded files and folders
│
└── data/                  # Local runtime data, if created
```

The `data/` directory and local database files may be created while using the application. Runtime data should not be committed to the public repository.

## ⚙️ Installation and Setup

### Prerequisites

* Python 3.12 recommended.
* GitHub repository containing the project files.
* Internet connection for installing dependencies and downloading OCR models when required.

### Step 1: Clone the Repository

Open Command Prompt or a terminal and run:

```bash
git clone https://github.com/samyukthaa05/intelligent-document-processing-system.git
```

Move into the project directory:

```bash
cd intelligent-document-processing-system
```

### Step 2: Create a Virtual Environment

On Windows:

```bash
py -3.12 -m venv .venv
```

Activate the environment:

```bat
.venv\Scripts\activate
```

### Step 3: Install Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install the project requirements:

```bash
python -m pip install -r requirements.txt
```

Wait until the installation finishes.

### Step 4: Run the Streamlit Application

```bash
python -m streamlit run app.py
```

Open the local address displayed in the terminal. The default Streamlit address is:

```text
http://localhost:8501
```

### Optional: Run the FastAPI Backend

Open a second terminal in the project directory, activate the virtual environment, and run:

```bash
uvicorn api:app --host 127.0.0.1 --port 8000
```

API health check:

```text
http://127.0.0.1:8000/health
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

If port 8000 is already in use, select another available port.

## 🚀 How to Use

1. Start the Streamlit application.
2. Open the application in your browser.
3. Navigate to the document-processing section.
4. Upload a PDF, PNG, JPG, or JPEG document.
5. Start the extraction process.
6. Review the extracted text and identified fields.
7. Correct inaccurate or missing values where necessary.
8. Check validation warnings.
9. Download the reviewed results in JSON or CSV format.
10. Save reviewed results to the local history when needed.

**Important:** Always verify extracted values before using them in business processes.

## 🔌 API Endpoints

The optional FastAPI backend provides endpoints for document processing and record management.

| Endpoint                     | Purpose                          |
| ---------------------------- | -------------------------------- |
| `GET /`                      | API information                  |
| `GET /health`                | Health check                     |
| `POST /process`              | Process an uploaded document     |
| `GET /documents`             | Retrieve saved document records  |
| `GET /documents/{record_id}` | Retrieve a specific saved record |

Interactive documentation is available at `/docs` while the API server is running.

## 🧪 Testing

The repository includes `test_backend.py` for backend testing.

To run the test file:

```bash
python test_backend.py
```

Review the terminal output to determine whether the tests pass.

Test the application with different document types, including:

* Digital PDFs with embedded text.
* Clear invoice images.
* Scanned documents supported by the OCR pipeline.
* Documents containing missing or incorrectly formatted fields.
* Documents with different invoice layouts.

Verify extraction results, validation messages, file exports, and saved-history functionality.

## ⚠️ Limitations

* Extraction patterns are designed as a baseline and may not work for every invoice format.
* OCR accuracy depends on image quality, resolution, orientation, and text clarity.
* Extracted fields may be incomplete or incorrect.
* Scanned PDF processing requires the necessary OCR dependencies and model files.
* Validation rules cannot guarantee that all extracted values are correct.
* The SQLite database is local to the environment where the application runs.
* This project is a demonstration system and should not be treated as a fully production-ready document-processing platform.

## 🔮 Future Enhancements

Potential improvements include:

* Machine-learning-based document classification.
* More advanced Named Entity Recognition (NER).
* Confidence scores for extracted fields.
* Improved table and line-item extraction.
* Support for additional document formats and layouts.
* Authentication and role-based access control.
* Cloud database integration.
* Automated testing and continuous integration.
* Deployment as a publicly accessible web application.
* Improved multilingual OCR support.

These are potential future enhancements and are not necessarily implemented in the current version.

## 🤝 Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a branch for your changes.
3. Implement and test your changes.
4. Submit a pull request describing your improvements.

## 🔐 Data and Privacy

Do not upload confidential invoices, personal information, passwords, API keys, or other sensitive information to a public repository.

Review extracted information before exporting or sharing it.

## 📜 License

A license has not yet been specified for this repository. Add an appropriate open-source license if you intend to permit others to reuse or modify the project.

---

**Project:** Intelligent Document Processing System
**Repository:** [GitHub Repository](https://github.com/samyukthaa05/intelligent-document-processing-system)
