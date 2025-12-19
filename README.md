# SHL Assessment Recommendation System

This project implements an intelligent assessment recommendation system for SHL Individual Test Solutions.  
It accepts a natural language query or job description and returns the most relevant assessments by balancing technical and behavioral competencies.

The system is designed as an end-to-end solution including data scraping, recommendation logic, evaluation, API exposure, and a user-facing web application.

---

## 🚀 Features

- Scrapes SHL **Individual Test Solutions** (excluding pre-packaged solutions)
- Intelligent recommendation based on query intent
- Balanced results across:
  - Knowledge & Skills assessments
  - Personality & Behavioral assessments
- FastAPI backend with SHL-compliant API responses
- Streamlit frontend for easy interaction
- Evaluation using **Mean Recall@10**
- Production-ready setup with environment variables

---

## 🧠 System Architecture

**Workflow:**

1. User provides a job description or query
2. Query is analyzed for technical and behavioral intent
3. Assessments are ranked using relevance scoring
4. Balanced recommendations are selected
5. Results are returned via API and displayed in UI

---

## 📁 Project Structure

shl-assessment-recommendation/
│
├── backend/
│ ├── api/ # FastAPI endpoints
│ ├── core/ # Recommendation logic
│ └── utils/
│
├── frontend/ # Streamlit application
│
├── data/
│ ├── processed/ # SHL assessment catalog
│ └── evaluation/ # Train/Test datasets and outputs
│
├── experiments/ # Evaluation & submission scripts
│
├── approach.md # Detailed approach document
├── README.md
├── requirements.txt
└── .gitignore

yaml
Copy code

---

## 🔧 Setup Instructions (Local)

### 1️⃣ Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
2️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
▶️ Running the Application (Local)
Start Backend (FastAPI)
bash
Copy code
uvicorn backend.api.app:app --reload
Backend will be available at:

cpp
Copy code
http://127.0.0.1:8000
Health check:

bash
Copy code
GET /health
Start Frontend (Streamlit)
bash
Copy code
streamlit run frontend/app.py
Frontend will be available at:

arduino
Copy code
http://localhost:8501
🔌 API Endpoints
Health Check
bash
Copy code
GET /health
Response:

json
Copy code
{
  "status": "healthy"
}
Recommendation Endpoint
bash
Copy code
POST /recommend
Request:

json
Copy code
{
  "query": "Hiring a Java developer with good communication skills"
}
Response:

json
Copy code
{
  "recommended_assessments": [
    {
      "name": "...",
      "url": "...",
      "description": "...",
      "duration": 45,
      "remote_support": "Yes",
      "adaptive_support": "Yes",
      "test_type": ["Knowledge & Skills"]
    }
  ]
}
📊 Evaluation
Metric used: Mean Recall@10

Evaluated using provided labeled training dataset

Evaluation script located in:

bash
Copy code
experiments/evaluate.py
Run:

bash
Copy code
python experiments/evaluate.py
📄 Submission Artifacts
API URL (FastAPI)

Web application URL (Streamlit)

GitHub repository

approach.md (2-page approach document)

submission.csv (final predictions on test set)

🛠️ Technology Stack
Python

FastAPI

Streamlit

Pandas

scikit-learn

python-dotenv

 Author
Deeshanshi Sahu
B.Tech Computer Science
SHL Assessment – Generative AI Assignment

