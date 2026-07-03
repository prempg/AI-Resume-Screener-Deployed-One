# AI Resume Analyzer

AI Resume Analyzer is a full-stack GenAI application that analyzes a candidate's resume against a Job Description and provides:

- ATS Match Score
- Resume Strengths
- Resume Weaknesses
- Missing Skills
- Improvement Suggestions
- Better Resume Bullet Points
- Final Career Advice

The application supports both text-based and scanned/image-based resume PDFs.

## Architecture

User
↓
Streamlit UI
↓
FastAPI
↓
Redis Queue
↓
RQ Worker
↓
Resume Analyzer
↓
PDF Text Extraction / Vision Fallback
↓
Groq LLM
↓
MongoDB
↓
Analysis Result

## Tech Stack

### Backend
- Python
- FastAPI

### Frontend
- Streamlit

### AI
- Groq API
- LLM-based resume analysis
- Vision model fallback for scanned resumes

### Database
- MongoDB

### Background Processing
- Redis-compatible Valkey
- RQ Worker

### PDF Processing
- PyMuPDF
- pdf2image
- Poppler

### Infrastructure
- Docker Compose
- VS Code Dev Containers

## Features

### Resume Upload
Users can upload a resume in PDF format.

### Job Description Input
Users can either:
- Paste the Job Description as text
- Upload a Job Description PDF

### AI Resume Analysis
The application compares the resume with the Job Description and generates a structured analysis report.

### Scanned Resume Support
The system first attempts normal PDF text extraction.

If no text is found, the PDF is converted into images and analyzed using a vision-capable model.

### Background Job Processing
Resume analysis runs asynchronously using Redis/Valkey and RQ workers.

### Analysis Status
The frontend polls the backend and displays job status:

- queued
- processing
- processed
- failed

## Project Structure

```text
app/
├── analyzers/
│   └── resume_analyzer.py
├── api/
│   ├── health.py
│   └── resume.py
├── db/
├── job_queue/
│   ├── q.py
│   └── workers.py
├── prompts/
│   └── resume_prompt.py
├── services/
│   └── groq_service.py
├── utils/
│   ├── file.py
│   └── pdf.py
├── config.py
├── main.py
├── server.py
└── streamlit_app.py