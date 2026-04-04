# 🚀 AI Resume Assistant

> An end-to-end NLP + LLM powered application that analyses your resume against any job description and delivers real-time, actionable feedback to improve your ATS score and job-match quality.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?style=flat-square&logo=streamlit)
![Groq](https://img.shields.io/badge/LLM-Groq%20%7C%20Llama%203.3%2070B-orange?style=flat-square)
![NLP](https://img.shields.io/badge/NLP-TF--IDF%20%7C%20Cosine%20Similarity-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

---

## 📸 Demo

![App Screenshot](Screenshot%202026-04-02%20121105.png)

---

## 🧠 Overview

Most job seekers don't know why their resume gets rejected — the AI Resume Assistant solves that. Upload your PDF resume, paste a job description, and get:

- A **TF-IDF cosine similarity match score** between your resume and the JD
- **60+ skill gap analysis** across ML, cloud, databases, BI tools, and more
- **LLM-powered personalised feedback** via Groq's Llama 3.3 70B — covering strengths, gaps, quick wins, and a rewritten bullet point example

---

## ✨ Features

| Feature | Details |
|---|---|
| 📄 Resume Parsing | Extracts clean text from PDF using PyPDF2 |
| 🎯 Match Score | TF-IDF vectorisation + cosine similarity |
| 🧩 Skill Extraction | Regex-based matching across 60+ technical & soft skills |
| ✅ Matched Skills | Skills present in both resume and JD |
| 🚨 Missing Skills | Skills in JD but absent from resume |
| 💡 Bonus Skills | Extra skills on resume beyond JD requirements |
| 🤖 LLM Feedback | Groq API (Llama 3.3 70B) — structured, actionable career coaching |
| 🎨 Dark UI | Custom Streamlit dark theme with skill chips and score circle |

---

## ⚙️ Tech Stack

- **Language:** Python 3.10+
- **Frontend:** Streamlit (custom dark CSS)
- **NLP:** Scikit-learn (TF-IDF, Cosine Similarity), Regex
- **LLM:** Groq API — `llama-3.3-70b-versatile`
- **PDF Parsing:** PyPDF2

---

## 🧩 How It Works

```
Resume PDF  ──►  Text Extraction (PyPDF2)
                        │
                        ▼
              Text Cleaning & Normalisation
                        │
           ┌────────────┴────────────┐
           ▼                         ▼
   Skill Extraction           TF-IDF Vectorisation
   (60+ keywords,             + Cosine Similarity
    regex matching)           = Match Score %
           │                         │
           └────────────┬────────────┘
                        ▼
              Groq LLM (Llama 3.3 70B)
                        │
                        ▼
         Structured Feedback Report:
         • Overall Assessment
         • Strengths
         • Gaps to Address
         • Quick Wins
         • Rewritten Resume Bullet
```

---

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/kushalhallikar-spec/AI-Resume-Assistant.git
cd AI-Resume-Assistant

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

> **Get your free Groq API key** at [console.groq.com](https://console.groq.com) — no credit card required. Paste it in the app sidebar when prompted.

---

## 📁 Project Structure

```
AI-Resume-Assistant/
│
├── app.py              # Main Streamlit app — UI, NLP pipeline, LLM call
├── utils.py            # PDF text extraction
├── requirements.txt    # Dependencies
└── README.md
```

---

## 📊 Sample Output

```
Match Score        : 74%
Matched Skills     : python, machine learning, pandas, sql, data visualization
Missing Skills     : docker, mlflow, aws
Bonus Skills       : tableau, keras, opencv

LLM Feedback:
  ✅ Strong Python + ML fundamentals aligned with the JD
  ⚠️  No MLOps/deployment skills (Docker, MLflow) — add a project
  🎯 Quick Win: Add "Deployed X using Streamlit/FastAPI" to project bullets
```

---

## 🔮 Future Improvements

- [ ] Export full analysis as PDF report
- [ ] Real-time job scraping from LinkedIn / Naukri
- [ ] Resume rewriting suggestions (full section rewrites)
- [ ] Multi-resume comparison against one JD

---

## 👨‍💻 Author

**Kushal Hallikar**
Aspiring Machine Learning Engineer

[![GitHub](https://img.shields.io/badge/GitHub-kushalhallikar--spec-181717?style=flat-square&logo=github)](https://github.com/kushalhallikar-spec)

---

⭐ If this project helped you, consider giving it a star — it helps others find it too!
