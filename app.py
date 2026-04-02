import streamlit as st
from utils import extract_text_from_pdf
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="AI Resume Assistant")

st.title("🚀 AI Resume Assistant")
st.write("Analyze your resume and get intelligent feedback")

st.markdown("---")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_desc = st.text_area("Paste Job Description")

SKILLS = [
    "python", "machine learning", "deep learning", "sql",
    "data analysis", "pandas", "numpy", "scikit-learn",
    "tensorflow", "keras", "excel", "power bi", "tableau",
    "nlp", "data visualization", "statistics"
]

if uploaded_file and job_desc:

    resume_text = extract_text_from_pdf(uploaded_file)

    # Clean text
    resume_clean = " ".join([
        w for w in resume_text.lower().split()
        if w not in ENGLISH_STOP_WORDS and len(w) > 2
    ])

    job_clean = " ".join([
        w for w in job_desc.lower().split()
        if w not in ENGLISH_STOP_WORDS and len(w) > 2
    ])

    # Similarity
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_clean, job_clean])
    score = round(cosine_similarity(vectors[0:1], vectors[1:2])[0][0] * 100, 2)

    st.subheader("🎯 Match Score")
    st.progress(int(score))
    st.write(f"{score}% match")

    st.markdown("---")

    # Skills
    resume_skills = [s for s in SKILLS if s in resume_clean]
    job_skills = [s for s in SKILLS if s in job_clean]

    missing_skills = list(set(job_skills) - set(resume_skills))
    matched_skills = list(set(job_skills) & set(resume_skills))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🚨 Missing Skills")
        if missing_skills:
            for skill in missing_skills:
                st.write(f"• {skill}")
        else:
            st.success("No major missing skills")

    with col2:
        st.subheader("✅ Matched Skills")
        if matched_skills:
            for skill in matched_skills:
                st.write(f"• {skill}")
        else:
            st.write("No matched skills found")

    st.markdown("---")

    # 🔥 SMART FEEDBACK (NO AI BUT LOOKS LIKE AI)
    st.subheader("🧠 Smart Feedback")

    if score > 75:
        st.success("Strong match. Your resume aligns well with the job requirements.")
    elif score > 50:
        st.warning("Moderate match. You can improve your resume by adding relevant skills.")
    else:
        st.error("Weak match. Significant improvements are needed.")

    if missing_skills:
        st.write("📌 Add these skills to improve your chances:")
        for skill in missing_skills[:5]:
            st.write(f"- {skill}")

    st.write("💡 Suggestions:")
    st.write("- Add project-based experience")
    st.write("- Use measurable achievements (e.g., improved accuracy by 20%)")
    st.write("- Highlight tools and technologies clearly")

    st.markdown("---")

    st.subheader("📄 Resume Preview")
    st.text(resume_text[:800])

st.markdown("---")
st.write("Built by Kushal • ML Engineer")