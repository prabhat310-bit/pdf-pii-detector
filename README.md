# PDF PII Detection API

An AI-powered backend application that detects Personally Identifiable Information (PII) from uploaded PDF documents using FastAPI and LLMs.

---

## 🚀 Project Overview

This project allows users to upload a PDF file and automatically extract sensitive information such as names, emails, phone numbers, and addresses.

It combines:
- PDF text extraction
- LLM-based PII detection
- API-based architecture

---

## 🧠 Key Features

- Upload PDF files via API
- Extract text from documents using PyyMUPDF
- Detect PII using LLM
- Return structured JSON output
- Modular and scalable backend design

---

## 🏗️ Tech Stack

- **Backend:** FastAPI
- **LLM Integration:** Llama + Groq (or similar)
- **PDF Processing:** PyMUPDF 
- **Frontend:** Basic HTML, CSS, JavaScript
- **API Testing:** Swagger UI (/docs)

---

## 📂 Project Structure
project/
│
├── main.py # FastAPI app and routes
├── services/
│ ├── pdf_parser.py # Extract text from PDF
│ └── llm_service.py # LLM interaction and PII detection
│
├── frontend/
│ ├── index.html
│ ├── script.js
│ └── style.css
│
├── requirements.txt
└── README.md


---


---

## ⚙️ How It Works

1. User uploads a PDF file from frontend
2. File is sent to FastAPI backend via POST request
3. Backend extracts text using PDF parser
4. Text is passed to LLM via API call
5. LLM detects PII and returns structured output
6. Response is sent back to frontend and displayed

---

## 🔄 API Endpoint

### POST `/process`

**Request:**
- Form-data
  - `file`: PDF file

**Response:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "1234567890"
}

