import streamlit as st
import fitz
from PIL import Image
import pytesseract
import io
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("📄 AI Resume Analyzer - For Job Matching")

# Tesseract کا راستہ - آپ کے لیپ ٹاپ کے حساب سے
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_any_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    if len(text.strip()) < 50:
        st.warning("Image PDF detected, running OCR...")
        text = ""
        for page in doc:
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            text += pytesseract.image_to_string(img) + "\n"
    return text

st.sidebar.header("Job Description")
job_desc = st.sidebar.text_area("Paste Job Description here", height=300)

uploaded_file = st.file_uploader("Upload your CV (PDF)", type="pdf")

skills_list = ["Data Analysis", "Data Visualization", "Deep Learning", "Git", "Machine Learning", "NLP", "Numpy", "Pandas", "Python", "SQL", "Tensorflow"]

if uploaded_file and job_desc:
    with st.spinner('Reading CV...'):
        resume_text = extract_text_from_any_pdf(uploaded_file)
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([resume_text, job_desc])
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0] * 100
        
        st.success(f"CV Read! {len(resume_text)} characters")
        st.metric("Match Percentage", f"{similarity:.2f}%")
        
        data = []
        for skill in skills_list:
            in_resume = "Yes" if skill.lower() in resume_text.lower() else "No"
            in_job = "Yes" if skill.lower() in job_desc.lower() else "No"
            data.append([skill, in_resume, in_job])
        
        df = pd.DataFrame(data, columns=["Skill", "In Resume", "Required for Job"])
        st.dataframe(df, use_container_width=True)