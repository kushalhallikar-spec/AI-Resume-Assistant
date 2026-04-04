import streamlit as st
from groq import Groq
import re
from utils import extract_text_from_pdf
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Assistant",
    page_icon="🚀",
    layout="wide"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; }

    /* Section cards */
    .card {
        background: #1a1d27;
        border: 1px solid #2e3148;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    /* Score circle */
    .score-circle {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 130px;
        height: 130px;
        border-radius: 50%;
        font-size: 2rem;
        font-weight: 700;
        margin: auto;
    }
    .score-high   { background: #0d3b2e; border: 4px solid #00c896; color: #00c896; }
    .score-medium { background: #3b2d0d; border: 4px solid #f5a623; color: #f5a623; }
    .score-low    { background: #3b0d0d; border: 4px solid #e74c3c; color: #e74c3c; }

    /* Skill chips */
    .chip-matched { display:inline-block; background:#0d3b2e; color:#00c896;
                    border:1px solid #00c896; border-radius:20px;
                    padding:4px 12px; margin:3px; font-size:0.82rem; }
    .chip-missing { display:inline-block; background:#3b0d0d; color:#e74c3c;
                    border:1px solid #e74c3c; border-radius:20px;
                    padding:4px 12px; margin:3px; font-size:0.82rem; }
    .chip-extra   { display:inline-block; background:#1a2a3b; color:#5b9bd5;
                    border:1px solid #5b9bd5; border-radius:20px;
                    padding:4px 12px; margin:3px; font-size:0.82rem; }

    /* Section headers */
    .section-title {
        font-size: 1.1rem; font-weight: 600;
        color: #a0a8c0; text-transform: uppercase;
        letter-spacing: 0.08em; margin-bottom: 0.8rem;
    }

    /* LLM feedback box */
    .feedback-box {
        background: #12151f;
        border-left: 4px solid #7c6af7;
        border-radius: 0 8px 8px 0;
        padding: 1.2rem 1.5rem;
        line-height: 1.7;
        color: #d0d4e8;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Skill Dictionary (expanded) ────────────────────────────────────────────────
SKILLS = {
    # Programming
    "python", "r", "java", "scala", "c++", "c", "javascript", "typescript",
    "go", "rust", "bash", "shell scripting",
    # ML/DL
    "machine learning", "deep learning", "neural networks", "reinforcement learning",
    "transfer learning", "computer vision", "natural language processing", "nlp",
    "large language models", "llm", "generative ai", "transformers", "bert", "gpt",
    "fine-tuning", "rag", "retrieval augmented generation",
    # ML Libraries
    "scikit-learn", "tensorflow", "keras", "pytorch", "hugging face", "xgboost",
    "lightgbm", "catboost", "opencv", "spacy", "nltk", "langchain",
    # Data
    "pandas", "numpy", "matplotlib", "seaborn", "plotly", "data analysis",
    "data visualization", "feature engineering", "eda", "statistics",
    "hypothesis testing", "a/b testing", "data cleaning", "data wrangling",
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "firebase", "sqlite",
    "bigquery", "snowflake",
    # Cloud & MLOps
    "aws", "gcp", "azure", "docker", "kubernetes", "mlflow", "airflow",
    "ci/cd", "fastapi", "flask", "streamlit", "git", "github",
    # BI Tools
    "power bi", "tableau", "excel", "looker", "google analytics",
    # Soft skills
    "communication", "leadership", "problem solving", "teamwork", "agile", "scrum"
}


def extract_skills(text: str) -> set:
    """Extract skills using keyword matching with phrase support."""
    text_lower = text.lower()
    found = set()
    for skill in SKILLS:
        # Use word boundary for single words, plain search for multi-word
        if " " in skill:
            if skill in text_lower:
                found.add(skill)
        else:
            if re.search(rf"\b{re.escape(skill)}\b", text_lower):
                found.add(skill)
    return found


def compute_similarity(text1: str, text2: str) -> float:
    """TF-IDF cosine similarity between two texts."""
    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        vecs = vectorizer.fit_transform([text1, text2])
        return round(cosine_similarity(vecs[0:1], vecs[1:2])[0][0] * 100, 1)
    except Exception:
        return 0.0


def get_groq_feedback(resume_text: str, job_desc: str, score: float,
                      matched: list, missing: list, api_key: str) -> str:
    """Call Groq API for personalised resume feedback."""
    client = Groq(api_key=api_key)

    prompt = f"""You are an expert career coach and ATS specialist. Analyse the resume and job description below and provide actionable, specific feedback.

MATCH SCORE: {score}%
MATCHED SKILLS: {", ".join(matched) if matched else "None"}
MISSING SKILLS: {", ".join(missing) if missing else "None"}

--- RESUME (first 2000 chars) ---
{resume_text[:2000]}

--- JOB DESCRIPTION ---
{job_desc[:1500]}

Provide feedback in this exact format:

## 📊 Overall Assessment
(2-3 sentences on fit)

## ✅ Strengths
- (3 specific strengths from the resume relevant to this JD)

## ⚠️ Gaps to Address
- (3-4 specific gaps with actionable fixes)

## 🎯 Quick Wins (do these first)
- (2-3 immediate changes to improve ATS score)

## 💬 Suggested Resume Bullet (example)
Rewrite one weak area as a strong, metric-driven bullet point.

Keep the tone direct and practical. No generic advice."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    return response.choices[0].message.content


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 2rem 0 1rem 0;'>
    <h1 style='color:#ffffff; font-size:2.4rem; font-weight:800;'>🚀 AI Resume Assistant</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Sidebar: API Key ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    api_key = st.text_input("Groq API Key", type="password",
                            placeholder="gsk_...")
    st.caption("Get your free key at [console.groq.com](https://console.groq.com)")
    st.markdown("---")
    st.markdown("### 📖 How to Use")
    st.markdown("""
1. Enter your Anthropic API key
2. Upload your resume (PDF)
3. Paste the job description
4. Click **Analyse**
5. Review your personalised feedback
    """)

# ── Inputs ──────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.markdown('<div class="section-title">📄 Your Resume</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")

with col_right:
    st.markdown('<div class="section-title">💼 Job Description</div>', unsafe_allow_html=True)
    job_desc = st.text_area("Paste JD here", height=200, label_visibility="collapsed",
                            placeholder="Paste the full job description here...")

analyse_btn = st.button("🔍 Analyse Resume", use_container_width=True, type="primary")

st.markdown("---")

# ── Analysis ────────────────────────────────────────────────────────────────────
if analyse_btn:
    if not uploaded_file:
        st.warning("⚠️ Please upload your resume PDF.")
        st.stop()
    if not job_desc.strip():
        st.warning("⚠️ Please paste the job description.")
        st.stop()
    if not api_key:
        st.warning("⚠️ Please enter your Anthropic API key in the sidebar.")
        st.stop()

    with st.spinner("Extracting and analysing your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        score = compute_similarity(resume_text, job_desc)

        resume_skills = extract_skills(resume_text)
        job_skills    = extract_skills(job_desc)

        matched_skills = sorted(resume_skills & job_skills)
        missing_skills = sorted(job_skills - resume_skills)
        extra_skills   = sorted(resume_skills - job_skills)

    # ── Row 1: Score + Skills ────────────────────────────────────────────────
    r1_left, r1_right = st.columns([1, 2], gap="large")

    with r1_left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🎯 Match Score</div>', unsafe_allow_html=True)

        score_class = "score-high" if score >= 70 else ("score-medium" if score >= 45 else "score-low")
        label = "Strong Match" if score >= 70 else ("Moderate" if score >= 45 else "Weak Match")

        st.markdown(f"""
        <div class="score-circle {score_class}">{score}%</div>
        <p style='text-align:center; color:#a0a8c0; margin-top:0.8rem;'>{label}</p>
        """, unsafe_allow_html=True)
        st.progress(int(min(score, 100)))
        st.markdown('</div>', unsafe_allow_html=True)

    with r1_right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🧩 Skill Breakdown</div>', unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs([
            f"✅ Matched ({len(matched_skills)})",
            f"🚨 Missing ({len(missing_skills)})",
            f"💡 Bonus ({len(extra_skills)})"
        ])
        with tab1:
            if matched_skills:
                st.markdown(" ".join(f'<span class="chip-matched">{s}</span>' for s in matched_skills),
                            unsafe_allow_html=True)
            else:
                st.info("No matched skills detected.")
        with tab2:
            if missing_skills:
                st.markdown(" ".join(f'<span class="chip-missing">{s}</span>' for s in missing_skills),
                            unsafe_allow_html=True)
            else:
                st.success("No missing critical skills!")
        with tab3:
            if extra_skills:
                st.markdown(" ".join(f'<span class="chip-extra">{s}</span>' for s in extra_skills),
                            unsafe_allow_html=True)
            else:
                st.info("No extra skills detected.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Row 2: Claude Feedback ────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-title">🤖 AI Feedback</div>', unsafe_allow_html=True)

    with st.spinner("Groq AI is reviewing your resume... ✨"):
        try:
            feedback = get_groq_feedback(
                resume_text, job_desc, score,
                matched_skills, missing_skills, api_key
            )
            st.markdown(f'<div class="feedback-box">{feedback}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Error getting feedback: {str(e)}")

    # ── Row 3: Resume Preview ─────────────────────────────────────────────────
    with st.expander("📄 View Extracted Resume Text"):
        st.text(resume_text[:1500] + ("..." if len(resume_text) > 1500 else ""))

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#4b5268; font-size:0.85rem;'>"
    "Built by Kushal • Powered by Groq (Llama 3.3 70B) • "
    "<a href='https://github.com/kushalhallikar-spec/AI-Resume-Assistant' "
    "style='color:#7c6af7;'>GitHub</a></p>",
    unsafe_allow_html=True
)
