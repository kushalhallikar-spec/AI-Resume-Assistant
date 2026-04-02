# 🚀 AI Resume Assistant

A Machine Learning + NLP based application that analyzes resumes against job descriptions and provides actionable insights to improve job matching.

---

## 🧠 Overview

This project helps users evaluate how well their resume matches a job description. It extracts relevant skills, computes similarity scores, and provides meaningful feedback to improve resume quality.

---

## ✨ Features

* 📄 Upload Resume (PDF)
* 📝 Paste Job Description
* 🎯 Match Score using TF-IDF & Cosine Similarity
* 🚨 Missing Skills Detection
* ✅ Matched Skills Identification
* 🧠 Smart Feedback System
* 📊 Clean and interactive UI using Streamlit

---

## ⚙️ Tech Stack

* **Python**
* **Streamlit**
* **Scikit-learn**
* **NLP (TF-IDF, Text Cleaning)**
* **PyPDF2**

---

## 🧩 How It Works

1. Resume is parsed from PDF
2. Text is cleaned (stopword removal, normalization)
3. Skills are extracted using predefined skill mapping
4. TF-IDF vectorization converts text to numerical form
5. Cosine similarity calculates match score
6. Missing & matched skills are identified
7. Smart feedback is generated

---

## 📊 Sample Output

* Match Score: 72%
* Missing Skills: SQL, Machine Learning
* Matched Skills: Python, Pandas
* Feedback: Suggestions to improve resume quality

---

## 🚀 Run Locally

```bash
git clone https://github.com/kushalhallikar-spec/AI-Resume-Assistant.git
cd AI-Resume-Assistant
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Project Structure

```text
AI-Resume-Assistant/
│
├── app.py
├── utils.py
├── requirements.txt
├── README.md
```

## 📊 Results

- Achieved meaningful match scoring using TF-IDF  
- Successfully identified skill gaps  
- Provided actionable resume improvement suggestions  
---

## 🧠 Key Learnings

- Importance of text preprocessing in NLP  
- Feature extraction using TF-IDF  
- Building end-to-end ML applications  
- Deploying models using Streamlit

## 🎯 Future Improvements

* Add real-time job scraping
* Improve skill detection using advanced NLP
* Integrate LLM for dynamic feedback
* Export analysis report (PDF)

---

## 👨‍💻 Author

**Kushal**
Aspiring Machine Learning Engineer

---

⭐ If you found this project useful, consider giving it a star!
